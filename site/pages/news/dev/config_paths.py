# Configurazione percorsi per ARCS-VV Blog System
# Questo file viene importato da tutti i moduli del blog per i percorsi corretti

from pathlib import Path
import os

# Se l'utente lancia l'eseguibile dalla radice del sito (consigliato), usa CWD
CWD = Path.cwd()
if (CWD / "templates").exists() and (CWD / "pages").exists():
	BASE_DIR = CWD
else:
	# Fallback: relativo al file (per esecuzione da sorgente)
	DEV_DIR = Path(__file__).resolve().parent
	NEWS_DIR_FALLBACK = DEV_DIR.parent           # .../pages/news
	PAGES_DIR_FALLBACK = NEWS_DIR_FALLBACK.parent         # .../pages
	BASE_DIR = PAGES_DIR_FALLBACK.parent         # .../ (radice del sito)

# Percorsi principali
TEMPLATES_DIR = BASE_DIR / "templates"
MAIN_CSS = BASE_DIR / "main.css"
ICONS_DIR = BASE_DIR / "icons"
IMAGES_DIR = BASE_DIR / "immagini"
PAGES_DIR = BASE_DIR / "pages"
NEWS_DIR = PAGES_DIR / "news"
PDF_DIR = NEWS_DIR / "pdf"         # Allegati PDF specifici del blog/news

# Dati del blog/news
NEWS_JSON_PATH = NEWS_DIR / "news.json"
POSTS_DIR = NEWS_DIR                # Salva i post direttamente in pages/news
NEWS_INDEX_FILE = PAGES_DIR / "news.html"

print("✅ Configurazione percorsi caricata:")
print(f"   📁 BASE_DIR: {BASE_DIR}")
print(f"   📁 PAGES_DIR: {PAGES_DIR}")
print(f"   📁 NEWS_DIR: {NEWS_DIR}")
print(f"   📁 TEMPLATES_DIR: {TEMPLATES_DIR}")
print(f"   📄 NEWS_JSON_PATH: {NEWS_JSON_PATH}")
print(f"   📁 POSTS_DIR: {POSTS_DIR}")
print(f"   📁 PDF_DIR: {PDF_DIR}")