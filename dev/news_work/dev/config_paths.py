# Configurazione percorsi per ARCS-VV Blog System
# Questo file viene importato da tutti i moduli del blog per i percorsi corretti

import os

# Percorso base del progetto (radice)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Percorsi principali
PAGES_DIR = os.path.join(BASE_DIR, "pages")
NEWS_DIR = os.path.join(PAGES_DIR, "news")
IMAGES_DIR = os.path.join(BASE_DIR, "immagini")
PDF_DIR = os.path.join(BASE_DIR, "pdf")  # se esiste
DOCS_DIR = os.path.join(BASE_DIR, "documenti")  # se esiste
POSTS_DIR = r"C:\Users\stefa\OneDrive\arcs-vv-nuovo\pages\news"

# File principali
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
NEWS_FILE = os.path.join(NEWS_DIR, "news.html")
MAIN_CSS = os.path.join(BASE_DIR, "main.css")

# Template e configurazioni
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

print(f"✅ Configurazione percorsi caricata:")
print(f"   📁 BASE_DIR: {BASE_DIR}")
print(f"   📁 PAGES_DIR: {PAGES_DIR}")
print(f"   📁 NEWS_DIR: {NEWS_DIR}")
print(f"   📁 IMAGES_DIR: {IMAGES_DIR}")
print(f"   📁 PDF_DIR: {PDF_DIR}")
print(f"   📁 TEMPLATES_DIR: {TEMPLATES_DIR}")