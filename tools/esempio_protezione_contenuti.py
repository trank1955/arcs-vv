#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esempio Sistema di Protezione Contenuti - Page Manager ARCS-VV
Dimostra come vengono identificati e protetti elementi importanti
"""

import sys
from pathlib import Path

# Aggiungi la directory tools al path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

try:
    from page_manager import PageManager
    
    def esempio_protezione_contenuti():
        """Esempio del sistema di protezione dei contenuti"""
        print("🛡️  ESEMPIO SISTEMA PROTEZIONE CONTENUTI")
        print("="*60)
        print("Questo script mostra come il Page Manager identifica")
        print("e protegge automaticamente elementi importanti delle pagine.")
        print("="*60)
        
        # Crea istanza del manager
        manager = PageManager()
        
        # Seleziona la pagina index.html (home)
        pages = manager.list_available_pages()
        home_page = None
        
        for page in pages:
            if page.name == "index.html":
                home_page = page
                break
        
        if not home_page:
            print("❌ Pagina 'index.html' non trovata!")
            return
        
        print(f"✅ Pagina selezionata: {home_page.name}")
        
        # Carica il contenuto e identifica elementi protetti
        if not manager.load_page_content(home_page):
            print("❌ Impossibile caricare il contenuto della pagina")
            return
        
        print(f"\n📖 Contenuto caricato: {len(manager.page_content['text_content'])} caratteri")
        
        # Mostra elementi protetti identificati
        print("\n🛡️  ELEMENTI PROTETTI IDENTIFICATI:")
        print("="*50)
        
        for category, elements in manager.protected_content.items():
            if elements:
                print(f"\n📋 {category.upper()}:")
                for i, element in enumerate(elements, 1):
                    # Mostra solo i primi 80 caratteri per chiarezza
                    preview = element[:80].replace('\n', ' ').strip()
                    if len(element) > 80:
                        preview += "..."
                    print(f"  {i}. {preview}")
            else:
                print(f"\n📋 {category.upper()}: Nessun elemento trovato")
        
        print("\n" + "="*50)
        
        # Dimostra come funziona la protezione
        print("\n🔍 COME FUNZIONA LA PROTEZIONE:")
        print("-" * 40)
        print("1. Il sistema identifica automaticamente:")
        print("   • Pulsanti con class='button'")
        print("   • Form completi")
        print("   • Script inline")
        print("   • Elementi personalizzati (custom-box, visitor-counter)")
        print("   • Elementi con ID specifici")
        
        print("\n2. Durante la rigenerazione:")
        print("   • Gli elementi protetti vengono temporaneamente sostituiti")
        print("   • Il nuovo contenuto viene inserito")
        print("   • Gli elementi protetti vengono ripristinati")
        print("   • La funzionalità della pagina rimane intatta")
        
        print("\n3. Vantaggi:")
        print("   • ✅ Pulsanti e form non scompaiono mai")
        print("   • ✅ Script continuano a funzionare")
        print("   • ✅ Elementi personalizzati sono preservati")
        print("   • ✅ Sicurezza totale per funzionalità importanti")
        
        print("\n" + "="*50)
        
        # Esempio pratico di modifica
        print("\n📝 ESEMPIO PRATICO DI MODIFICA:")
        print("-" * 40)
        print("Se modifichi il contenuto testuale della home page:")
        print("• Il testo verrà aggiornato")
        print("• I pulsanti 'Diventa volontario' e 'Fai una donazione' rimarranno")
        print("• Il contatore visite rimarrà intatto")
        print("• La custom-box con le informazioni ARCS-VV rimarrà")
        print("• Tutti gli script continueranno a funzionare")
        
        print("\n" + "="*50)
        
        print("\n🎯 PROSSIMI PASSI:")
        print("1. Per testare la protezione, usa:")
        print("   python3 page_manager.py")
        print("2. Seleziona la pagina da modificare")
        print("3. Usa l'opzione 8 per vedere gli elementi protetti")
        print("4. Modifica il contenuto con sicurezza!")
        
        print("\n" + "="*50)
        
    if __name__ == "__main__":
        esempio_protezione_contenuti()
        
except ImportError as e:
    print(f"❌ Errore di importazione: {e}")
    print("Verifica che page_manager.py sia nella stessa directory")
except Exception as e:
    print(f"❌ Errore durante l'esempio: {e}")
    print("Controlla la configurazione del progetto")
