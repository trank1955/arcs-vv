@echo off
title ARCS-VV Blog Manager
cls
echo.
echo     🏠 ARCS-VV Blog Manager
echo     ========================
echo.
echo     Avvio dell'applicazione...
echo.

REM Controlla se Python è disponibile
python --version >nul 2>&1
if errorlevel 1 (
    echo     ❌ Python non trovato!
    echo     Installa Python da https://python.org
    echo.
    pause
    exit /b 1
)

REM Controlla se siamo nella cartella corretta
if not exist "blog_creator_simple.py" (
    echo     ❌ File del blog non trovati!
    echo     Assicurati di essere nella cartella corretta del sito ARCS-VV
    echo.
    pause
    exit /b 1
)

REM Avvia l'applicazione
python arcs_blog_manager.py

REM Se c'è un errore
if errorlevel 1 (
    echo.
    echo     ❌ Errore nell'avvio dell'applicazione
    echo.
    pause
)
