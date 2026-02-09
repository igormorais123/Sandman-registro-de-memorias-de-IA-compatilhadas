#!/usr/bin/env python3
"""
Job Orchestrator - Orquestrador de trabalhos longos via sub-agentes

Princípios:
1. NUNCA acumular contexto na sessão principal
2. Cada tarefa roda em sub-agente isolado (sessions_spawn)
3. Estado persiste em arquivo JSON, não na memória
4. Checkpoints obrigatórios a cada etapa
5. Retomável de qualquer ponto

Uso:
    # Definir job
    job_def = {
        "id": "analise-bardin-2026-02-03",
        "name": "Análise Bardin Reconvenção",
        "tasks": [
            {"id": "task_01", "prompt": "...", "input_files": [...], "depends_on": []},
            {"id": "task_02", "prompt": "...", "depends_on": ["task_01"]},
        ],
        "consolidation": {"prompt": "..."},
    }
    
    # Executar
    python3 orchestrator.py run job_def.json
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from job_state import JobManager

CLAWD_DIR = Path("/root/clawd")
JOBS_DIR = CLAWD_DIR / "jobs"


def load_job_definition(path: str) -> dict:
    """Carrega definição do job."""
    with open(path) as f:
        return json.load(f)


def save_task_result(job_id: str, task_id: str, result: dict):
    """Salva resultado de uma tarefa."""
    results_dir = JOBS_DIR / job_id / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    result_file = results_dir / f"{task_id}.json"
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    
    return result_file


def run_task_via_subagent(task: dict, job_id: str, timeout: int = 300) -> dict:
    """
    Executa tarefa via sub-agente isolado.
    Usa sessions_spawn para contexto separado.
    """
    # Construir prompt completo para o sub-agente
    prompt = f"""
TAREFA: {task.get('name', task['id'])}
JOB_ID: {job_id}
TASK_ID: {task['id']}

INSTRUÇÕES:
{task['prompt']}

INPUT FILES:
{json.dumps(task.get('input_files', []), indent=2)}

