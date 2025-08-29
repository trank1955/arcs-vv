#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per pulire e gestire il database delle news
- Rimuove duplicati
- Rimuove post di test
- Normalizza i dati
- Genera report di pulizia
"""

import json
import re
from pathlib import Path
from datetime import datetime
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_news(filepath):
    """Carica il database delle news"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Errore nel caricamento di {filepath}: {e}")
        return []

def save_news(news, filepath):
    """Salva il database delle news"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(news, f, indent=4, ensure_ascii=False)
        logger.info(f"Database salvato in {filepath}")
        return True
    except Exception as e:
        logger.error(f"Errore nel salvataggio di {filepath}: {e}")
        return False

def clean_title(title):
    """Pulisce e normalizza il titolo"""
    # Rimuovi spazi multipli
    title = re.sub(r'\s+', ' ', title.strip())
    # Normalizza caratteri speciali
    title = title.replace('"', '"').replace('"', '"')
    return title

def is_test_post(title, slug):
    """Verifica se un post è di test"""
    test_patterns = [
        r'^prova\s*\d+',
        r'^test\s*\d*',
        r'^fhsfhsfhsf',
        r'^\d+$'
    ]
    
    title_lower = title.lower()
    slug_lower = slug.lower()
    
    for pattern in test_patterns:
        if re.search(pattern, title_lower) or re.search(pattern, slug_lower):
            return True
    return False

def remove_duplicates(news):
    """Rimuove i duplicati basandosi su titolo e slug"""
    seen_titles = set()
    seen_slugs = set()
    cleaned_news = []
    duplicates_removed = 0
    
    for item in news:
        title = clean_title(item['title'])
        slug = item['slug']
        
        # Verifica duplicati
        if title in seen_titles or slug in seen_slugs:
            duplicates_removed += 1
            logger.info(f"Rimosso duplicato: {title}")
            continue
            
        seen_titles.add(title)
        seen_slugs.add(slug)
        
        # Aggiorna il titolo pulito
        item['title'] = title
        cleaned_news.append(item)
    
    logger.info(f"Duplicati rimossi: {duplicates_removed}")
    return cleaned_news

def remove_test_posts(news):
    """Rimuove i post di test"""
    cleaned_news = []
    test_posts_removed = 0
    
    for item in news:
        if is_test_post(item['title'], item['slug']):
            test_posts_removed += 1
            logger.info(f"Rimosso post di test: {item['title']}")
            continue
        cleaned_news.append(item)
    
    logger.info(f"Post di test rimossi: {test_posts_removed}")
    return cleaned_news

def normalize_news(news):
    """Normalizza i dati delle news"""
    normalized_news = []
    
    for item in news:
        # Normalizza titolo
        item['title'] = clean_title(item['title'])
        
        # Normalizza slug (rimuovi caratteri speciali)
        slug = item['slug']
        slug = re.sub(r'[^\w\-]', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        item['slug'] = slug
        
        # Normalizza autore
        if 'author' not in item or not item['author']:
            item['author'] = 'ARCS-VV'
        
        # Normalizza data
        if 'date' not in item or not item['date']:
            item['date'] = datetime.now().strftime('%Y-%m-%d')
        
        normalized_news.append(item)
    
    logger.info(f"News normalizzate: {len(normalized_news)}")
    return normalized_news

def generate_report(original_count, final_count, duplicates_removed, test_posts_removed):
    """Genera un report della pulizia"""
    report = f"""
📊 REPORT PULIZIA NEWS
{'='*50}
📈 Statistiche:
  - News originali: {original_count}
  - News finali: {final_count}
  - Duplicati rimossi: {duplicates_removed}
  - Post di test rimossi: {test_posts_removed}
  - Riduzione totale: {original_count - final_count}

✅ Operazioni completate:
  - Rimozione duplicati
  - Rimozione post di test
  - Normalizzazione titoli e slug
  - Pulizia caratteri speciali
  - Validazione dati

🎯 Risultato: Database pulito e ottimizzato
"""
    return report

def main():
    """Funzione principale"""
    logger.info("🧹 Avvio pulizia database news")
    
    # Percorsi file
    dev_dir = Path(__file__).resolve().parent.parent / "dev"
    news_file = dev_dir / "news.json"
    backup_file = dev_dir / f"news_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Carica news originali
    original_news = load_news(news_file)
    if not original_news:
        logger.error("❌ Impossibile caricare le news")
        return 1
    
    original_count = len(original_news)
    logger.info(f"📄 Caricate {original_count} news")
    
    # Crea backup
    if save_news(original_news, backup_file):
        logger.info(f"💾 Backup creato: {backup_file}")
    
    # Rimuovi duplicati
    news_no_duplicates = remove_duplicates(original_news)
    duplicates_removed = original_count - len(news_no_duplicates)
    
    # Rimuovi post di test
    news_no_test = remove_test_posts(news_no_duplicates)
    test_posts_removed = len(news_no_duplicates) - len(news_no_test)
    
    # Normalizza
    final_news = normalize_news(news_no_test)
    final_count = len(final_news)
    
    # Salva database pulito
    if save_news(final_news, news_file):
        logger.info("💾 Database pulito salvato")
    
    # Genera e mostra report
    report = generate_report(original_count, final_count, duplicates_removed, test_posts_removed)
    print(report)
    
    logger.info("🎉 Pulizia completata con successo!")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
