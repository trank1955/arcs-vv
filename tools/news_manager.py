#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Manager Interattivo per ARCS-VV
Script completo per gestire news, foto, filmati, PDF e molto altro
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Importa le funzioni del blog manager
try:
    from blog_manager import (
        create_news_article, 
        generate_news_json_from_html,
        update_news_page,
        slugify
    )
except ImportError:
    print("❌ Errore: Impossibile importare blog_manager")
    print("Assicurati di essere nella directory tools/")
    sys.exit(1)

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsManager:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.news_dir = self.root / "pages" / "news"
        self.images_dir = self.root / "immagini"
        self.news_json = self.news_dir / "news.json"
        
        # Crea directory se non esistono
        self.news_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
    
    def show_menu(self):
        """Mostra il menu principale"""
        print("\n" + "="*60)
        print("🎯 NEWS MANAGER ARCS-VV - GESTIONE COMPLETA")
        print("="*60)
        print("1. 📰 Crea nuova news")
        print("2. 🖼️  Carica immagine per news")
        print("3. 🎥 Carica filmato/YouTube")
        print("4. 📄 Carica documento PDF")
        print("5. ✏️  Modifica news esistente")
        print("6. 🗑️  Cancella news")
        print("7. 📋 Lista tutte le news")
        print("8. 🔄 Aggiorna pagina principale")
        print("9. 🧹 Pulisci database news")
        print("10. 📊 Statistiche news")
        print("0. 🚪 Esci")
        print("="*60)
    
    def create_news(self):
        """Crea una nuova news interattivamente"""
        print("\n📰 CREAZIONE NUOVA NEWS")
        print("-" * 40)
        
        # Input titolo
        while True:
            title = input("📝 Titolo della news: ").strip()
            if title:
                break
            print("❌ Il titolo non può essere vuoto!")
        
        # Input riassunto
        while True:
            summary = input("📄 Riassunto della news: ").strip()
            if summary:
                break
            print("❌ Il riassunto non può essere vuoto!")
        
        # Input immagine
        print("\n🖼️  Gestione immagine:")
        print("1. Usa immagine di default")
        print("2. Carica nuova immagine")
        print("3. Seleziona immagine esistente")
        
        image_choice = input("Scelta (1-3): ").strip()
        image = None
        
        if image_choice == "1":
            image = "blog-cover_photo-300.jpeg"
            print("✅ Usando immagine di default")
        elif image_choice == "2":
            image = self.upload_image()
        elif image_choice == "3":
            image = self.select_existing_image()
            if image:
                print(f"✅ Immagine selezionata: {image}")
            else:
                print("⚠️  Nessuna immagine selezionata, proseguendo senza immagine...")
        
        # Input autore
        author = input("👤 Autore (default: ARCS-VV): ").strip() or "ARCS-VV"
        
        # Conferma creazione
        print(f"\n📋 Riepilogo news:")
        print(f"   Titolo: {title}")
        print(f"   Riassunto: {summary}")
        print(f"   Immagine: {image or 'Nessuna'}")
        print(f"   Autore: {author}")
        
        confirm = input("\n✅ Confermi la creazione? (s/n): ").strip().lower()
        if confirm in ['s', 'si', 'y', 'yes']:
            success = create_news_article(title, summary, image, author)
            if success:
                print("🎉 News creata con successo!")
                # Aggiorna la pagina principale
                self.update_main_page()
            else:
                print("❌ Errore nella creazione della news")
        else:
            print("❌ Creazione annullata")
    
    def upload_image(self):
        """Carica una nuova immagine"""
        print("\n🖼️  CARICAMENTO NUOVA IMMAGINE")
        print("-" * 40)
        
        # Mostra immagini esistenti
        existing_images = list(self.images_dir.glob("*.jpg")) + list(self.images_dir.glob("*.jpeg")) + list(self.images_dir.glob("*.png"))
        if existing_images:
            print("📁 Immagini esistenti nella directory:")
            for i, img in enumerate(existing_images, 1):
                print(f"   {i:2d}. {img.name}")
            print("💡 Suggerimento: Se vuoi usare un'immagine esistente, torna al menu principale e scegli '3. Seleziona immagine esistente'")
        
        # Input percorso immagine
        while True:
            image_path = input("\n📁 Percorso immagine da caricare: ").strip()
            if not image_path:
                return None
            
            source_path = Path(image_path)
            if not source_path.exists():
                print(f"❌ File non trovato: {image_path}")
                continue
            
            if not source_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                print("❌ Formato immagine non supportato. Usa: .jpg, .jpeg, .png, .gif")
                continue
            
            break
        
        # Genera nome file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_name = f"news_{timestamp}{source_path.suffix}"
        dest_path = self.images_dir / new_name
        
        try:
            shutil.copy2(source_path, dest_path)
            print(f"✅ Immagine caricata: {new_name}")
            return new_name
        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            return None
    
    def select_existing_image(self):
        """Seleziona un'immagine esistente"""
        print("\n🖼️  SELEZIONE IMMAGINE ESISTENTE")
        print("-" * 40)
        
        images = list(self.images_dir.glob("*.jpg")) + list(self.images_dir.glob("*.jpeg")) + list(self.images_dir.glob("*.png"))
        
        if not images:
            print("❌ Nessuna immagine trovata nella directory immagini/")
            return None
        
        print("📁 Immagini disponibili:")
        for i, img in enumerate(images, 1):
            print(f"   {i:2d}. {img.name}")
        
        while True:
            try:
                choice = int(input(f"\n🎯 Scegli immagine (1-{len(images)}): ").strip())
                if 1 <= choice <= len(images):
                    selected = images[choice - 1]
                    print(f"✅ Immagine selezionata: {selected.name}")
                    return selected.name
                else:
                    print("❌ Scelta non valida!")
            except ValueError:
                print("❌ Inserisci un numero valido!")
    
    def upload_video(self):
        """Carica un filmato o link YouTube/Vimeo"""
        print("\n🎥 CARICAMENTO FILMATO/YOUTUBE/VIMEO")
        print("-" * 40)
        
        print("1. Link YouTube")
        print("2. Link Vimeo")
        print("3. File video locale")
        
        choice = input("Scelta (1-3): ").strip()
        
        if choice == "1":
            youtube_url = input("🔗 URL YouTube: ").strip()
            if youtube_url:
                # Estrai ID video
                video_id = self.extract_youtube_id(youtube_url)
                if video_id:
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                    print(f"✅ Thumbnail YouTube generato: {thumbnail_url}")
                    print(f"🎬 Il video sarà visualizzato embedded nella pagina")
                    return f"youtube_{video_id}"
                else:
                    print("❌ URL YouTube non valido")
                    return None
        elif choice == "2":
            vimeo_url = input("🔗 URL Vimeo: ").strip()
            if vimeo_url:
                # Estrai ID video Vimeo
                video_id = self.extract_vimeo_id(vimeo_url)
                if video_id:
                    thumbnail_url = f"https://vumbnail.com/{video_id}.jpg"
                    print(f"✅ Thumbnail Vimeo generato: {thumbnail_url}")
                    print(f"🎬 Il video sarà visualizzato embedded nella pagina")
                    return f"vimeo_{video_id}"
                else:
                    print("❌ URL Vimeo non valido")
                    return None
        elif choice == "3":
            return self.upload_video_file()
        
        return None
    
    def extract_youtube_id(self, url):
        """Estrae l'ID del video YouTube dall'URL"""
        import re
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def extract_vimeo_id(self, url):
        """Estrae l'ID del video Vimeo dall'URL"""
        import re
        patterns = [
            r'vimeo\.com/(\d+)',
            r'vimeo\.com/channels/\w+/(\d+)',
            r'vimeo\.com/groups/\w+/videos/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def upload_video_file(self):
        """Carica un file video locale"""
        print("\n📁 CARICAMENTO FILE VIDEO")
        print("-" * 40)
        
        while True:
            video_path = input("📁 Percorso file video: ").strip()
            if not video_path:
                return None
            
            source_path = Path(video_path)
            if not source_path.exists():
                print(f"❌ File non trovato: {video_path}")
                continue
            
            if not source_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
                print("❌ Formato video non supportato. Usa: .mp4, .avi, .mov, .mkv")
                continue
            
            break
        
        # Genera nome file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_name = f"video_{timestamp}{source_path.suffix}"
        dest_path = self.images_dir / new_name
        
        try:
            shutil.copy2(source_path, dest_path)
            print(f"✅ Video caricato: {new_name}")
            return new_name
        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            return None
    
    def upload_pdf(self):
        """Carica un documento PDF"""
        print("\n📄 CARICAMENTO DOCUMENTO PDF")
        print("-" * 40)
        
        while True:
            pdf_path = input("📁 Percorso file PDF: ").strip()
            if not pdf_path:
                return None
            
            source_path = Path(pdf_path)
            if not source_path.exists():
                print(f"❌ File non trovato: {pdf_path}")
                continue
            
            if not source_path.suffix.lower() == '.pdf':
                print("❌ File deve essere in formato PDF")
                continue
            
            break
        
        # Genera nome file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_name = f"documento_{timestamp}.pdf"
        dest_path = self.images_dir / new_name
        
        try:
            shutil.copy2(source_path, dest_path)
            print(f"✅ PDF caricato: {new_name}")
            return new_name
        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            return None
    
    def edit_news(self):
        """Modifica una news esistente"""
        print("\n✏️  MODIFICA NEWS ESISTENTE")
        print("-" * 40)
        
        # Lista news esistenti
        if not self.news_json.exists():
            print("❌ Nessuna news trovata")
            return
        
        with open(self.news_json, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        if not news_data:
            print("❌ Nessuna news nel database")
            return
        
        print("📋 News disponibili:")
        for i, news in enumerate(news_data, 1):
            print(f"   {i}. {news['title']} ({news['date']})")
        
        try:
            choice = int(input(f"\n🎯 Scegli news da modificare (1-{len(news_data)}): ").strip())
            if not (1 <= choice <= len(news_data)):
                print("❌ Scelta non valida!")
                return
            
            selected_news = news_data[choice - 1]
            print(f"\n✏️  Modifica: {selected_news['title']}")
            
            # Modifica titolo
            new_title = input(f"📝 Nuovo titolo (attuale: {selected_news['title']}): ").strip()
            if new_title:
                selected_news['title'] = new_title
                selected_news['slug'] = slugify(new_title)
            
            # Modifica riassunto
            new_summary = input(f"📄 Nuovo riassunto (attuale: {selected_news['summary']}): ").strip()
            if new_summary:
                selected_news['summary'] = new_summary
            
            # Salva modifiche
            with open(self.news_json, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, indent=2, ensure_ascii=False)
            
            print("✅ News modificata con successo!")
            
        except ValueError:
            print("❌ Inserisci un numero valido!")
    
    def delete_news(self):
        """Cancella una news"""
        print("\n🗑️  CANCELLAZIONE NEWS")
        print("-" * 40)
        
        if not self.news_json.exists():
            print("❌ Nessuna news trovata")
            return
        
        with open(self.news_json, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        if not news_data:
            print("❌ Nessuna news nel database")
            return
        
        print("📋 News disponibili:")
        for i, news in enumerate(news_data, 1):
            print(f"   {i}. {news['title']} ({news['date']})")
        
        try:
            choice = int(input(f"\n🎯 Scegli news da cancellare (1-{len(news_data)}): ").strip())
            if not (1 <= choice <= len(news_data)):
                print("❌ Scelta non valida!")
                return
            
            selected_news = news_data[choice - 1]
            print(f"\n🗑️  Cancellazione: {selected_news['title']}")
            
            confirm = input("⚠️  Sei sicuro di voler cancellare questa news? (s/n): ").strip().lower()
            if confirm in ['s', 'si', 'y', 'yes']:
                # Rimuovi dal JSON
                news_data.pop(choice - 1)
                with open(self.news_json, 'w', encoding='utf-8') as f:
                    json.dump(news_data, f, indent=2, ensure_ascii=False)
                
                # Rimuovi file HTML se esiste
                html_file = self.news_dir / f"{selected_news['slug']}.html"
                if html_file.exists():
                    html_file.unlink()
                    print("✅ File HTML rimosso")
                
                print("✅ News cancellata con successo!")
            else:
                print("❌ Cancellazione annullata")
                
        except ValueError:
            print("❌ Inserisci un numero valido!")
    
    def list_news(self):
        """Mostra tutte le news"""
        print("\n📋 LISTA COMPLETA NEWS")
        print("-" * 40)
        
        if not self.news_json.exists():
            print("❌ Nessuna news trovata")
            return
        
        with open(self.news_json, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        if not news_data:
            print("❌ Nessuna news nel database")
            return
        
        print(f"📊 Totale news: {len(news_data)}")
        print()
        
        for i, news in enumerate(news_data, 1):
            print(f"{i:2d}. 📰 {news['title']}")
            print(f"     📅 {news['date']} | 👤 {news['author']}")
            print(f"     🔗 {news['slug']}.html")
            if news.get('image'):
                print(f"     🖼️  {news['image']}")
            print(f"     📄 {news['summary'][:80]}{'...' if len(news['summary']) > 80 else ''}")
            print()
    
    def update_main_page(self):
        """Aggiorna la pagina principale delle news"""
        print("\n🔄 AGGIORNAMENTO PAGINA PRINCIPALE")
        print("-" * 40)
        
        try:
            success = update_news_page()
            if success:
                print("✅ Pagina principale aggiornata con successo!")
            else:
                print("❌ Errore nell'aggiornamento della pagina")
        except Exception as e:
            print(f"❌ Errore: {e}")
    
    def clean_database(self):
        """Pulisce il database delle news"""
        print("\n🧹 PULIZIA DATABASE NEWS")
        print("-" * 40)
        
        try:
            # Rigenera il database dai file HTML
            count = generate_news_json_from_html()
            print(f"✅ Database rigenerato con {count} articoli")
            
            # Aggiorna la pagina principale
            self.update_main_page()
            
        except Exception as e:
            print(f"❌ Errore nella pulizia: {e}")
    
    def show_statistics(self):
        """Mostra statistiche delle news"""
        print("\n📊 STATISTICHE NEWS")
        print("-" * 40)
        
        if not self.news_json.exists():
            print("❌ Nessuna news trovata")
            return
        
        with open(self.news_json, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        if not news_data:
            print("❌ Nessuna news nel database")
            return
        
        # Statistiche generali
        total_news = len(news_data)
        print(f"📊 Totale news: {total_news}")
        
        # News per anno
        years = {}
        for news in news_data:
            year = news['date'][:4]
            years[year] = years.get(year, 0) + 1
        
        print(f"\n📅 News per anno:")
        for year in sorted(years.keys()):
            print(f"   {year}: {years[year]} news")
        
        # News con immagini
        news_with_images = sum(1 for news in news_data if news.get('image'))
        print(f"\n🖼️  News con immagini: {news_with_images}/{total_news}")
        
        # Autori
        authors = {}
        for news in news_data:
            author = news.get('author', 'Sconosciuto')
            authors[author] = authors.get(author, 0) + 1
        
        print(f"\n👤 Autori:")
        for author, count in authors.items():
            print(f"   {author}: {count} news")
    
    def run(self):
        """Esegue il menu principale"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\n🎯 Scegli opzione (0-10): ").strip()
                
                if choice == "0":
                    print("\n👋 Arrivederci! Grazie per aver usato News Manager ARCS-VV")
                    break
                elif choice == "1":
                    self.create_news()
                elif choice == "2":
                    image = self.upload_image()
                    if image:
                        print(f"✅ Immagine caricata: {image}")
                elif choice == "3":
                    video = self.upload_video()
                    if video:
                        print(f"✅ Video caricato: {video}")
                elif choice == "4":
                    pdf = self.upload_pdf()
                    if pdf:
                        print(f"✅ PDF caricato: {pdf}")
                elif choice == "5":
                    self.edit_news()
                elif choice == "6":
                    self.delete_news()
                elif choice == "7":
                    self.list_news()
                elif choice == "8":
                    self.update_main_page()
                elif choice == "9":
                    self.clean_database()
                elif choice == "10":
                    self.show_statistics()
                else:
                    print("❌ Opzione non valida!")
                
                input("\n⏸️  Premi INVIO per continuare...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interruzione richiesta dall'utente")
                break
            except Exception as e:
                print(f"\n❌ Errore inaspettato: {e}")
                input("\n⏸️  Premi INVIO per continuare...")

def main():
    """Funzione principale"""
    print("🚀 Avvio News Manager ARCS-VV...")
    
    try:
        manager = NewsManager()
        manager.run()
    except Exception as e:
        print(f"❌ Errore fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
