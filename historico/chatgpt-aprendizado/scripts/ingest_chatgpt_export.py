#!/usr/bin/env python3
"""Ingestão do conversations.json (export do ChatGPT) para gerar:
- um índice de sessões em `sessoes/`
- candidatos de memória em `temp/candidatos_memoria.yaml`

Modo "seguro": não inventa nada; armazena evidências (conversation_id, timestamps, trechos).
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from pathlib import Path


def iso(ts: float | int | None) -> str:
    if ts is None:
        return ""
    try:
        return dt.datetime.utcfromtimestamp(ts).replace(microsecond=0).isoformat() + "Z"
    except Exception:
        return ""


def stable_id(*parts: str) -> str:
    h = hashlib.sha256("|".join(parts).encode("utf-8", errors="ignore")).hexdigest()
    return h[:12]


def extract_text(msg: dict) -> str:
    # Export costuma trazer content.parts (lista de strings)
    content = (msg or {}).get("content") or {}
    parts = content.get("parts")
    if isinstance(parts, list):
        return "\n".join([p for p in parts if isinstance(p, str)]).strip()
    # fallback
    if isinstance(content, dict) and isinstance(content.get("text"), str):
        return content["text"].strip()
    return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("conversations_json", type=str)
    ap.add_argument("--out", type=str, default=".")
    args = ap.parse_args()

    out = Path(args.out).resolve()
    sessions_dir = out / "sessoes"
    temp_dir = out / "temp"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(Path(args.conversations_json).read_text(encoding="utf-8"))

    # Export pode ser uma lista ou um dict com chave "conversations"
    conversations = data.get("conversations") if isinstance(data, dict) else data
    if not isinstance(conversations, list):
        raise SystemExit("Formato inesperado: não encontrei lista de conversas")

    candidates = []

    # Heurística: frases com marcadores de preferência/identidade/processo
    trigger = re.compile(
        r"\b(prefiro|gosto|quero|objetivo|diretriz|sempre|nunca|lembre|remember|meu sistema|rotina|framework)\b",
        re.IGNORECASE,
    )

    for conv in conversations:
        cid = str(conv.get("id") or conv.get("conversation_id") or "")
        title = (conv.get("title") or "").strip()
        ctime = iso(conv.get("create_time"))
        utime = iso(conv.get("update_time"))

        mapping = conv.get("mapping")
        if not isinstance(mapping, dict):
            continue

        # Ordenar por create_time do message quando disponível
        msgs = []
        for node in mapping.values():
            msg = (node or {}).get("message")
            if not isinstance(msg, dict):
                continue
            role = ((msg.get("author") or {}).get("role") or "").strip()
            text = extract_text(msg)
            if not text:
                continue
            ts = msg.get("create_time")
            msgs.append((ts if isinstance(ts, (int, float)) else 0, role, text))

        msgs.sort(key=lambda x: x[0])

        # Salvar sessão (transcrição bruta)
        sid = stable_id(cid, title, ctime, utime)
        session_path = sessions_dir / f"{sid}.md"
        with session_path.open("w", encoding="utf-8") as f:
            f.write(f"# Sessão {sid}\n\n")
            f.write(f"- conversation_id: {cid}\n")
            f.write(f"- título: {title}\n")
            f.write(f"- criado: {ctime}\n")
            f.write(f"- atualizado: {utime}\n\n")
            for ts, role, text in msgs:
                f.write(f"## {role} ({iso(ts)})\n\n")
                f.write(text)
                f.write("\n\n")

        # Gerar candidatos (heurística simples, para revisão humana)
        for ts, role, text in msgs:
            if role not in ("user", "assistant"):
                continue
            for line in [ln.strip() for ln in text.splitlines() if ln.strip()]:
                if len(line) < 18:
                    continue
                if not trigger.search(line):
                    continue
                # Normalizar como candidato
                cand_id = stable_id(sid, role, line[:200])
                candidates.append(
                    {
                        "id": cand_id,
                        "origem": {
                            "sessao": sid,
                            "conversation_id": cid,
                            "timestamp": iso(ts),
                            "role": role,
                        },
                        "texto": line,
                        "categoria_sugerida": "(revisar)",
                        "projeto": "(revisar)",
                        "confianca": "Baixa",
                        "tags": [],
                        "proxima_acao": "(revisar)",
                    }
                )

    # Salvar candidatos
    out_yaml = temp_dir / "candidatos_memoria.yaml"
    # YAML minimalista sem dependências
    with out_yaml.open("w", encoding="utf-8") as f:
        f.write("# candidatos extraídos automaticamente (REVISAR)\n")
        f.write("# Cada item traz evidência: sessão + conversation_id + timestamp\n\n")
        for c in candidates:
            f.write("- id: " + c["id"] + "\n")
            f.write("  projeto: " + json.dumps(c["projeto"], ensure_ascii=False) + "\n")
            f.write("  categoria: " + json.dumps(c["categoria_sugerida"], ensure_ascii=False) + "\n")
            f.write("  texto: " + json.dumps(c["texto"], ensure_ascii=False) + "\n")
            f.write("  confianca: " + json.dumps(c["confianca"], ensure_ascii=False) + "\n")
            f.write("  tags: []\n")
            f.write("  proxima_acao: " + json.dumps(c["proxima_acao"], ensure_ascii=False) + "\n")
            f.write("  origem:\n")
            f.write("    sessao: " + c["origem"]["sessao"] + "\n")
            f.write("    conversation_id: " + json.dumps(c["origem"]["conversation_id"], ensure_ascii=False) + "\n")
            f.write("    timestamp: " + json.dumps(c["origem"]["timestamp"], ensure_ascii=False) + "\n")
            f.write("    role: " + json.dumps(c["origem"]["role"], ensure_ascii=False) + "\n")

    print(f"OK: {len(conversations)} conversas processadas")
    print(f"Sessões: {sessions_dir}")
    print(f"Candidatos: {out_yaml}")


if __name__ == "__main__":
    main()
