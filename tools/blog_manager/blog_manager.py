#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog Manager per ARCS-VV
Gestisce la generazione e aggiornamento delle news
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_project_root() -> Path:
    """Ottiene la root del progetto ARCS-VV"""
    # Se siamo nella directory tools/, sali di un livello
    current_dir = Path.cwd()
    if current_dir.name == 'tools':
        return current_dir.parent
    # Se siamo nella root del progetto
    elif (current_dir / 'pages' / 'news').exists():
        return current_dir
    # Altrimenti, cerca la root del progetto
    else:
        # Cerca la directory che contiene 'pages/news'
        for parent in current_dir.parents:
            if (parent / 'pages' / 'news').exists():
                return parent
        # Fallback: usa la directory corrente
        return current_dir

# Percorsi - usa sempre il percorso assoluto dalla root del progetto
ROOT = get_project_root()
NEWS_DIR = ROOT / "pages" / "news"
NEWS_JSON_PATH = NEWS_DIR / "news.json"
TEMPLATE_PATH = ROOT / "templates" / "news_template.html"

class NewsArticle:
    def __init__(self, title: str, slug: str, author: str = "ARCS-VV", 
                 date: str = None, image: str = None, summary: str = None):
        self.title = title
        self.slug = slug
        self.author = author
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.image = image
        self.summary = summary
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "slug": self.slug,
            "author": self.author,
            "date": self.date,
            "image": self.image,
            "summary": self.summary
        }

def slugify(title: str) -> str:
    """Converte un titolo in uno slug URL-friendly"""
    # Converti in minuscolo
    slug = title.lower()
    # Sostituisci caratteri speciali con trattini
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Sostituisci spazi con trattini
    slug = re.sub(r'[-\s]+', '-', slug)
    # Rimuovi trattini iniziali e finali
    slug = slug.strip('-')
    return slug

def extract_news_from_html() -> List[NewsArticle]:
    """Estrae le informazioni delle news dai file HTML esistenti"""
    articles = []
    
    if not NEWS_DIR.exists():
        logger.error(f"Directory news non trovata: {NEWS_DIR}")
        return articles
    
    for html_file in NEWS_DIR.glob("*.html"):
        if html_file.name == "news.html":
            continue
            
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Estrai titolo
            title_match = re.search(r'<title>([^<]+)</title>', content)
            title = title_match.group(1).strip() if title_match else html_file.stem
            
            # Estrai data
            date_match = re.search(r'Pubblicato il (\d{4}-\d{2}-\d{2})', content)
            date = date_match.group(1) if date_match else "2025-08-09"
            
            # Estrai immagine
            img_match = re.search(r'src="[^"]*/([^/"]+\.(?:jpg|jpeg|png))"', content)
            image = img_match.group(1) if img_match else None
            
            # Estrai riassunto
            summary_match = re.search(r'<p>([^<]+)</p>', content)
            summary = summary_match.group(1).strip() if summary_match else None
            
            # Crea slug dal nome del file
            slug = html_file.stem
            
            article = NewsArticle(
                title=title,
                slug=slug,
                date=date,
                image=image,
                summary=summary
            )
            articles.append(article)
            
        except Exception as e:
            logger.error(f"Errore nel parsing di {html_file}: {e}")
    
    return articles

def generate_news_json_from_html() -> int:
    """Genera news.json dai file HTML esistenti"""
    articles = extract_news_from_html()
    
    if not articles:
        logger.warning("Nessun articolo trovato")
        return 0
    
    # Converti in dizionari
    news_data = [article.to_dict() for article in articles]
    
    # Salva in news.json
    try:
        with open(NEWS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Generato news.json con {len(articles)} articoli")
        return len(articles)
    except Exception as e:
        logger.error(f"Errore nel salvataggio di news.json: {e}")
        return 0

def create_news_article(title: str, summary: str, image: str = None, 
                       author: str = "ARCS-VV") -> bool:
    """Crea un nuovo articolo news"""
    slug = slugify(title)
    html_file = NEWS_DIR / f"{slug}.html"
    
    if html_file.exists():
        logger.warning(f"Articolo con slug '{slug}' già esiste")
        return False
    
    # Crea il contenuto HTML
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} – ARCS-VV</title>
  <link rel="icon" type="image/x-icon" href="../../icons/favicon.ico">
  <link rel="stylesheet" href="../../main.css?v=1080">
</head>
<body>
  <div id="menu-inject"></div>
  <script src="../../menu.js"></script>
  <main style="max-width:800px;margin:auto;">
    <h1>{title} – ARCS-VV</h1>
    <p style="color:#888;font-size:0.95em;">Pubblicato il {datetime.now().strftime('%Y-%m-%d')} da {author}</p>
    
    {f'<img src="../../immagini/{image}" alt="{title}" style="width:100%;height:300px;object-fit:cover;border-radius:8px;margin-bottom:1.5em;">' if image else ''}
    
    <div class="blog-content">
      <p>{summary}</p>
    </div>
    
    <p><a href="../news.html">&larr; Torna all'elenco news</a></p>
  </main>
</body>
</html>"""
    
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Creato nuovo articolo: {html_file}")
        
        # Aggiorna news.json
        generate_news_json_from_html()
        
        return True
    except Exception as e:
        logger.error(f"Errore nella creazione dell'articolo: {e}")
        return False

def update_news_page() -> bool:
    """Aggiorna la pagina principale delle news"""
    news_file = ROOT / "pages" / "news.html"
    
    if not news_file.exists():
        logger.error(f"File news.html non trovato: {news_file}")
        return False
    
    # Leggi le news dal JSON
    try:
        with open(NEWS_JSON_PATH, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
    except Exception as e:
        logger.error(f"Errore nella lettura di news.json: {e}")
        return False
    
    # TODO: Implementare la generazione automatica della pagina news.html
    # Per ora, aggiorniamo solo il JSON
    logger.info(f"News.json aggiornato con {len(news_data)} articoli")
    return True

if __name__ == "__main__":
    # Test delle funzionalità
    print("Blog Manager per ARCS-VV")
    print("=" * 40)
    print(f"Root directory: {ROOT}")
    print(f"News directory: {NEWS_DIR}")
    print(f"News JSON path: {NEWS_JSON_PATH}")
    print("=" * 40)
    
    # Genera news.json dai file HTML esistenti
    count = generate_news_json_from_html()
    print(f"Generati {count} articoli in news.json")
    
    # Esempio di creazione di un nuovo articolo
    # create_news_article(
    #     title="Nuova iniziativa di solidarietà",
    #     summary="Descrizione della nuova iniziativa...",
    #     image="blog-cover_photo-300.jpeg"
    # )
