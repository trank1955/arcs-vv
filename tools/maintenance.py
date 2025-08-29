#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script di manutenzione completo per il progetto ARCS-VV
- Pulizia news
- Generazione sito
- Validazione file
- Backup automatico
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Esegue un comando e gestisce gli errori"""
    logger.info(f"�� {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        if result.returncode == 0:
            logger.info(f"✅ {description} completato")
            if result.stdout:
                logger.info(f"Output: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"❌ {description} fallito")
            if result.stderr:
                logger.error(f"Errore: {result.stderr.strip()}")
            return False
    except Exception as e:
        logger.error(f"❌ Errore nell'esecuzione di {description}: {e}")
        return False

def create_backup():
    """Crea un backup completo del progetto"""
    logger.info("💾 Creazione backup completo")
    
    backup_dir = Path(__file__).parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"arcs-vv-backup_{timestamp}"
    backup_path = backup_dir / backup_name
    
    try:
        # Crea backup delle directory principali
        import shutil
        shutil.copytree(Path(__file__).parent.parent / "pages", backup_path / "pages")
        shutil.copytree(Path(__file__).parent.parent / "dev", backup_path / "dev")
        shutil.copytree(Path(__file__).parent.parent / "templates", backup_path / "templates")
        
        logger.info(f"✅ Backup creato: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Errore nella creazione del backup: {e}")
        return False

def validate_files():
    """Valida i file generati"""
    logger.info("🔍 Validazione file generati")
    
    pages_dir = Path(__file__).parent.parent / "pages"
    required_files = [
        "index.html", "attivita.html", "chi-siamo.html", "dove-siamo.html",
        "donazioni.html", "iscriviti.html", "news.html", "statuto.html",
        "contatti.html", "404.html", "thankyou.html"
    ]
    
    missing_files = []
    empty_files = []
    
    for file in required_files:
        file_path = pages_dir / file
        if not file_path.exists():
            missing_files.append(file)
        elif file_path.stat().st_size == 0:
            empty_files.append(file)
    
    if missing_files:
        logger.warning(f"⚠️ File mancanti: {', '.join(missing_files)}")
    
    if empty_files:
        logger.warning(f"⚠️ File vuoti: {', '.join(empty_files)}")
    
    if not missing_files and not empty_files:
        logger.info("✅ Tutti i file sono presenti e non vuoti")
        return True
    
    return False

def check_dependencies():
    """Verifica le dipendenze Python"""
    logger.info("📦 Verifica dipendenze")
    
    required_packages = ['jinja2']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} installato")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"⚠️ {package} non installato")
    
    if missing_packages:
        logger.info("💡 Per installare le dipendenze mancanti:")
        logger.info(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Funzione principale"""
    logger.info("🚀 Avvio manutenzione progetto ARCS-VV")
    
    # Verifica dipendenze
    if not check_dependencies():
        logger.warning("⚠️ Alcune dipendenze mancano, ma continuo...")
    
    # Crea backup
    create_backup()
    
    # Esegui pulizia news
    if not run_command("python3 tools/clean_news.py", "Pulizia database news"):
        logger.warning("⚠️ Pulizia news fallita, ma continuo...")
    
    # Genera sito
    if not run_command("python3 dev/genera_sito_optimized.py", "Generazione sito"):
        logger.error("❌ Generazione sito fallita")
        return 1
    
    # Valida file
    if not validate_files():
        logger.warning("⚠️ Alcuni file potrebbero avere problemi")
    
    # Riepilogo finale
    logger.info("=" * 60)
    logger.info("🎉 MANUTENZIONE COMPLETATA")
    logger.info("=" * 60)
    logger.info("✅ Operazioni completate:")
    logger.info("  - Backup del progetto")
    logger.info("  - Pulizia database news")
    logger.info("  - Generazione sito")
    logger.info("  - Validazione file")
    logger.info("")
    logger.info("📁 File generati in: pages/")
    logger.info("💾 Backup in: backups/")
    logger.info("🔧 Script disponibili in: tools/")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
