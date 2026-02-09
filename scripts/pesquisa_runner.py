#!/usr/bin/env python3
"""
Pesquisa Runner — Pipeline completo de pesquisa eleitoral.
Interpreta pedido, cria pesquisa, executa, monitora e retorna resultados.

Uso direto:
  python3 pesquisa_runner.py criar --template tpl-basico-intencao-voto --amostra 100
  python3 pesquisa_runner.py criar --titulo "Rejeição Arruda" --perguntas perguntas.json --amostra 200
  python3 pesquisa_runner.py iniciar <pesquisa_id>
  python3 pesquisa_runner.py status <pesquisa_id>
  python3 pesquisa_runner.py resultados <pesquisa_id>
  python3 pesquisa_runner.py listar
  python3 pesquisa_runner.py templates

Uso como módulo (pelo Clawd):
  from pesquisa_runner import PesquisaRunner
  runner = PesquisaRunner()
  resultado = runner.pipeline_completo(pedido="intenção de voto com 200 eleitores")
"""

import json
import os
import sys
import time
import random
import re
from datetime import datetime
from pathlib import Path

# Adicionar path do api_client
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "pesquisador-eleitoral"))
from api_client import (
    get_token, _request, login,
    listar_eleitores, listar_candidatos, listar_templates, obter_template,
    criar_pesquisa, listar_pesquisas, obter_pesquisa, iniciar_pesquisa,
    status_pesquisa, respostas_pesquisa, estatisticas_eleitores,
)


# ============================================
# MAPEAMENTO DE TEMPLATES
# ============================================

TEMPLATE_MAP = {
    # Palavras-chave → template ID
    "intenção de voto": "tpl-basico-intencao-voto",
    "intencao de voto": "tpl-basico-intencao-voto",
    "voto": "tpl-basico-intencao-voto",
    "quem vota": "tpl-basico-intencao-voto",
    "votaria": "tpl-basico-intencao-voto",
    "cenário eleitoral": "tpl-cenario-eleitoral-completo",
    "cenario eleitoral": "tpl-cenario-eleitoral-completo",
    "cenário completo": "tpl-cenario-eleitoral-completo",
    "rejeição": "tpl-avancado-rejeicao-profunda",
    "rejeicao": "tpl-avancado-rejeicao-profunda",
    "rejeitado": "tpl-avancado-rejeicao-profunda",
    "não votaria": "tpl-avancado-rejeicao-profunda",
    "avaliação governo": "tpl-basico-avaliacao-governo",
    "avaliacao governo": "tpl-basico-avaliacao-governo",
    "aprovação": "tpl-basico-avaliacao-governo",
    "aprovacao": "tpl-basico-avaliacao-governo",
    "decisão de voto": "tpl-avancado-decisao-voto",
    "decisao de voto": "tpl-avancado-decisao-voto",
    "por que vota": "tpl-avancado-decisao-voto",
    "governador": "tpl-avancado-governador-df",
    "governador df": "tpl-avancado-governador-df",
    "perfil psicográfico": "tpl-avancado-perfil-psicografico",
    "perfil psicografico": "tpl-avancado-perfil-psicografico",
    "psicográfico": "tpl-avancado-perfil-psicografico",
    "desempenho parlamentar": "tpl-parlamentar-desempenho",
    "deputado": "tpl-parlamentar-desempenho",
    "senador": "tpl-parlamentar-desempenho",
    "representatividade": "tpl-parlamentar-representatividade",
    "podc estratégico": "tpl-podc-completo-estrategico",
    "podc estrategico": "tpl-podc-completo-estrategico",
    "podc tático": "tpl-podc-completo-tatico",
    "podc tatico": "tpl-podc-completo-tatico",
    "podc": "tpl-podc-completo-estrategico",
}

