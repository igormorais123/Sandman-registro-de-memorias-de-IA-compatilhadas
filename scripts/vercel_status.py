#!/usr/bin/env python3
"""Vercel Status — lista projetos e deployments."""
import os, sys, json, urllib.request

API_KEY = os.environ.get("VERCEL_API_KEY", "TSljjil4ENqZPkFA890sCz5s")
BASE = "https://api.vercel.com"

def api_get(path):
    req = urllib.request.Request(
        f"{BASE}{path}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def list_projects():
    data = api_get("/v9/projects")
    for p in data.get("projects", []):
        status = "🟢" if p.get("targets", {}).get("production") else "⚪"
        print(f"  {status} {p['name']}")
        if p.get("link", {}).get("repo"):
            print(f"     repo: {p['link']['repo']}")
        aliases = p.get("targets", {}).get("production", {}).get("alias", [])
        if aliases and isinstance(aliases, list):
            domains = [a for a in aliases if isinstance(a, str)]
            if domains:
                print(f"     domains: {', '.join(domains)}")

def list_deployments(project=None, limit=5):
    path = f"/v6/deployments?limit={limit}"
    if project:
        path += f"&projectId={project}"
    data = api_get(path)
    for d in data.get("deployments", []):
        state_emoji = {"READY": "🟢", "ERROR": "🔴", "BUILDING": "🟡"}.get(d.get("readyState", ""), "⚪")
        print(f"  {state_emoji} {d.get('name', '?')} — {d.get('readyState', '?')} — {d.get('url', '')}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "projects"
    
    if cmd == "projects":
        print("📦 Projetos Vercel:")
        list_projects()
    elif cmd == "deployments":
        proj = sys.argv[2] if len(sys.argv) > 2 else None
        print("🚀 Deployments recentes:")
        list_deployments(proj)
    else:
        print(f"Uso: vercel_status.py [projects|deployments] [project_id]")
