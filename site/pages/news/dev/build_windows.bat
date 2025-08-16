@echo off
setlocal

REM Attiva virtualenv se presente
if exist .venv\Scripts\activate.bat (
	call .venv\Scripts\activate.bat
)

REM Installa dipendenze necessarie
python -m pip install --upgrade pip
python -m pip install -r ..\..\..\requirements.txt pyinstaller

REM Costruisce EXE a file singolo
pyinstaller --noconsole --onefile --name ArcsBlogManager --add-data "..\..\..\templates;templates" --add-data "..\..\..\pages;pages" --add-data "..\..\..\immagini;immagini" --add-data "..\..\..\icons;icons" --add-data "..\..\..\main.css;main.css" arcs_blog_manager.py

echo.
echo Build completata. Trovi l'eseguibile in dist\ArcsBlogManager.exe
endlocal