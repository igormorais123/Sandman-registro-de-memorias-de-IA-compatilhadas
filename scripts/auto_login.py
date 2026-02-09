#!/usr/bin/env python3
"""
Auto Login - Usa o cofre para login automático via Playwright
Nexo executa isso quando Igor pede acesso a um sistema
"""

import json
import sys
import asyncio
from pathlib import Path

VAULT_PATH = Path("/root/clawd/.secrets/vault.json")

def get_credentials(site_key):
    """Busca credenciais do cofre"""
    with open(VAULT_PATH) as f:
        vault = json.load(f)
    
    # Busca em web_logins
    if site_key in vault.get("web_logins", {}):
        return vault["web_logins"][site_key]
    
    # Busca em governo
    if site_key in vault.get("governo", {}):
        return vault["governo"][site_key]
    
    return None

async def login_sei(creds):
    """Login específico para SEI-GDF"""
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(creds["url"])
        
        # SEI usa iframe para login
        await page.wait_for_selector('input[name="txtUsuario"], #txtUsuario', timeout=10000)
        await page.fill('input[name="txtUsuario"], #txtUsuario', creds["usuario"])
        await page.fill('input[name="pwdSenha"], #pwdSenha', creds["senha"])
        await page.click('button[type="submit"], #sbmLogin')
        
        await page.wait_for_load_state('networkidle')
        
        # Captura página logada
        content = await page.content()
        title = await page.title()
        
        await browser.close()
        
        return {"success": True, "title": title, "logged_in": "Sair" in content or "usuario" in content.lower()}

async def login_generic(creds):
    """Login genérico - tenta campos comuns"""
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(creds["url"])
        await page.wait_for_load_state('networkidle')
        
        # Tenta encontrar campos de login comuns
        user_selectors = [
            'input[name="username"]', 'input[name="user"]', 'input[name="email"]',
            'input[name="login"]', 'input[type="email"]', '#username', '#email', '#user'
        ]
        pass_selectors = [
            'input[name="password"]', 'input[name="senha"]', 'input[name="pass"]',
            'input[type="password"]', '#password', '#senha'
        ]
        
        for sel in user_selectors:
            try:
                if await page.locator(sel).count() > 0:
                    await page.fill(sel, creds["usuario"])
                    break
            except:
                continue
        
        for sel in pass_selectors:
            try:
                if await page.locator(sel).count() > 0:
                    await page.fill(sel, creds["senha"])
                    break
            except:
                continue
        
        # Tenta submeter
        submit_selectors = [
            'button[type="submit"]', 'input[type="submit"]',
            'button:has-text("Entrar")', 'button:has-text("Login")', 'button:has-text("Acessar")'
        ]
        
        for sel in submit_selectors:
            try:
                if await page.locator(sel).count() > 0:
                    await page.click(sel)
                    break
            except:
                continue
        
        await page.wait_for_load_state('networkidle')
        
        title = await page.title()
        url = page.url
        
        await browser.close()
        
        return {"success": True, "title": title, "url": url}

async def main(site_key):
    creds = get_credentials(site_key)
    
    if not creds:
        print(f"Erro: Site '{site_key}' não encontrado no cofre")
        return
    
    if not creds.get("usuario") or not creds.get("senha"):
        print(f"Erro: Credenciais incompletas para '{site_key}'")
        print(f"Usuario: {'✓' if creds.get('usuario') else '✗'}")
        print(f"Senha: {'✓' if creds.get('senha') else '✗'}")
        return
    
    print(f"Fazendo login em: {creds.get('name', site_key)}")
    print(f"URL: {creds['url']}")
    
    if site_key == "sei_gdf":
        result = await login_sei(creds)
    else:
        result = await login_generic(creds)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: auto_login.py <site_key>")
        print("Exemplo: auto_login.py sei_gdf")
        sys.exit(1)
    
    asyncio.run(main(sys.argv[1]))