# Filtros de amostra por região
REGIOES_FILTROS = {
    "ceilândia": "Ceilândia", "ceilandia": "Ceilândia",
    "taguatinga": "Taguatinga", "samambaia": "Samambaia",
    "plano piloto": "Plano Piloto", "gama": "Gama",
    "planaltina": "Planaltina", "águas claras": "Águas Claras",
    "aguas claras": "Águas Claras", "sobradinho": "Sobradinho",
    "santa maria": "Santa Maria", "guará": "Guará", "guara": "Guará",
    "recanto": "Recanto das Emas", "sol nascente": "Sol Nascente/Pôr do Sol",
    "vicente pires": "Vicente Pires", "riacho fundo": "Riacho Fundo",
    "são sebastião": "São Sebastião", "sao sebastiao": "São Sebastião",
    "estrutural": "SCIA/Estrutural", "brazlândia": "Brazlândia",
    "lago norte": "Lago Norte", "lago sul": "Lago Sul",
    "sudoeste": "Sudoeste/Octogonal", "cruzeiro": "Cruzeiro",
}


class PesquisaRunner:
    """Pipeline completo de pesquisa eleitoral."""

    def __init__(self):
        self.token = None
        self._ensure_auth()

    def _ensure_auth(self):
        self.token = get_token()

    # ========================================
    # INTERPRETAÇÃO DO PEDIDO
    # ========================================

    def interpretar_pedido(self, texto: str) -> dict:
        """Interpreta um pedido em linguagem natural e retorna config da pesquisa."""
        texto_lower = texto.lower()
        config = {
            "template_id": None,
            "titulo": None,
            "amostra": 100,  # default
            "filtros": {},
            "candidato_foco": None,
            "tipo": "mista",
            "perguntas_custom": None,
        }

        # Detectar template
        for keyword, tpl_id in TEMPLATE_MAP.items():
            if keyword in texto_lower:
                config["template_id"] = tpl_id
                break

        # Detectar tamanho da amostra
        match = re.search(r'(\d+)\s*eleitor', texto_lower)
        if match:
            config["amostra"] = min(int(match.group(1)), 1000)
        elif "todos" in texto_lower or "1000" in texto_lower:
            config["amostra"] = 1000
        elif "pequena" in texto_lower or "rápida" in texto_lower or "rapida" in texto_lower:
            config["amostra"] = 50
        elif "média" in texto_lower or "media" in texto_lower:
            config["amostra"] = 200
        elif "grande" in texto_lower or "completa" in texto_lower:
            config["amostra"] = 500

        # Detectar região
        for keyword, regiao in REGIOES_FILTROS.items():
            if keyword in texto_lower:
                config["filtros"]["regiao_administrativa"] = regiao
                break

        # Detectar candidato foco
        candidatos_keywords = {
            "arruda": "José Roberto Arruda",
            "celina": "Maria Celina Leão Fontenele Montenegro",
            "damares": "Damares Regina Alves",
            "flávia arruda": "Flávia Carolina Peres Arruda",
            "flavia arruda": "Flávia Carolina Peres Arruda",
            "izalci": "Izalci Lucas Ferreira",
            "caputo": "Francisco Caputo",
            "grass": "Leandro Antonio Grass Peixoto",
            "leandro grass": "Leandro Antonio Grass Peixoto",
            "paulo neto": "Manoel Paulo de Andrade Neto",
            "paula belmonte": "Paula Moreno Paro Belmonte",
            "cappelli": "Ricardo Garcia Cappelli",
            "ibaneis": "Ibaneis",
        }
        for keyword, candidato in candidatos_keywords.items():
            if keyword in texto_lower:
                config["candidato_foco"] = candidato
                break

        # Detectar tipo
        if "quali" in texto_lower:
            config["tipo"] = "qualitativa"
        elif "quanti" in texto_lower:
            config["tipo"] = "quantitativa"

        # Gerar título automático
        if not config["titulo"]:
            parts = []
            if config["template_id"]:
                # Nome amigável do template
                tpl_names = {
                    "tpl-basico-intencao-voto": "Intenção de Voto",
                    "tpl-cenario-eleitoral-completo": "Cenário Eleitoral Completo",
                    "tpl-avancado-rejeicao-profunda": "Análise de Rejeição",
                    "tpl-basico-avaliacao-governo": "Avaliação de Governo",
                    "tpl-avancado-decisao-voto": "Decisão de Voto",
                    "tpl-avancado-governador-df": "Governador DF",
                    "tpl-avancado-perfil-psicografico": "Perfil Psicográfico",
                    "tpl-parlamentar-desempenho": "Desempenho Parlamentar",
                    "tpl-parlamentar-representatividade": "Representatividade",
                    "tpl-podc-completo-estrategico": "PODC Estratégico",
                    "tpl-podc-completo-tatico": "PODC Tático",
                }
                parts.append(tpl_names.get(config["template_id"], "Pesquisa"))
            else:
                parts.append("Pesquisa Eleitoral")

            if config["candidato_foco"]:
                parts.append(f"- {config['candidato_foco']}")

            if config["filtros"].get("regiao_administrativa"):
                parts.append(f"- {config['filtros']['regiao_administrativa']}")

            parts.append(f"- DF 2026")
            config["titulo"] = " ".join(parts)

        return config

    # ========================================
    # ADAPTAÇÃO DE TEMPLATES
    # ========================================

    def _adaptar_perguntas_template(self, perguntas_raw: list) -> list:
        """Adapta perguntas do template pro formato aceito pela API de criação."""
        # Mapeamento de tipos do template → tipos aceitos pela API
        tipo_map = {
            "aberta": "aberta",
            "aberta_longa": "aberta_longa",
            "unica": "multipla_escolha",  # API não tem "unica", usar multipla_escolha
            "multipla": "multipla_escolha",
            "escala": "escala_likert",
            "escala_likert": "escala_likert",
            "sim_nao": "sim_nao",
            "ranking": "ranking",
            "numerica": "numerica",
            "multipla_escolha": "multipla_escolha",
        }

        adaptadas = []
        for p in perguntas_raw:
            tipo_original = p.get("tipo", "aberta")
            tipo_api = tipo_map.get(tipo_original, "aberta")

            # Converter opções de objetos para strings
            opcoes_raw = p.get("opcoes", [])
            opcoes = []
            for op in opcoes_raw:
                if isinstance(op, dict):
                    opcoes.append(op.get("texto", op.get("valor", str(op))))
                else:
                    opcoes.append(str(op))

            pergunta = {
                "codigo": p.get("codigo", f"P{len(adaptadas)+1}"),
                "texto": p.get("texto", ""),
                "tipo": tipo_api,
                "categoria": p.get("categoria", "geral"),
                "obrigatoria": p.get("obrigatoria", True),
                "ordem": p.get("ordem", len(adaptadas) + 1),
            }

            # Adicionar instrução se existir
            if p.get("instrucoes"):
                pergunta["instrucoes"] = p["instrucoes"]

            # Adicionar opções só se não for aberta
            if opcoes and tipo_api not in ("aberta", "aberta_longa"):
                pergunta["opcoes"] = opcoes

            adaptadas.append(pergunta)

        return adaptadas

    # ========================================
    # SELEÇÃO DE AMOSTRA
    # ========================================

    def selecionar_amostra(self, tamanho: int, filtros: dict = None) -> list:
        """Seleciona IDs de eleitores para a amostra."""
        # Buscar todos os eleitores (paginado)
        all_ids = []
        pagina = 1
        while True:
            params = {"pagina": pagina, "por_pagina": 100}
            if filtros:
                params.update(filtros)
            result = _request("GET", "/api/v1/eleitores/", token=self.token, params=params)
            eleitores = result.get("eleitores", [])
            if not eleitores:
                break
            all_ids.extend([e["id"] for e in eleitores])
            if len(all_ids) >= result.get("total", 0):
                break
            pagina += 1

        # Amostra aleatória
        if len(all_ids) <= tamanho:
            return all_ids
        return random.sample(all_ids, tamanho)

    # ========================================
    # CRIAÇÃO DA PESQUISA
    # ========================================

    def criar(self, config: dict) -> dict:
        """Cria pesquisa a partir da config interpretada."""
        perguntas = config.get("perguntas_custom")

        # Se tem template, buscar perguntas dele e adaptar formato
        if config["template_id"] and not perguntas:
            try:
                tpl = obter_template(config["template_id"])
                raw_perguntas = tpl.get("perguntas", [])
                perguntas = self._adaptar_perguntas_template(raw_perguntas)
            except Exception as e:
                print(f"⚠️ Template não encontrado: {e}", file=sys.stderr)

        # Montar instrução geral
        instrucao = "Você está respondendo uma pesquisa eleitoral sobre o DF em 2026."
        if config.get("candidato_foco"):
            instrucao += f" A pesquisa tem foco em {config['candidato_foco']}."
        instrucao += " Responda de forma genuína, considerando sua experiência de vida, valores, classe social e visão política."

        # Selecionar amostra
        print(f"📊 Selecionando amostra de {config['amostra']} eleitores...")
        eleitor_ids = self.selecionar_amostra(config["amostra"], config.get("filtros"))
        print(f"✅ {len(eleitor_ids)} eleitores selecionados")

        # Criar pesquisa
        data = {
            "titulo": config["titulo"],
            "tipo": config.get("tipo", "mista"),
            "descricao": f"Pesquisa com {len(eleitor_ids)} eleitores do DF. "
                        f"Pesquisador: Clawd (INTEIA). Data: {datetime.now().strftime('%d/%m/%Y')}.",
            "instrucao_geral": instrucao,
            "eleitores_ids": eleitor_ids,
        }
        if perguntas:
            data["perguntas"] = perguntas

        result = _request("POST", "/api/v1/pesquisas/", data=data, token=self.token)
        pesquisa_id = result.get("id")
        print(f"✅ Pesquisa criada: {pesquisa_id}")
        print(f"   Título: {config['titulo']}")
        print(f"   Tipo: {config.get('tipo', 'mista')}")
        print(f"   Eleitores: {len(eleitor_ids)}")
        if perguntas:
            print(f"   Perguntas: {len(perguntas)}")

        return {
            "pesquisa_id": pesquisa_id,
            "config": config,
            "eleitor_ids": eleitor_ids,
            "resultado": result,
        }

    # ========================================
    # EXECUÇÃO VIA ENTREVISTAS (flow correto)
    # ========================================

    def criar_entrevista(self, titulo: str, perguntas: list,
                         eleitor_ids: list, tipo: str = "mista",
                         instrucao: str = None) -> dict:
        """Cria uma entrevista (o objeto que realmente executa no backend)."""
        # Adaptar perguntas pro formato PerguntaCreate da API
        perguntas_api = []
        for p in perguntas:
            pergunta = {
                "texto": p.get("texto", ""),
                "tipo": p.get("tipo", "aberta"),
                "obrigatoria": p.get("obrigatoria", True),
            }
            if p.get("opcoes") and p["tipo"] not in ("aberta", "aberta_longa"):
                pergunta["opcoes"] = p["opcoes"]
            if p.get("instrucoes") or p.get("instrucoes_ia"):
                pergunta["instrucoes_ia"] = p.get("instrucoes_ia", p.get("instrucoes", ""))
            perguntas_api.append(pergunta)

        data = {
            "titulo": titulo,
            "tipo": tipo,
            "perguntas": perguntas_api,
            "eleitores_ids": eleitor_ids,
        }
        if instrucao:
            data["descricao"] = instrucao

        result = _request("POST", "/api/v1/entrevistas/", data=data, token=self.token)
        return result

    def iniciar(self, entrevista_id: str, limite_custo: float = 100.0,
                batch_size: int = 10) -> dict:
        """Inicia execução de uma entrevista (processa eleitores com Claude)."""
        print(f"🚀 Iniciando entrevista {entrevista_id}...")
        try:
            data = {
                "usar_opus_para_complexas": True,
                "limite_custo_reais": limite_custo,
                "batch_size": batch_size,
                "delay_entre_batches_ms": 500,
            }
            result = _request("POST", f"/api/v1/entrevistas/{entrevista_id}/iniciar",
                            data=data, token=self.token)
            print(f"✅ Entrevista iniciada! Processando com Claude em background...")
            return result
        except Exception as e:
            print(f"❌ Erro ao iniciar: {e}")
            return {"error": str(e)}

    def monitorar(self, entrevista_id: str, intervalo: int = 15,
                  timeout: int = 1800, callback=None) -> dict:
        """Monitora progresso de uma entrevista até concluir ou timeout."""
        inicio = time.time()
        ultimo_progresso = -1

        while time.time() - inicio < timeout:
            try:
                # Endpoint de progresso da entrevista
                try:
                    status = _request("GET", f"/api/v1/entrevistas/{entrevista_id}/progresso",
                                    token=self.token)
                except:
                    status = _request("GET", f"/api/v1/entrevistas/{entrevista_id}",
                                    token=self.token)

                progresso = status.get("progresso", 0)
                st = status.get("status", "?")
                processados = status.get("eleitores_processados", 0)
                total = status.get("total_eleitores", 0)
                custo = status.get("custo_atual", status.get("custo_real", 0))

                if progresso != ultimo_progresso:
                    msg = f"📊 [{st}] {progresso}% — {processados}/{total} eleitores | R${custo:.2f}"
                    print(msg)
                    if callback:
                        callback(msg, status)
                    ultimo_progresso = progresso

                if st in ("concluida", "completed", "finalizada"):
                    print("✅ Entrevista concluída!")
                    return status

                if st in ("erro", "error", "falha"):
                    print(f"❌ Entrevista falhou: {status.get('erro_mensagem', '?')}")
                    return status

            except Exception as e:
                print(f"⚠️ Erro ao monitorar: {e}")

            time.sleep(intervalo)

        print(f"⏰ Timeout ({timeout}s) — entrevista ainda em andamento")
        return {"status": "timeout", "entrevista_id": entrevista_id}

    # ========================================
    # RESULTADOS
    # ========================================

    def obter_resultados(self, entrevista_id: str) -> dict:
        """Obtém resultados da entrevista."""
        try:
            entrevista = _request("GET", f"/api/v1/entrevistas/{entrevista_id}",
                                token=self.token)
            try:
                respostas = _request("GET", f"/api/v1/entrevistas/{entrevista_id}/respostas",
                                   token=self.token, params={"por_pagina": 500})
            except:
                respostas = {"respostas": entrevista.get("respostas", [])}
            return {
                "entrevista": entrevista,
                "respostas": respostas,
            }
        except Exception as e:
            return {"error": str(e)}

    def formatar_resultados(self, dados: dict) -> str:
        """Formata resultados para envio via WhatsApp."""
        entrevista = dados.get("entrevista", dados.get("pesquisa", {}))
        respostas = dados.get("respostas", {})

        lines = []
        lines.append(f"📊 *{entrevista.get('titulo', 'Pesquisa')}*")
        lines.append(f"Status: {entrevista.get('status', '?')}")
        lines.append(f"Eleitores: {entrevista.get('total_eleitores', '?')}")
        custo = entrevista.get('custo_real', 0)
        if custo:
            lines.append(f"Custo: R${custo:.2f}")
        lines.append(f"Progresso: {entrevista.get('progresso', 0)}%")
        lines.append("")

        resp_list = respostas.get("respostas", [])
        if isinstance(resp_list, list) and resp_list:
            lines.append(f"*Amostra de respostas ({min(5, len(resp_list))} de {len(resp_list)}):*")
            for r in resp_list[:5]:
                eleitor = r.get("eleitor_nome", r.get("eleitor_id", "?"))
                lines.append(f"\n👤 _{eleitor}_")
                resps = r.get("respostas", r.get("resposta", []))
                if isinstance(resps, list):
                    for resp in resps[:3]:
                        pergunta = str(resp.get("pergunta_texto", resp.get("codigo", "?")))[:60]
                        resposta = str(resp.get("resposta_texto", resp.get("valor", "?")))[:100]
                        lines.append(f"  P: {pergunta}")
                        lines.append(f"  R: {resposta}")
                elif isinstance(resps, str):
                    lines.append(f"  R: {resps[:200]}")

        return "\n".join(lines)

    # ========================================
    # PIPELINE COMPLETO
    # ========================================

    def pipeline_completo(self, pedido: str = None, config: dict = None,
                         callback=None) -> dict:
        """
        Pipeline completo: interpretar → criar → iniciar → monitorar → resultados.
        
        Args:
            pedido: Texto em linguagem natural do Igor
            config: Config já pronta (opcional, substitui pedido)
            callback: Função chamada com updates de progresso
        
        Returns:
            Dict com todas as etapas e resultado final
        """
        resultado = {"etapas": [], "sucesso": False}

        # 1. Interpretar
        if not config and pedido:
            config = self.interpretar_pedido(pedido)
            resultado["etapas"].append({"etapa": "interpretar", "config": config})
            if callback:
                callback(f"🧠 Interpretei: {config['titulo']} | {config['amostra']} eleitores | Template: {config['template_id']}", None)

        if not config:
            return {"error": "Preciso de um pedido ou config"}

        # 2. Selecionar amostra e preparar perguntas
        try:
            print(f"📊 Selecionando amostra de {config['amostra']} eleitores...")
            eleitor_ids = self.selecionar_amostra(config["amostra"], config.get("filtros"))
            print(f"✅ {len(eleitor_ids)} eleitores selecionados")

            perguntas = config.get("perguntas_custom")
            if config["template_id"] and not perguntas:
                tpl = obter_template(config["template_id"])
                perguntas = self._adaptar_perguntas_template(tpl.get("perguntas", []))

            if not perguntas:
                resultado["error"] = "Sem perguntas definidas (template não encontrado ou perguntas custom vazias)"
                return resultado

            resultado["etapas"].append({"etapa": "preparar", "eleitores": len(eleitor_ids), "perguntas": len(perguntas)})
        except Exception as e:
            resultado["error"] = f"Erro ao preparar: {e}"
            return resultado

        # 3. Criar entrevista (o objeto real que executa)
        try:
            instrucao = "Pesquisa eleitoral DF 2026."
            if config.get("candidato_foco"):
                instrucao += f" Foco em {config['candidato_foco']}."

            entrevista = self.criar_entrevista(
                titulo=config["titulo"],
                perguntas=perguntas,
                eleitor_ids=eleitor_ids,
                tipo=config.get("tipo", "mista"),
                instrucao=instrucao,
            )
            entrevista_id = entrevista.get("id")
            resultado["entrevista_id"] = entrevista_id
            resultado["etapas"].append({"etapa": "criar_entrevista", "id": entrevista_id})
            custo_est = entrevista.get("custo_estimado", 0)
            if callback:
                callback(f"✅ Entrevista criada: {entrevista_id} | Custo estimado: R${custo_est:.2f}", None)
            print(f"✅ Entrevista criada: {entrevista_id} | Custo estimado: R${custo_est:.2f}")
        except Exception as e:
            resultado["error"] = f"Erro ao criar entrevista: {e}"
            return resultado

        # 4. Iniciar execução (Claude processa em background no Render)
        try:
            inicio = self.iniciar(entrevista_id)
            resultado["etapas"].append({"etapa": "iniciar", "resultado": inicio})
            if callback:
                callback(f"🚀 Execução iniciada! Claude processando {len(eleitor_ids)} eleitores...", None)
        except Exception as e:
            resultado["error"] = f"Erro ao iniciar: {e}"
            resultado["etapas"].append({"etapa": "iniciar", "error": str(e)})
            return resultado

        # 5. Monitorar progresso
        status_final = self.monitorar(entrevista_id, callback=callback)
        resultado["etapas"].append({"etapa": "monitorar", "status": status_final.get("status")})

        # 6. Resultados
        if status_final.get("status") in ("concluida", "completed", "finalizada"):
            dados = self.obter_resultados(entrevista_id)
            resultado["resultados"] = dados
            resultado["resumo"] = self.formatar_resultados(dados)
            resultado["sucesso"] = True
            if callback:
                callback(resultado["resumo"], dados)

        return resultado


