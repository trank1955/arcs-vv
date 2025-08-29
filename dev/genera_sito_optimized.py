#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore ottimizzato per il sito ARCS-VV
- Genera tutte le pagine HTML dai template Jinja2
- Gestione errori robusta
- Logging dettagliato
- Validazione dei file generati
"""

import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import logging

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dati menu centralizzato
MENU = [
    {"title": "Home", "url": "index.html"},
    {"title": "Attività", "url": "attivita.html"},
    {"title": "Chi siamo", "url": "chi-siamo.html"},
    {"title": "Dove siamo", "url": "dove-siamo.html"},
    {"title": "Donazioni", "url": "donazioni.html"},
    {"title": "Contatti", "url": "contatti.html"},
]

# Dati di tutte le pagine principali
PAGES = [
    {"filename": "index.html", "template": "index.html"},
    {"filename": "attivita.html", "template": "attivita.html"},
    {"filename": "chi-siamo.html", "template": "chi-siamo.html"},
    {"filename": "dove-siamo.html", "template": "dove-siamo.html"},
    {"filename": "donazioni.html", "template": "donazioni.html"},
    {"filename": "iscriviti.html", "template": "iscriviti.html"},
    {"filename": "news.html", "template": "news.html"},
    {"filename": "statuto.html", "template": "statuto.html"},
    {"filename": "contatti.html", "template": "contatti.html"},
    {"filename": "404.html", "template": "404.html"},
    {"filename": "thankyou.html", "template": "thankyou.html"},
]

def setup_environment():
    """Configura l'ambiente Jinja2 e verifica i percorsi"""
    try:
        # Ottieni il percorso assoluto della directory dev
        dev_dir = Path(__file__).resolve().parent
        project_root = dev_dir.parent
        templates_dir = project_root / "templates"
        output_dir = project_root / "pages"
        
        # Verifica che la directory templates esista
        if not templates_dir.exists():
            logger.error(f"Directory templates non trovata: {templates_dir}")
            return None, None, None
            
        # Crea la directory output se non esiste
        output_dir.mkdir(exist_ok=True)
        
        # Setup Jinja2
        env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        logger.info(f"Ambiente configurato:")
        logger.info(f"  Templates: {templates_dir}")
        logger.info(f"  Output: {output_dir}")
        
        return env, output_dir, project_root
        
    except Exception as e:
        logger.error(f"Errore nella configurazione dell'ambiente: {e}")
        return None, None, None

def validate_template(env, template_name):
    """Verifica che un template esista e sia valido"""
    try:
        template = env.get_template(template_name)
        return template is not None
    except TemplateNotFound:
        logger.warning(f"Template non trovato: {template_name}")
        return False
    except Exception as e:
        logger.error(f"Errore nel template {template_name}: {e}")
        return False

def generate_page(env, output_dir, page_info, project_root):
    """Genera una singola pagina"""
    try:
        template_name = page_info["template"]
        filename = page_info["filename"]
        
        # Verifica template
        if not validate_template(env, template_name):
            return False
            
        # Genera la pagina
        template = env.get_template(template_name)
        output = template.render()
        
        # Percorso output
        out_path = output_dir / filename
        
        # Scrivi il file
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
            
        # Verifica che il file sia stato creato
        if out_path.exists() and out_path.stat().st_size > 0:
            logger.info(f"✅ Pagina generata: {filename} ({out_path.stat().st_size} bytes)")
            return True
        else:
            logger.error(f"❌ Errore nella generazione di {filename}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Errore nella generazione di {page_info['filename']}: {e}")
        return False

def main():
    """Funzione principale"""
    logger.info("🚀 Avvio generazione sito ARCS-VV")
    
    # Setup ambiente
    env, output_dir, project_root = setup_environment()
    if not all([env, output_dir, project_root]):
        logger.error("❌ Impossibile configurare l'ambiente")
        return 1
    
    # Statistiche
    total_pages = len(PAGES)
    successful_pages = 0
    failed_pages = []
    
    logger.info(f"�� Generazione di {total_pages} pagine...")
    
    # Genera tutte le pagine
    for page in PAGES:
        if generate_page(env, output_dir, page, project_root):
            successful_pages += 1
        else:
            failed_pages.append(page["filename"])
    
    # Riepilogo
    logger.info("=" * 50)
    logger.info("📊 RIEPILOGO GENERAZIONE")
    logger.info("=" * 50)
    logger.info(f"Pagine totali: {total_pages}")
    logger.info(f"✅ Successo: {successful_pages}")
    logger.info(f"❌ Fallite: {len(failed_pages)}")
    
    if failed_pages:
        logger.warning("Pagine fallite:")
        for page in failed_pages:
            logger.warning(f"  - {page}")
    
    if successful_pages == total_pages:
        logger.info("🎉 Generazione completata con successo!")
        return 0
    else:
        logger.warning("⚠️ Generazione completata con alcuni errori")
        return 1

if __name__ == "__main__":
    sys.exit(main())
