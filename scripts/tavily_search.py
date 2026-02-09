#!/usr/bin/env python3
"""Tavily Deep Search — pesquisa avançada com extração de conteúdo."""
import os, sys, json, urllib.request

API_KEY = os.environ.get("TAVILY_API_KEY", "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")

def search(query, max_results=5, search_depth="advanced", include_answer=True):
    data = json.dumps({
        "api_key": API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": include_answer,
        "include_raw_content": False
    }).encode()
    
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: tavily_search.py 'sua query' [max_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_r = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    result = search(query, max_results=max_r)
    
    if result.get("answer"):
        print(f"\n📋 Resposta: {result['answer']}\n")
    
    for i, r in enumerate(result.get("results", []), 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        print(f"   {r.get('content', '')[:200]}")
        print()