# ============================================
# CLI
# ============================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    runner = PesquisaRunner()

    if cmd == "criar":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--template", default=None)
        parser.add_argument("--titulo", default=None)
        parser.add_argument("--amostra", type=int, default=100)
        parser.add_argument("--tipo", default="mista")
        parser.add_argument("--regiao", default=None)
        parser.add_argument("--candidato", default=None)
        parser.add_argument("--perguntas", default=None, help="Arquivo JSON")
        parser.add_argument("--iniciar", action="store_true", help="Iniciar após criar")
        parser.add_argument("--limite-custo", type=float, default=100.0)
        args = parser.parse_args(sys.argv[2:])

        config = {
            "template_id": args.template,
            "titulo": args.titulo or f"Pesquisa Eleitoral DF - {datetime.now().strftime('%d/%m/%Y')}",
            "amostra": args.amostra,
            "tipo": args.tipo,
            "filtros": {},
            "candidato_foco": args.candidato,
            "perguntas_custom": None,
        }
        if args.regiao:
            config["filtros"]["regiao_administrativa"] = args.regiao
        if args.perguntas:
            config["perguntas_custom"] = json.loads(Path(args.perguntas).read_text())

        # Preparar perguntas
        perguntas = config.get("perguntas_custom")
        if config["template_id"] and not perguntas:
            tpl = obter_template(config["template_id"])
            perguntas = runner._adaptar_perguntas_template(tpl.get("perguntas", []))

        eleitor_ids = runner.selecionar_amostra(config["amostra"], config.get("filtros"))

        instrucao = "Pesquisa eleitoral DF 2026."
        if config.get("candidato_foco"):
            instrucao += f" Foco em {config['candidato_foco']}."

        result = runner.criar_entrevista(
            titulo=config["titulo"],
            perguntas=perguntas,
            eleitor_ids=eleitor_ids,
            tipo=config["tipo"],
            instrucao=instrucao,
        )
        entrevista_id = result.get("id")
        print(f"✅ Entrevista criada: {entrevista_id}")
        print(f"   Custo estimado: R${result.get('custo_estimado', 0):.2f}")
        print(f"   Eleitores: {len(eleitor_ids)}")

        if args.iniciar:
            runner.iniciar(entrevista_id, limite_custo=args.limite_custo)

    elif cmd == "iniciar":
        entrevista_id = sys.argv[2]
        runner.iniciar(entrevista_id)

    elif cmd == "status":
        entrevista_id = sys.argv[2]
        try:
            s = _request("GET", f"/api/v1/entrevistas/{entrevista_id}", token=runner.token)
            print(f"Status: {s.get('status')} | Progresso: {s.get('progresso', 0)}%")
            print(f"Eleitores: {s.get('eleitores_processados', 0)}/{s.get('total_eleitores', 0)}")
            print(f"Custo: R${s.get('custo_real', 0):.2f}")
        except:
            s = _request("GET", f"/api/v1/pesquisas/{entrevista_id}", token=runner.token)
            print(json.dumps(s, indent=2, ensure_ascii=False, default=str)[:3000])

    elif cmd == "monitorar":
        entrevista_id = sys.argv[2]
        runner.monitorar(entrevista_id)

    elif cmd == "resultados":
        pesquisa_id = sys.argv[2]
        dados = runner.obter_resultados(pesquisa_id)
        print(runner.formatar_resultados(dados))

    elif cmd == "listar":
        pesquisas = listar_pesquisas()
        for p in pesquisas.get("pesquisas", []):
            status_emoji = {"rascunho": "📝", "em_andamento": "⏳", "concluida": "✅", "erro": "❌"}.get(p["status"], "❓")
            print(f"  {status_emoji} [{p['id'][:8]}] {p['titulo']} | {p['status']} | {p['total_eleitores']} eleitores")

    elif cmd == "templates":
        templates = listar_templates()
        items = templates if isinstance(templates, list) else templates.get("templates", [])
        for t in items:
            print(f"  📋 [{t['id']}] {t.get('nome', t.get('titulo', '?'))}")

    elif cmd == "pipeline":
        # Pipeline completo a partir de texto natural
        pedido = " ".join(sys.argv[2:])
        print(f"🧠 Interpretando: '{pedido}'")
        resultado = runner.pipeline_completo(pedido=pedido)
        if resultado.get("sucesso"):
            print("\n" + resultado.get("resumo", ""))
        else:
            print(f"\n❌ {resultado.get('error', 'Falha desconhecida')}")
            print(json.dumps(resultado, indent=2, default=str)[:2000])

    elif cmd == "interpretar":
        # Só interpretar sem executar (debug)
        pedido = " ".join(sys.argv[2:])
        config = runner.interpretar_pedido(pedido)
        print(json.dumps(config, indent=2, ensure_ascii=False))

    else:
        print(f"❌ Comando desconhecido: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
