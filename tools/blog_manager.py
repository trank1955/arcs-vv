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
    
    # Determina se c'è un video e genera il contenuto appropriato
    video_embed = None
    if image:
        if 'youtube' in image.lower():
            video_id = image.replace('youtube_', '')
            video_embed = f"https://www.youtube.com/embed/{video_id}"
        elif 'vimeo' in image.lower():
            video_id = image.replace('vimeo_', '')
            video_embed = f"https://player.vimeo.com/video/{video_id}"
    
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
    
    {f'<div style="margin-bottom:1.5em;"><iframe width="100%" height="400" src="{video_embed}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius:8px;"></iframe></div>' if video_embed else f'<img src="../../immagini/{image}" alt="{title}" style="width:100%;height:300px;object-fit:cover;border-radius:8px;margin-bottom:1.5em;">' if image else ''}
    
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
    """Aggiorna la pagina principale delle news con le nuove news dal JSON"""
    
    news_html_path = ROOT / "pages" / "news.html"
    
    if not news_html_path.exists():
        logger.error(f"File news.html non trovato: {news_html_path}")
        return False
    
    # Leggi le news dal JSON
    try:
        with open(NEWS_JSON_PATH, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        logger.info(f"Caricate {len(news_data)} news dal JSON")
    except Exception as e:
        logger.error(f"Errore nella lettura di news.json: {e}")
        return False
    
    # Leggi la pagina HTML esistente
    try:
        with open(news_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        logger.info("Pagina news.html caricata")
    except Exception as e:
        logger.error(f"Errore nella lettura di news.html: {e}")
        return False
    
    # Ordina le news per data (più recenti in cima)
    news_data_sorted = sorted(news_data, key=lambda x: x['date'], reverse=True)
    logger.info(f"News ordinate cronologicamente (più recenti in cima)")
    
    # Crea il contenuto HTML per tutte le news (non solo le ultime 5)
    news_html = ""
    
    for i, news in enumerate(news_data_sorted):
        # Apri una nuova riga se è l'inizio di una coppia
        if i % 2 == 0:
            news_html += "  <!-- COPPIA " + str((i // 2) + 1) + " -->\n      <tr>\n"
        
        # Determina l'immagine da usare e se c'è un video
        image_src = "../immagini/blog-cover_photo-300.jpeg"  # Default
        video_embed = None
        
        if news.get('image'):
            if 'youtube' in news['image'].lower():
                # Estrai ID video YouTube
                video_id = news['image'].replace('youtube_', '')
                image_src = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                video_embed = f"https://www.youtube.com/embed/{video_id}"
            elif 'vimeo' in news['image'].lower():
                # Estrai ID video Vimeo
                video_id = news['image'].replace('vimeo_', '')
                image_src = f"https://vumbnail.com/{video_id}.jpg"
                video_embed = f"https://player.vimeo.com/video/{video_id}"
            elif 'hqdefault' in news['image']:
                image_src = "https://img.youtube.com/vi/gYX7G39FUbU/hqdefault.jpg"
            elif 'blog-med' in news['image']:
                image_src = f"../immagini/{news['image']}"
            else:
                image_src = f"../immagini/{news['image']}"
        
        # Formatta la data
        try:
            date_obj = datetime.strptime(news['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d %B %Y')
        except:
            formatted_date = news['date']
        
        # Genera il contenuto HTML per la news
        if video_embed:
            # News con video - mostra thumbnail e link al video
            news_html += f"""        <td width="50%" valign="top">
          <div class="article-card" style="background: transparent; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="position: relative;">
              <img src="{image_src}" alt="{news['title']}" style="width: 100%; height: 220px; object-fit: cover; display: block;">
              <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.8); border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 24px;">▶️</span>
              </div>
            </div>
            <div style="padding: 1.5em;">
              <div style="color: #666; font-size: 0.9em; margin-bottom: 0.5em;">📅 {formatted_date}</div>
              <h2 style="color: #006699; margin: 0 0 1em 0; font-size: 1.3em; line-height: 1.3;">{news['title']}</h2>
              <p style="color: #555; line-height: 1.6; margin-bottom: 1.5em;">{news.get('summary', 'Nessun riassunto disponibile.')}</p>
              <a href="news/{news['slug']}.html" style="color: #006699; text-decoration: none; font-weight: 600;">🎥 Guarda il video →</a>
            </div>
          </div>
        </td>"""
        else:
            # News normale - mostra immagine e link "leggi tutto"
            news_html += f"""        <td width="50%" valign="top">
          <div class="article-card" style="background: transparent; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
            <img src="{image_src}" alt="{news['title']}" style="width: 100%; height: 220px; object-fit: cover; display: block;">
            <div style="padding: 1.5em;">
              <div style="color: #666; font-size: 0.9em; margin-bottom: 0.5em;">📅 {formatted_date}</div>
              <h2 style="color: #006699; margin: 0 0 1em 0; font-size: 1.3em; line-height: 1.3;">{news['title']}</h2>
              <p style="color: #555; line-height: 1.6; margin-bottom: 1.5em;">{news.get('summary', 'Nessun riassunto disponibile.')}</p>
              <a href="news/{news['slug']}.html" style="color: #006699; text-decoration: none; font-weight: 600;">Leggi tutto →</a>
            </div>
          </div>
        </td>"""
        
        # Chiudi la riga se è la fine di una coppia O se è l'ultima news
        if i % 2 == 1:
            # Fine di una coppia completa
            news_html += "\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
        elif i == len(news_data) - 1:
            # Ultima news - completa la riga se necessario
            if i % 2 == 0:
                # Ultima news in posizione pari (riga incompleta)
                news_html += "\n        <td width=\"50%\" valign=\"top\"></td>\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
            else:
                # Ultima news in posizione dispari (riga completa)
                news_html += "\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
    
    # Crea la nuova tabella completa
    new_table = f"""  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;max-width:900px;">

{news_html}
  </table>"""
    
    # Trova la sezione della tabella principale e sostituiscila completamente
    table_start = "  <table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"margin:0 auto;max-width:900px;\">"
    mobile_section = "      <!-- Layout alternativo per MOBILE -->"
    
    if table_start in html_content and mobile_section in html_content:
        # Trova l'inizio della tabella e l'inizio della sezione mobile
        start_pos = html_content.find(table_start)
        mobile_pos = html_content.find(mobile_section)
        
        if start_pos < mobile_pos:
            # Sostituisci tutto il contenuto dalla tabella alla sezione mobile
            html_content = html_content[:start_pos] + new_table + "\n\n      " + html_content[mobile_pos:]
            logger.info("Contenuto dalla tabella alla sezione mobile sostituito completamente")
        else:
            logger.error("Ordine errato: sezione mobile prima della tabella")
            return False
    else:
        logger.error("Tabella principale o sezione mobile non trovata nella pagina HTML")
        return False
    
    # Salva la pagina aggiornata
    try:
        with open(news_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Pagina news.html aggiornata e salvata")
        return True
    except Exception as e:
        logger.error(f"Errore nel salvataggio di news.html: {e}")
        return False

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