FORMATO DE OUTPUT:
Retorne APENAS um JSON válido com a estrutura esperada.
Não inclua texto antes ou depois do JSON.
"""
    
    # Por enquanto, usar exec com codex/gemini
    # TODO: Integrar com sessions_spawn quando disponível
    
    # Salvar prompt em arquivo temporário
    prompt_file = JOBS_DIR / job_id / "prompts" / f"{task['id']}_prompt.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(prompt)
    
    return {
        "status": "pending",
        "task_id": task['id'],
        "prompt_file": str(prompt_file),
        "message": "Task prepared - execute via sub-agent"
    }


def check_dependencies(task: dict, completed_tasks: set) -> bool:
    """Verifica se dependências da tarefa foram satisfeitas."""
    deps = task.get("depends_on", [])
    return all(dep in completed_tasks for dep in deps)


def run_job(job_def: dict, resume: bool = True) -> dict:
    """
    Executa um job completo.
    
    Args:
        job_def: Definição do job
        resume: Se True, retoma de onde parou
    
    Returns:
        Estado final do job
    """
    job_id = job_def["id"]
    job = JobManager(job_id)
    
    # Iniciar ou retomar
    state = job.start({
        "name": job_def.get("name", job_id),
        "total_tasks": len(job_def.get("tasks", [])),
        "completed_tasks": [],
        "failed_tasks": [],
        "pending_tasks": [t["id"] for t in job_def.get("tasks", [])]
    })
    
    if state.get("resume_count", 0) > 0:
        print(f"⟳ Retomando job {job_id} (tentativa #{state['resume_count']})")
        completed = set(state.get("completed_tasks", []))
    else:
        print(f"▶ Iniciando job {job_id}")
        completed = set()
    
    tasks = job_def.get("tasks", [])
    pending = [t for t in tasks if t["id"] not in completed]
    
    print(f"  {len(completed)}/{len(tasks)} tarefas completas")
    print(f"  {len(pending)} tarefas pendentes")
    
    # Processar tarefas em ordem de dependência
    max_iterations = len(tasks) * 2  # Evitar loop infinito
    iteration = 0
    
    while pending and iteration < max_iterations:
        iteration += 1
        progress_made = False
        
        for task in pending[:]:  # Cópia para poder remover
            if not check_dependencies(task, completed):
                continue
            
            print(f"\n→ Executando: {task['id']}")
            
            try:
                result = run_task_via_subagent(task, job_id)
                
                if result.get("status") == "pending":
                    # Tarefa preparada mas precisa execução manual via sub-agente
                    print(f"  📋 Prompt salvo: {result['prompt_file']}")
                    # Não remover de pending - será executado por sub-agente
                    break  # Sair do loop - orquestrador principal vai coordenar
                
                # Salvar resultado
                save_task_result(job_id, task["id"], result)
                
                # Atualizar estado
                completed.add(task["id"])
                pending.remove(task)
                
                job.checkpoint({
                    "completed_tasks": list(completed),
                    "pending_tasks": [t["id"] for t in pending],
                    "last_completed": task["id"]
                }, f"Completou {task['id']}")
                
                print(f"  ✓ Completo")
                progress_made = True
                
            except Exception as e:
                print(f"  ✗ Erro: {e}")
                state = job.checkpoint({
                    "failed_tasks": state.get("failed_tasks", []) + [task["id"]],
                    "last_error": str(e)
                }, f"Falhou {task['id']}: {e}")
                pending.remove(task)
        
        if not progress_made:
            # Nenhuma tarefa pode progredir - pode ser dependência circular ou aguardando sub-agentes
            break
    
    # Finalizar
    if not pending:
        job.complete({"total_completed": len(completed)})
        print(f"\n✓ Job {job_id} COMPLETO")
    else:
        print(f"\n⏸ Job {job_id} PAUSADO - {len(pending)} tarefas pendentes")
    
    return job.get_state()


def generate_job_definition(config: dict) -> dict:
    """Gera definição de job a partir de config simplificado."""
    tasks = []
    
    for i, item in enumerate(config.get("items", [])):
        task = {
            "id": f"task_{i+1:02d}_{item.get('name', 'unnamed')}",
            "name": item.get("name", f"Task {i+1}"),
            "prompt": item.get("prompt", ""),
            "input_files": item.get("input_files", []),
            "depends_on": item.get("depends_on", [])
        }
        tasks.append(task)
    
    return {
        "id": config.get("id", f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
        "name": config.get("name", "Unnamed Job"),
        "tasks": tasks,
        "consolidation": config.get("consolidation", {})
    }


# CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: orchestrator.py <comando> [args]")
        print("Comandos:")
        print("  run <job_def.json>     - Executa job")
        print("  status <job_id>        - Status do job")
        print("  resume <job_id>        - Retoma job pausado")
        print("  list                   - Lista jobs")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "run":
        if len(sys.argv) < 3:
            print("Uso: orchestrator.py run <job_def.json>")
            sys.exit(1)
        job_def = load_job_definition(sys.argv[2])
        run_job(job_def)
    
    elif cmd == "status":
        if len(sys.argv) < 3:
            print("Uso: orchestrator.py status <job_id>")
            sys.exit(1)
        job = JobManager(sys.argv[2])
        print(json.dumps(job.get_state(), indent=2, ensure_ascii=False))
    
    elif cmd == "resume":
        if len(sys.argv) < 3:
            print("Uso: orchestrator.py resume <job_id>")
            sys.exit(1)
        # Carregar definição original
        job_def_file = JOBS_DIR / sys.argv[2] / "job_def.json"
        if not job_def_file.exists():
            print(f"Definição do job não encontrada: {job_def_file}")
            sys.exit(1)
        job_def = load_job_definition(str(job_def_file))
        run_job(job_def, resume=True)
    
    elif cmd == "list":
        jobs = JobManager.list_jobs()
        if not jobs:
            print("Nenhum job encontrado.")
        for j in jobs:
            status_emoji = {"running": "⏳", "completed": "✓", "failed": "✗"}.get(j['status'], "?")
            print(f"{status_emoji} {j['job_id']}: {j['status']}")
            if j.get('last_checkpoint'):
                print(f"   └─ Último checkpoint: {j['last_checkpoint'].get('message', 'N/A')}")
    
    else:
        print(f"Comando desconhecido: {cmd}")
        sys.exit(1)
