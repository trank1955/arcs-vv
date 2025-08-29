#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esempio di Utilizzo del Page Manager ARCS-VV
Dimostra come modificare una pagina esistente
"""

import sys
from pathlib import Path

# Aggiungi la directory tools al path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

try:
    from page_manager import PageManager
    
    def esempio_modifica_pagina():
        """Esempio di modifica della pagina 'chi-siamo.html'"""
        print("📚 ESEMPIO PAGE MANAGER ARCS-VV")
        print("="*60)
        print("Questo script mostra come modificare la pagina 'chi-siamo.html'")
        print("con nuovo contenuto, immagini e video.")
        print("="*60)
        
        # Crea istanza del manager
        manager = PageManager()
        
        # Seleziona la pagina chi-siamo.html
        pages = manager.list_available_pages()
        chi_siamo_page = None
        
        for page in pages:
            if page.name == "chi-siamo.html":
                chi_siamo_page = page
                break
        
        if not chi_siamo_page:
            print("❌ Pagina 'chi-siamo.html' non trovata!")
            return
        
        print(f"✅ Pagina selezionata: {chi_siamo_page.name}")
        
        # Carica il contenuto esistente
        if not manager.load_page_content(chi_siamo_page):
            print("❌ Impossibile caricare il contenuto della pagina")
            return
        
        print(f"📖 Contenuto caricato: {len(manager.page_content['text_content'])} caratteri")
        
        # Esempio di nuovo contenuto HTML
        nuovo_contenuto = """<h2>La nostra missione</h2>
<p>ARCS-VV è un'associazione di volontariato che promuove <strong>l'integrazione sociale</strong> e la <em>solidarietà</em> nel territorio di Vittorio Veneto.</p>

<h3>Chi siamo</h3>
<p>La nostra associazione è composta da:</p>
<ul>
  <li>Volontari locali impegnati nel sociale</li>
  <li>Operatori sociali qualificati</li>
  <li>Migranti che vogliono contribuire alla comunità</li>
</ul>

<h3>I nostri valori</h3>
<p>Crediamo fermamente in:</p>
<ul>
  <li><strong>Accoglienza</strong> e inclusione</li>
  <li><em>Solidarietà</em> e mutuo aiuto</li>
  <li>Integrazione culturale e linguistica</li>
  <li>Supporto concreto alle persone in difficoltà</li>
</ul>

<h3>Come puoi aiutarci</h3>
<p>Hai diverse possibilità per sostenerci:</p>
<ul>
  <li>Diventare volontario attivo</li>
  <li>Fare una donazione</li>
  <li>Partecipare ai nostri eventi</li>
  <li>Diffondere la nostra missione</li>
</ul>"""
        
        # Aggiorna il contenuto
        manager.page_content['text_content'] = nuovo_contenuto
        print("✅ Contenuto testuale aggiornato")
        
        # Esempio di aggiunta immagine
        print("\n🖼️  Aggiunta immagine di esempio...")
        manager.page_content['images'].append({
            'filename': 'volontari.jpg',
            'alt_text': 'Volontari ARCS-VV al lavoro',
            'caption': 'I nostri volontari durante un laboratorio di italiano'
        })
        
        # Esempio di aggiunta video YouTube
        print("🎥 Aggiunta video YouTube di esempio...")
        manager.page_content['videos'].append({
            'type': 'youtube',
            'id': 'pW99e2YZcmI',
            'url': 'https://www.youtube.com/watch?v=pW99e2YZcmI',
            'title': 'Presentazione ARCS-VV'
        })
        
        # Esempio di aggiunta PDF
        print("📄 Aggiunta PDF di esempio...")
        manager.page_content['pdfs'].append({
            'filename': 'statuto-arcs-vv.pdf',
            'title': 'Statuto ARCS-VV',
            'description': 'Documento ufficiale dell\'associazione'
        })
        
        # Mostra riepilogo
        print("\n📋 RIEPILOGO MODIFICHE:")
        print("="*40)
        manager.show_summary()
        
        print("\n" + "="*60)
        print("🎯 COSA SUCCEDE ORA:")
        print("1. Il contenuto è stato preparato in memoria")
        print("2. Per applicare le modifiche, esegui:")
        print("   python3 page_manager.py")
        print("3. Seleziona la pagina 'chi-siamo.html'")
        print("4. Scegli opzione 5 per rigenerare la pagina")
        print("="*60)
        
        print("\n⚠️  IMPORTANTE:")
        print("- Fai sempre backup prima di modificare")
        print("- Le modifiche vengono applicate solo dopo la rigenerazione")
        print("- Testa sempre la pagina dopo le modifiche")
        
    if __name__ == "__main__":
        esempio_modifica_pagina()
        
except ImportError as e:
    print(f"❌ Errore di importazione: {e}")
    print("Verifica che page_manager.py sia nella stessa directory")
except Exception as e:
    print(f"❌ Errore durante l'esempio: {e}")
    print("Controlla la configurazione del progetto")
