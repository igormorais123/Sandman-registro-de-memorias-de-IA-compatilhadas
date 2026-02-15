@echo off
title Helena da Colmeia
cd /d C:\Users\IgorPC\Colmeia

REM Sync antes de abrir
echo Sincronizando com GitHub...
git pull origin main --quiet 2>nul

REM Abrir Claude Code
claude --print "Oi Helena! Leia HELENA.md e MEMORY.md. Assuma sua identidade e me cumprimente brevemente."
