@echo off

REM Aller dans le dossier d'OBS
cd /d "C:\Program Files\obs-studio\bin\64bit"

REM Lancer OBS
start obs64.exe

REM Attendre 5 secondes
timeout /t 5 /nobreak >nul

REM Lancer le bot

cd /d "CheminVersLeBot\code"

start "" "CheminVersPython\python.exe" "CheminVersLeBot\bot.py"