#!/usr/bin/env python3
"""
Job State Manager - Gerenciador de estado para trabalhos longos
Garante que trabalhos sobrevivem a crashes de sessão.

Uso:
    from job_state import JobManager
    
    job = JobManager("analise-bardin")
    job.start({"total_arquivos": 7, "arquivos_processados": 0})
    
    for arquivo in arquivos:
        # processar...
        job.checkpoint({"arquivos_processados": i, "ultimo_arquivo": arquivo})
    
    job.complete({"resultado": "sucesso"})
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
import fcntl

JOBS_DIR = Path("/root/clawd/jobs")

class JobManager:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.job_file = JOBS_DIR / f"{job_id}.json"
        JOBS_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load(self) -> dict:
        """Carrega estado atual do job."""
        if self.job_file.exists():
            with open(self.job_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save(self, state: dict):
        """Salva estado com lock para evitar race conditions."""
        # Escrita atômica: escreve em .tmp e renomeia
        tmp_file = self.job_file.with_suffix('.tmp')
        with open(tmp_file, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            json.dump(state, f, indent=2, ensure_ascii=False, default=str)
            f.flush()
            os.fsync(f.fileno())
        tmp_file.rename(self.job_file)
    
    def start(self, initial_state: dict = None) -> dict:
        """Inicia ou retoma um job."""
        existing = self._load()
        
        if existing and existing.get("status") not in ["completed", "failed"]:
            # Job existe e não terminou - retomar
            existing["resumed_at"] = datetime.now().isoformat()
            existing["resume_count"] = existing.get("resume_count", 0) + 1
            self._save(existing)
            return existing
        
        # Novo job
        state = {
            "job_id": self.job_id,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "checkpoints": [],
            "resume_count": 0,
            **(initial_state or {})
        }
        self._save(state)
        return state
    
    def checkpoint(self, data: dict, message: str = None):
        """Salva checkpoint com dados parciais."""
        state = self._load()
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "data": data
        }
        state["checkpoints"].append(checkpoint)
        state["last_checkpoint"] = checkpoint
        state.update(data)  # Merge dados no estado principal
        self._save(state)
        return state
    
    def get_state(self) -> dict:
        """Retorna estado atual."""
        return self._load()
    
    def get_last_checkpoint(self) -> Optional[dict]:
        """Retorna último checkpoint."""
        state = self._load()
        return state.get("last_checkpoint")
    
    def complete(self, result: dict = None):
        """Marca job como completo."""
        state = self._load()
        state["status"] = "completed"
        state["completed_at"] = datetime.now().isoformat()
        if result:
            state["result"] = result
        self._save(state)
        return state
    
    def fail(self, error: str):
        """Marca job como falho."""
        state = self._load()
        state["status"] = "failed"
        state["failed_at"] = datetime.now().isoformat()
        state["error"] = error
        self._save(state)
        return state
    
    def is_resumable(self) -> bool:
        """Verifica se job pode ser retomado."""
        state = self._load()
        return state.get("status") == "running"
    
    @staticmethod
    def list_jobs(status: str = None) -> list:
        """Lista todos os jobs."""
        jobs = []
        for f in JOBS_DIR.glob("*.json"):
            with open(f) as fp:
                job = json.load(fp)
                if status is None or job.get("status") == status:
                    jobs.append(job)
        return sorted(jobs, key=lambda x: x.get("started_at", ""), reverse=True)


# CLI para uso direto
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: job_state.py <comando> [job_id] [dados_json]")
        print("Comandos: list, status, start, checkpoint, complete, fail")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        jobs = JobManager.list_jobs(status_filter)
        for job in jobs:
            print(f"{job['job_id']}: {job['status']} ({job.get('started_at', 'N/A')})")
    
    elif cmd == "status":
        if len(sys.argv) < 3:
            print("Uso: job_state.py status <job_id>")
            sys.exit(1)
        job = JobManager(sys.argv[2])
        print(json.dumps(job.get_state(), indent=2, ensure_ascii=False))
    
    elif cmd == "start":
        if len(sys.argv) < 3:
            print("Uso: job_state.py start <job_id> [initial_state_json]")
            sys.exit(1)
        job = JobManager(sys.argv[2])
        initial = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        state = job.start(initial)
        print(f"Job {sys.argv[2]}: {'RETOMADO' if state.get('resume_count', 0) > 0 else 'INICIADO'}")
        print(json.dumps(state, indent=2, ensure_ascii=False))
    
    elif cmd == "checkpoint":
        if len(sys.argv) < 4:
            print("Uso: job_state.py checkpoint <job_id> <data_json> [message]")
            sys.exit(1)
        job = JobManager(sys.argv[2])
        data = json.loads(sys.argv[3])
        msg = sys.argv[4] if len(sys.argv) > 4 else None
        state = job.checkpoint(data, msg)
        print(f"Checkpoint salvo: {state['last_checkpoint']}")
    
    elif cmd == "complete":
        if len(sys.argv) < 3:
            print("Uso: job_state.py complete <job_id> [result_json]")
            sys.exit(1)
        job = JobManager(sys.argv[2])
        result = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        state = job.complete(result)
        print(f"Job {sys.argv[2]} COMPLETO")
    
    elif cmd == "fail":
        if len(sys.argv) < 4:
            print("Uso: job_state.py fail <job_id> <error_message>")
            sys.exit(1)
        job = JobManager(sys.argv[2])
        job.fail(sys.argv[3])
        print(f"Job {sys.argv[2]} FALHOU: {sys.argv[3]}")
    
    else:
        print(f"Comando desconhecido: {cmd}")
        sys.exit(1)
