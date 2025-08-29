#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script per Page Manager ARCS-VV
Verifica le funzionalità base senza modificare file
"""

import sys
from pathlib import Path

# Aggiungi la directory tools al path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

try:
    from page_manager import PageManager
    
    def test_page_manager():
        """Test delle funzionalità base del Page Manager"""
        print("🧪 TEST PAGE MANAGER ARCS-VV")
        print("="*50)
        
        # Crea istanza
        manager = PageManager()
        print(f"✅ Project root: {manager.project_root}")
        print(f"✅ Pages directory: {manager.pages_dir}")
        print(f"✅ Images directory: {manager.images_dir}")
        
        # Test lista pagine
        print("\n📄 Test lista pagine disponibili:")
        pages = manager.list_available_pages()
        if pages:
            print(f"✅ Trovate {len(pages)} pagine:")
            for i, page in enumerate(pages[:5], 1):  # Mostra solo le prime 5
                print(f"  {i}. {page.name}")
            if len(pages) > 5:
                print(f"  ... e altre {len(pages) - 5} pagine")
        else:
            print("❌ Nessuna pagina trovata")
        
        # Test estrazione ID video
        print("\n🎥 Test estrazione ID video:")
        
        # YouTube
        youtube_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ"
        ]
        
        for url in youtube_urls:
            video_id = manager.extract_youtube_id(url)
            print(f"  YouTube: {url} → ID: {video_id}")
        
        # Vimeo
        vimeo_urls = [
            "https://vimeo.com/123456789",
            "https://player.vimeo.com/video/123456789"
        ]
        
        for url in vimeo_urls:
            video_id = manager.extract_vimeo_id(url)
            print(f"  Vimeo: {url} → ID: {video_id}")
        
        print("\n✅ Test completato con successo!")
        print("\n🚀 Per utilizzare il Page Manager completo:")
        print("   python3 page_manager.py")
        
    if __name__ == "__main__":
        test_page_manager()
        
except ImportError as e:
    print(f"❌ Errore di importazione: {e}")
    print("Verifica che page_manager.py sia nella stessa directory")
except Exception as e:
    print(f"❌ Errore durante il test: {e}")
    print("Controlla la configurazione del progetto")
