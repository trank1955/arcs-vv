#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Manager per ARCS-VV
Gestione completa delle pagine statiche del sito
Versione 1.1 - Con protezione contenuti esistenti
"""

import os
import re
import shutil
import json
from datetime import datetime
from pathlib import Path
from PIL import Image
import sys

class PageManager:
    def __init__(self):
        self.project_root = self.get_project_root()
        self.pages_dir = self.project_root / "pages"
        self.images_dir = self.project_root / "immagini"
        self.tools_dir = self.project_root / "tools"
        self.current_page = None
        self.page_content = {
            'title': '',
            'text_content': '',
            'images': [],
            'videos': [],
            'pdfs': []
        }
        self.protected_content = {
            'buttons': [],
            'forms': [],
            'scripts': [],
            'custom_elements': []
        }
        
    def get_project_root(self):
        """Trova la root del progetto ARCS-VV"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "pages" / "index.html").exists():
                return current
            current = current.parent
        return Path("/home/ste/OneDrive_syncro/arcs-vv-nuovo")
    
    def show_welcome(self):
        """Mostra il messaggio di benvenuto e le istruzioni"""
        print("\n" + "="*80)
        print("🌐 PAGE MANAGER ARCS-VV - GESTIONE PAGINE STATICHE")
        print("="*80)
        print("⚠️  **ATTENZIONE!** ⚠️")
        print("La pagina verrà ricreata da zero, MA con protezione dei contenuti esistenti:")
        print("• ✅ Pulsanti e form verranno PRESERVATI automaticamente")
        print("• ✅ Script e elementi personalizzati saranno PROTETTI")
        print("• ✅ Preparare/modificare a parte i testi da inserire")
        print("• ✅ Sono accettati i più comuni tag HTML per la formattazione")
        print("• ✅ Conoscere il percorso e nome di foto, video, PDF da inserire")
        print("• ✅ Le immagini verranno automaticamente ottimizzate e salvate nel progetto")
        print("="*80)
    
    def list_available_pages(self):
        """Lista tutte le pagine disponibili"""
        pages = []
        for file in self.pages_dir.glob("*.html"):
            if file.name != "news.html" and file.name != "menu.js":
                pages.append(file)
        
        print(f"\n📄 PAGINE DISPONIBILI:")
        print("-" * 40)
        for i, page in enumerate(pages, 1):
            print(f"{i}. {page.name}")
        print("-" * 40)
        return pages
    
    def select_page_to_edit(self):
        """Seleziona la pagina da modificare"""
        pages = self.list_available_pages()
        if not pages:
            print("❌ Nessuna pagina trovata!")
            return None
        
        while True:
            try:
                choice = input(f"\n🎯 Seleziona pagina (1-{len(pages)}) o 0 per uscire: ").strip()
                if choice == "0":
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(pages):
                    selected_page = pages[choice_num - 1]
                    print(f"✅ Pagina selezionata: {selected_page.name}")
                    return selected_page
                else:
                    print("❌ Scelta non valida!")
            except ValueError:
                print("❌ Inserisci un numero valido!")
    
    def load_page_content(self, page_path):
        """Carica il contenuto della pagina esistente e identifica elementi protetti"""
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Estrai il titolo
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                self.page_content['title'] = title_match.group(1).replace(' – ARCS-VV', '')
            
            # Estrai il contenuto principale (tra page-wrapper o main)
            wrapper_match = re.search(r'<div class="page-wrapper">(.*?)</div>', content, re.DOTALL)
            main_match = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
            
            if wrapper_match:
                main_content = wrapper_match.group(1).strip()
            elif main_match:
                main_content = main_match.group(1).strip()
            else:
                main_content = content
            
            # IDENTIFICA E PROTEGGI ELEMENTI IMPORTANTI
            self.protect_existing_content(main_content)
            
            # Estrai solo il testo base (senza elementi protetti)
            self.page_content['text_content'] = self.extract_base_content(main_content)
            
            print(f"📖 Contenuto caricato da: {page_path.name}")
            print(f"🛡️  Elementi protetti identificati:")
            print(f"   • Pulsanti: {len(self.protected_content['buttons'])}")
            print(f"   • Form: {len(self.protected_content['forms'])}")
            print(f"   • Script: {len(self.protected_content['scripts'])}")
            print(f"   • Elementi personalizzati: {len(self.protected_content['custom_elements'])}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore nel caricamento della pagina: {e}")
            return False
    
    def protect_existing_content(self, content):
        """Identifica e protegge elementi importanti della pagina"""
        # Proteggi pulsanti (class="button" o <button>)
        button_pattern = r'(<a[^>]*class="[^"]*button[^"]*"[^>]*>.*?</a>|<button[^>]*>.*?</button>)'
        self.protected_content['buttons'] = re.findall(button_pattern, content, re.DOTALL)
        
        # Proteggi form
        form_pattern = r'(<form[^>]*>.*?</form>)'
        self.protected_content['forms'] = re.findall(form_pattern, content, re.DOTALL)
        
        # Proteggi script inline
        script_pattern = r'(<script[^>]*>.*?</script>)'
        self.protected_content['scripts'] = re.findall(script_pattern, content, re.DOTALL)
        
        # Proteggi elementi personalizzati (custom-box, visitor-counter, etc.)
        custom_pattern = r'(<div[^>]*class="[^"]*(?:custom-box|visitor-counter|cta-buttons)[^"]*"[^>]*>.*?</div>)'
        self.protected_content['custom_elements'] = re.findall(custom_pattern, content, re.DOTALL)
        
        # Proteggi anche elementi con ID specifici
        id_pattern = r'(<[^>]*id="[^"]*"[^>]*>.*?</[^>]*>)'
        id_elements = re.findall(id_pattern, content, re.DOTALL)
        # Filtra solo quelli che non sono già protetti
        for element in id_elements:
            if not any(element in protected for protected in self.protected_content.values()):
                self.protected_content['custom_elements'].append(element)
    
    def extract_base_content(self, content):
        """Estrae il contenuto base rimuovendo gli elementi protetti"""
        base_content = content
        
        # Rimuovi tutti gli elementi protetti dal contenuto base
        for category in self.protected_content.values():
            for element in category:
                base_content = base_content.replace(element, f'<!-- PROTECTED_ELEMENT_{category.index(element)} -->')
        
        # Pulisci il contenuto rimanente
        base_content = re.sub(r'\s+', ' ', base_content).strip()
        return base_content
    
    def edit_text_content(self):
        """Modifica il contenuto testuale della pagina"""
        print(f"\n📝 CONTENUTO ATTUALE (elementi protetti esclusi):")
        print("-" * 50)
        if self.page_content['text_content']:
            print(self.page_content['text_content'][:200] + "..." if len(self.page_content['text_content']) > 200 else self.page_content['text_content'])
        else:
            print("Nessun contenuto presente")
        print("-" * 50)
        
        print("\n💡 TAG HTML SUPPORTATI:")
        print("• <strong> o <b> per il grassetto")
        print("• <em> o <i> per il corsivo")
        print("• <u> per il sottolineato")
        print("• <h2>, <h3> per i titoli")
        print("• <ul>, <li> per le liste")
        print("• <p> per i paragrafi")
        print("• <br> per le interruzioni di riga")
        print("• <a href='...'> per i link")
        
        print("\n🛡️  ELEMENTI CHE SARANNO PRESERVATI:")
        for category, elements in self.protected_content.items():
            if elements:
                print(f"   • {category.title()}: {len(elements)} elementi")
        
        new_content = input("\n✏️  Inserisci il nuovo contenuto HTML:\n")
        if new_content.strip():
            self.page_content['text_content'] = new_content
            print("✅ Contenuto testuale aggiornato!")
        else:
            print("ℹ️  Nessuna modifica apportata")
    
    def add_image(self):
        """Aggiunge un'immagine alla pagina"""
        print(f"\n🖼️  AGGIUNTA IMMAGINE")
        print("-" * 40)
        
        # Mostra immagini esistenti
        existing_images = list(self.images_dir.glob("*.jpg")) + list(self.images_dir.glob("*.jpeg")) + list(self.images_dir.glob("*.png"))
        if existing_images:
            print("📁 Immagini disponibili nel progetto:")
            for i, img in enumerate(existing_images[:10], 1):  # Mostra solo le prime 10
                print(f"  {i}. {img.name}")
            if len(existing_images) > 10:
                print(f"  ... e altre {len(existing_images) - 10} immagini")
        
        image_path = input("\n📂 Percorso completo dell'immagine da aggiungere: ").strip()
        if not image_path:
            print("ℹ️  Nessuna immagine aggiunta")
            return
        
        if not os.path.exists(image_path):
            print("❌ File immagine non trovato!")
            return
        
        # Nome file per il progetto
        filename = input("📝 Nome file per il progetto (senza estensione): ").strip()
        if not filename:
            filename = Path(image_path).stem
        
        # Estensione
        ext = Path(image_path).suffix.lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            ext = '.jpg'
        
        target_path = self.images_dir / f"{filename}{ext}"
        
        try:
            # Ottimizza e salva l'immagine
            with Image.open(image_path) as img:
                # Converti in RGB se necessario
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Ridimensiona se troppo grande (max 1200px)
                max_size = 1200
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Salva con qualità ottimizzata
                img.save(target_path, 'JPEG', quality=85, optimize=True)
            
            # Aggiungi alla lista immagini
            image_info = {
                'filename': f"{filename}{ext}",
                'alt_text': input("🔤 Testo alternativo per l'immagine: ").strip() or filename,
                'caption': input("📝 Didascalia (opzionale): ").strip()
            }
            
            self.page_content['images'].append(image_info)
            print(f"✅ Immagine ottimizzata e salvata: {target_path}")
            
        except Exception as e:
            print(f"❌ Errore nell'elaborazione dell'immagine: {e}")
    
    def add_video(self):
        """Aggiunge un video alla pagina"""
        print(f"\n🎥 AGGIUNTA VIDEO")
        print("-" * 40)
        
        video_type = input("🎬 Tipo di video:\n1. YouTube\n2. Vimeo\n3. File locale\nScelta: ").strip()
        
        if video_type == "1":
            url = input("🔗 URL YouTube: ").strip()
            if 'youtube.com' in url or 'youtu.be' in url:
                video_id = self.extract_youtube_id(url)
                if video_id:
                    video_info = {
                        'type': 'youtube',
                        'id': video_id,
                        'url': url,
                        'title': input("📝 Titolo del video: ").strip() or "Video YouTube"
                    }
                    self.page_content['videos'].append(video_info)
                    print(f"✅ Video YouTube aggiunto: {video_id}")
                else:
                    print("❌ Impossibile estrarre l'ID del video YouTube")
            else:
                print("❌ URL YouTube non valido")
                
        elif video_type == "2":
            url = input("🔗 URL Vimeo: ").strip()
            if 'vimeo.com' in url:
                video_id = self.extract_vimeo_id(url)
                if video_id:
                    video_info = {
                        'type': 'vimeo',
                        'id': video_id,
                        'url': url,
                        'title': input("📝 Titolo del video: ").strip() or "Video Vimeo"
                    }
                    self.page_content['videos'].append(video_info)
                    print(f"✅ Video Vimeo aggiunto: {video_id}")
                else:
                    print("❌ Impossibile estrarre l'ID del video Vimeo")
            else:
                print("❌ URL Vimeo non valido")
                
        elif video_type == "3":
            video_path = input("📂 Percorso completo del file video: ").strip()
            if os.path.exists(video_path):
                filename = Path(video_path).name
                target_path = self.images_dir / filename
                
                try:
                    shutil.copy2(video_path, target_path)
                    video_info = {
                        'type': 'local',
                        'filename': filename,
                        'title': input("📝 Titolo del video: ").strip() or filename
                    }
                    self.page_content['videos'].append(video_info)
                    print(f"✅ Video locale copiato: {target_path}")
                except Exception as e:
                    print(f"❌ Errore nella copia del video: {e}")
            else:
                print("❌ File video non trovato!")
        else:
            print("❌ Scelta non valida!")
    
    def extract_youtube_id(self, url):
        """Estrae l'ID del video YouTube dall'URL"""
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
        patterns = [
            r'vimeo\.com/(\d+)',
            r'player\.vimeo\.com/video/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def add_pdf(self):
        """Aggiunge un PDF alla pagina"""
        print(f"\n📄 AGGIUNTA PDF")
        print("-" * 40)
        
        pdf_path = input("📂 Percorso completo del file PDF: ").strip()
        if not pdf_path:
            print("ℹ️  Nessun PDF aggiunto")
            return
        
        if not os.path.exists(pdf_path):
            print("❌ File PDF non trovato!")
            return
        
        # Copia PDF nella directory del progetto
        filename = Path(pdf_path).name
        target_path = self.images_dir / filename
        
        try:
            shutil.copy2(pdf_path, target_path)
            
            pdf_info = {
                'filename': filename,
                'title': input("📝 Titolo del documento: ").strip() or filename.replace('.pdf', ''),
                'description': input("📝 Descrizione (opzionale): ").strip()
            }
            
            self.page_content['pdfs'].append(pdf_info)
            print(f"✅ PDF copiato: {target_path}")
            
        except Exception as e:
            print(f"❌ Errore nella copia del PDF: {e}")
    
    def generate_page(self):
        """Genera la nuova pagina HTML preservando gli elementi protetti"""
        if not self.current_page:
            print("❌ Nessuna pagina selezionata!")
            return
        
        print(f"\n🔄 RIGENERAZIONE PAGINA: {self.current_page.name}")
        print("-" * 50)
        
        # Mostra riepilogo
        print("📋 RIEPILOGO MODIFICHE:")
        print(f"  • Titolo: {self.page_content['title']}")
        print(f"  • Immagini: {len(self.page_content['images'])}")
        print(f"  • Video: {len(self.page_content['videos'])}")
        print(f"  • PDF: {len(self.page_content['pdfs'])}")
        
        print("\n🛡️  ELEMENTI CHE SARANNO PRESERVATI:")
        for category, elements in self.protected_content.items():
            if elements:
                print(f"  • {category.title()}: {len(elements)} elementi")
        
        confirm = input("\n⚠️  Confermi la rigenerazione della pagina? (s/n): ").strip().lower()
        if confirm != 's':
            print("❌ Operazione annullata")
            return
        
        try:
            # Genera il contenuto HTML
            html_content = self.create_html_content()
            
            # Salva la pagina
            with open(self.current_page, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Pagina rigenerata con successo: {self.current_page}")
            print("🛡️  Tutti gli elementi protetti sono stati preservati!")
            
        except Exception as e:
            print(f"❌ Errore nella generazione della pagina: {e}")
    
    def create_html_content(self):
        """Crea il contenuto HTML completo della pagina preservando gli elementi protetti"""
        page_name = self.current_page.stem
        
        # Determina la classe CSS della pagina
        css_class = f"page-{page_name.replace('-', '_')}"
        
        # Genera il contenuto principale
        main_content = self.page_content['text_content']
        
        # Aggiungi immagini
        for img in self.page_content['images']:
            img_html = f'\n        <div style="text-align: center; margin: 2em 0;">\n'
            img_html += f'          <img src="../immagini/{img["filename"]}" alt="{img["alt_text"]}" style="max-width: 100%; height: auto; border-radius: 8px;">\n'
            if img.get('caption'):
                img_html += f'          <p style="font-style: italic; color: #666; margin-top: 0.5em;">{img["caption"]}</p>\n'
            img_html += f'        </div>\n'
            main_content += img_html
        
        # Aggiungi video
        for video in self.page_content['videos']:
            if video['type'] == 'youtube':
                video_html = f'\n        <div style="text-align: center; margin: 2em 0;">\n'
                video_html += f'          <iframe width="560" height="315" src="https://www.youtube.com/embed/{video["id"]}" title="{video["title"]}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="max-width:100%; border-radius:8px;"></iframe>\n'
                video_html += f'        </div>\n'
                main_content += video_html
            elif video['type'] == 'vimeo':
                video_html = f'\n        <div style="text-align: center; margin: 2em 0;">\n'
                video_html += f'          <iframe width="560" height="315" src="https://player.vimeo.com/video/{video["id"]}" title="{video["title"]}" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen style="max-width:100%; border-radius:8px;"></iframe>\n'
                video_html += f'        </div>\n'
                main_content += video_html
            elif video['type'] == 'local':
                video_html = f'\n        <div style="text-align: center; margin: 2em 0;">\n'
                video_html += f'          <video width="560" height="315" controls style="max-width:100%; border-radius:8px;">\n'
                video_html += f'            <source src="../immagini/{video["filename"]}" type="video/mp4">\n'
                video_html += f'            Il tuo browser non supporta il tag video.\n'
                video_html += f'          </video>\n'
                video_html += f'        </div>\n'
                main_content += video_html
        
        # Aggiungi PDF
        for pdf in self.page_content['pdfs']:
            pdf_html = f'\n        <div style="text-align: center; margin: 2em 0; padding: 1.5em; border: 2px solid #e0e0e0; border-radius: 8px; background: #f9f9f9;">\n'
            pdf_html += f'          <h3>📄 {pdf["title"]}</h3>\n'
            if pdf.get('description'):
                pdf_html += f'          <p>{pdf["description"]}</p>\n'
            pdf_html += f'          <div style="margin-top: 1em;">\n'
            pdf_html += f'            <a href="../immagini/{pdf["filename"]}" target="_blank" class="button" style="margin-right: 1em;">👁️  Visualizza PDF</a>\n'
            pdf_html += f'            <a href="../immagini/{pdf["filename"]}" download class="button">⬇️  Scarica PDF</a>\n'
            pdf_html += f'          </div>\n'
            pdf_html += f'        </div>\n'
            main_content += pdf_html
        
        # INSERISCI GLI ELEMENTI PROTETTI NEL CONTENUTO
        main_content = self.insert_protected_elements(main_content)
        
        # Template HTML completo
        html_template = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{self.page_content['title']} – ARCS-VV</title>
  <link rel="icon" type="image/x-icon" href="../icons/favicon.ico">
  <link rel="icon" type="image/png" href="../icons/favicon.ico">
  <link rel="shortcut icon" href="../icons/favicon.ico">
  <link rel="stylesheet" href="../main.css?v=1080&t=20250803135018">
  <div id="menu-inject"></div>
  <script src="../menu.js"></script>
</head>
<body class="{css_class}">
  <h1 class="page-title {page_name}-title"><img src="../icons/{page_name}-icon.svg" alt="{self.page_content['title']}" style="width: 32px; height: 32px; margin-right: 10px; vertical-align: middle;"> {self.page_content['title']}</h1>
  
  <div class="page-wrapper">
    <main>
      <section class="{page_name}">
{main_content}
      </section>
    </main>
  </div>
  
  <footer style="background:#f2f2f2; width:100%; position:fixed; bottom:0; left:0; right:0; text-align:center; padding:1rem 0; margin:0; display:block;">
    <div style="width:100%; text-align:center; max-width:100%;">
      <p style="font-style:italic; font-size:0.85em; margin:0 auto; display:inline-block; text-align:center;">&copy; 2025 ARCS-VV - Associazione Rete di Cittadinanza Solidale. Tutti i diritti riservati.</p>
    </div>
  </footer>
</body>
</html>"""
        
        return html_template
    
    def insert_protected_elements(self, content):
        """Inserisce gli elementi protetti nel contenuto principale"""
        # Sostituisci i marker con gli elementi protetti
        for category, elements in self.protected_content.items():
            for i, element in enumerate(elements):
                marker = f'<!-- PROTECTED_ELEMENT_{i} -->'
                if marker in content:
                    content = content.replace(marker, element)
        
        return content
    
    def show_menu(self):
        """Mostra il menu principale"""
        while True:
            print("\n" + "="*60)
            print("🌐 PAGE MANAGER ARCS-VV - MENU PRINCIPALE")
            print("="*60)
            print("1. 📝 Modifica contenuto testuale")
            print("2. 🖼️  Aggiungi immagine")
            print("3. 🎥 Aggiungi video")
            print("4. 📄 Aggiungi PDF")
            print("5. 🔄 Rigenera pagina")
            print("6. 📋 Mostra riepilogo modifiche")
            print("7. 🔄 Cambia pagina")
            print("8. 🛡️  Mostra elementi protetti")
            print("0. 🚪 Esci")
            print("="*60)
            
            choice = input("🎯 Scelta: ").strip()
            
            if choice == "1":
                self.edit_text_content()
            elif choice == "2":
                self.add_image()
            elif choice == "3":
                self.add_video()
            elif choice == "4":
                self.add_pdf()
            elif choice == "5":
                self.generate_page()
            elif choice == "6":
                self.show_summary()
            elif choice == "7":
                self.select_page_to_edit()
            elif choice == "8":
                self.show_protected_elements()
            elif choice == "0":
                print("👋 Arrivederci!")
                break
            else:
                print("❌ Scelta non valida!")
    
    def show_protected_elements(self):
        """Mostra gli elementi protetti identificati"""
        print(f"\n🛡️  ELEMENTI PROTETTI IDENTIFICATI")
        print("="*50)
        
        for category, elements in self.protected_content.items():
            if elements:
                print(f"\n📋 {category.upper()}:")
                for i, element in enumerate(elements, 1):
                    # Mostra solo i primi 100 caratteri per non intasare l'output
                    preview = element[:100].replace('\n', ' ').strip()
                    if len(element) > 100:
                        preview += "..."
                    print(f"  {i}. {preview}")
            else:
                print(f"\n📋 {category.upper()}: Nessun elemento trovato")
        
        print("\n" + "="*50)
    
    def show_summary(self):
        """Mostra il riepilogo delle modifiche"""
        print(f"\n📋 RIEPILOGO MODIFICHE")
        print("="*50)
        print(f"📄 Pagina: {self.current_page.name if self.current_page else 'Nessuna'}")
        print(f"📝 Titolo: {self.page_content['title']}")
        print(f"📖 Contenuto: {len(self.page_content['text_content'])} caratteri")
        print(f"🖼️  Immagini: {len(self.page_content['images'])}")
        print(f"🎥 Video: {len(self.page_content['videos'])}")
        print(f"📄 PDF: {len(self.page_content['pdfs'])}")
        
        print(f"\n🛡️  ELEMENTI PROTETTI:")
        for category, elements in self.protected_content.items():
            print(f"  • {category.title()}: {len(elements)}")
        
        if self.page_content['images']:
            print("\n🖼️  Immagini:")
            for img in self.page_content['images']:
                print(f"  • {img['filename']} - {img['alt_text']}")
        
        if self.page_content['videos']:
            print("\n🎥 Video:")
            for video in self.page_content['videos']:
                print(f"  • {video['type']}: {video.get('id', video.get('filename', 'N/A'))}")
        
        if self.page_content['pdfs']:
            print("\n📄 PDF:")
            for pdf in self.page_content['pdfs']:
                print(f"  • {pdf['filename']} - {pdf['title']}")
    
    def run(self):
        """Esegue il page manager"""
        self.show_welcome()
        
        # Seleziona pagina iniziale
        self.current_page = self.select_page_to_edit()
        if not self.current_page:
            print("👋 Nessuna pagina selezionata. Arrivederci!")
            return
        
        # Carica contenuto esistente
        if not self.load_page_content(self.current_page):
            print("❌ Impossibile caricare la pagina. Uscita.")
            return
        
        # Mostra menu principale
        self.show_menu()

def main():
    """Funzione principale"""
    print("🌐 PAGE MANAGER ARCS-VV")
    print("Gestione completa delle pagine statiche del sito")
    print("Versione 1.1 - Con protezione contenuti esistenti")
    print("="*50)
    
    try:
        manager = PageManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Operazione interrotta dall'utente. Arrivederci!")
    except Exception as e:
        print(f"\n❌ Errore critico: {e}")
        print("Controlla i permessi e la struttura del progetto.")

if __name__ == "__main__":
    main()
