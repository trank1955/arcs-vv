#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per correggere i link delle news
- Sostituisce ../blog/posts/ con ../news/
- Aggiorna tutti i link rotti
"""

import os
import re
from pathlib import Path

def fix_news_links():
    """Corregge i link delle news nella pagina news.html"""
    
    news_file = Path("pages/news.html")
    if not news_file.exists():
        print("❌ File news.html non trovato")
        return False
    
    # Leggi il contenuto
    with open(news_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Conta i link da correggere
    old_links = re.findall(r'href="../blog/posts/[^"]*"', content)
    print(f"🔍 Trovati {len(old_links)} link da correggere")
    
    # Sostituisci i percorsi
    new_content = content.replace('../blog/posts/', '../news/')
    
    # Verifica se ci sono stati cambiamenti
    if new_content == content:
        print("✅ Nessun link da correggere")
        return True
    
    # Crea backup
    backup_file = news_file.with_suffix('.html.backup')
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup creato: {backup_file}")
    
    # Scrivi il file corretto
    with open(news_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Link delle news corretti!")
    
    # Mostra alcuni esempi di link corretti
    new_links = re.findall(r'href="../news/[^"]*"', new_content)
    print(f"🔗 Link corretti: {len(new_links)}")
    for link in new_links[:5]:  # Mostra i primi 5
        print(f"  {link}")
    
    return True

if __name__ == "__main__":
    print("🔧 Correzione link delle news...")
    if fix_news_links():
        print("🎉 Operazione completata con successo!")
    else:
        print("❌ Operazione fallita!")
