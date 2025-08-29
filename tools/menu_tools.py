#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Tools ARCS-VV - Centro di Controllo
Menu di lancio per tutti gli strumenti implementati
"""

import os
import sys
import subprocess
from pathlib import Path
import time

class ToolsLauncher:
    def __init__(self):
        self.project_root = self.get_project_root()
        self.tools_dir = self.project_root / "tools"
        self.current_tool = None
        
    def get_project_root(self):
        """Trova la root del progetto ARCS-VV"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "pages" / "index.html").exists():
                return current
            current = current.parent
        return Path("/home/ste/OneDrive_syncro/arcs-vv-nuovo")
    
    def clear_screen(self):
        """Pulisce lo schermo del terminale"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_header(self):
        """Mostra l'header del menu"""
        print("=" * 70)
        print("🛠️   MENU TOOLS ARCS-VV - CENTRO DI CONTROLLO")
        print("=" * 70)
        print(f"📍 Progetto: {self.project_root}")
        print(f"🔧 Tools disponibili: {len(self.get_available_tools())}")
        print(f"⏰ {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    def get_available_tools(self):
        """Restituisce la lista dei tool disponibili"""
        tools = {
            "1": {
                "name": "📰 Blog Manager",
                "file": "blog_manager.py",
                "description": "Gestione completa delle news (crea, modifica, elimina)",
                "category": "News Management"
            },
            "2": {
                "name": "📋 News Manager",
                "file": "news_manager.py",
                "description": "Interfaccia interattiva per gestire le news",
                "category": "News Management"
            },
            "3": {
                "name": "🔄 Rigenera Pagina News",
                "file": "regenerate_news_page.py",
                "description": "Ricrea completamente la pagina news.html",
                "category": "News Management"
            },
            "4": {
                "name": "📄 Page Manager",
                "file": "page_manager.py",
                "description": "Gestione e modifica delle pagine statiche",
                "category": "Page Management"
            },
            "5": {
                "name": "👥 Visitor Counter",
                "file": "visitor_counter.py",
                "description": "Gestione contatore visite e statistiche",
                "category": "Analytics"
            },
            "6": {
                "name": "📱 Test Responsività Mobile",
                "file": "test_responsive_mobile.py",
                "description": "Test automatico responsività mobile",
                "category": "Testing"
            },
            "7": {
                "name": "📱 Test Mobile Live",
                "file": "test_mobile_live.py",
                "description": "Test mobile in tempo reale con server",
                "category": "Testing"
            },
            "8": {
                "name": "🧪 Test Page Manager",
                "file": "test_page_manager.py",
                "description": "Test funzionalità base del page manager",
                "category": "Testing"
            },
            "9": {
                "name": "📖 Esempio Page Manager",
                "file": "esempio_page_manager.py",
                "description": "Esempio di utilizzo del page manager",
                "category": "Examples"
            },
            "10": {
                "name": "🛡️ Esempio Protezione Contenuti",
                "file": "esempio_protezione_contenuti.py",
                "description": "Dimostra sistema protezione contenuti",
                "category": "Examples"
            },
            "11": {
                "name": "🚀 Avvia Server HTTP",
                "file": "start_server.py",
                "description": "Avvia server HTTP per test locali",
                "category": "Development"
            },
            "12": {
                "name": "📚 Mostra Documentazione",
                "file": "show_docs.py",
                "description": "Mostra tutti i file README disponibili",
                "category": "Documentation"
            },
            "13": {
                "name": "🔍 Analisi Progetto",
                "file": "project_analyzer.py",
                "description": "Analisi completa struttura progetto",
                "category": "Development"
            },
            "14": {
                "name": "🧹 Pulizia Backup",
                "file": "cleanup_backups.py",
                "description": "Pulisce backup vecchi e file temporanei",
                "category": "Maintenance"
            },
            "15": {
                "name": "📊 Report Completo",
                "file": "generate_report.py",
                "description": "Genera report completo stato progetto",
                "category": "Reporting"
            },
            "16": {
                "name": "🏗️ Genera Sito Base",
                "file": "genera_sito_base.py",
                "description": "Generatore base: crea pagine da template Jinja2 (semplice)",
                "category": "Site Generation"
            },
            "17": {
                "name": "🚀 Genera Sito PRO",
                "file": "genera_sito_pro.py",
                "description": "Generatore avanzato: logging, validazione, gestione errori robusta",
                "category": "Site Generation"
            },
            "18": {
                "name": "🌐 Server Manager",
                "file": "server_manager.py",
                "description": "Gestione automatica server HTTP con context manager",
                "category": "Development"
            }
        }
        return tools
    
    def show_main_menu(self):
        """Mostra il menu principale"""
        self.clear_screen()
        self.show_header()
        
        tools = self.get_available_tools()
        
        # Raggruppa per categoria
        categories = {}
        for tool_id, tool in tools.items():
            cat = tool["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((tool_id, tool))
        
        # Mostra menu organizzato per categoria
        for category, category_tools in categories.items():
            print(f"\n📂 {category}:")
            print("-" * 50)
            for tool_id, tool in category_tools:
                print(f"  {tool_id:>2}. {tool['name']}")
                print(f"      {tool['description']}")
        
        print("\n" + "=" * 70)
        print("💡 COMANDI SPECIALI:")
        print("   📚 docs    - Mostra e visualizza documentazione")
        print("   🔍 info    - Informazioni progetto")
        print("   🚀 server  - Avvia server HTTP")
        print("   🧪 test    - Esegui tutti i test")
        print("   🆘 help    - Aiuto completo")
        print("   ❌ exit    - Esci dal menu")
        print("=" * 70)
    
    def run_tool(self, tool_id):
        """Esegue il tool selezionato"""
        tools = self.get_available_tools()
        
        if tool_id not in tools:
            print(f"❌ Tool {tool_id} non trovato!")
            return False
        
        tool = tools[tool_id]
        
        # Tutti i tool sono ora nella directory tools
        tool_file = self.tools_dir / tool["file"]
        
        if not tool_file.exists():
            print(f"❌ File {tool['file']} non trovato!")
            print(f"   Percorso cercato: {tool_file}")
            return False
        
        print(f"\n🚀 Avvio {tool['name']}...")
        print(f"📁 File: {tool_file}")
        print(f"📝 Descrizione: {tool['description']}")
        print("-" * 50)
        
        try:
            # Cambia directory al progetto e esegui il tool
            os.chdir(self.project_root)
            result = subprocess.run([
                sys.executable, str(tool_file)
            ], cwd=self.project_root)
            
            if result.returncode == 0:
                print(f"\n✅ {tool['name']} completato con successo!")
            else:
                print(f"\n⚠️  {tool['name']} completato con warning (exit code: {result.returncode})")
                
        except KeyboardInterrupt:
            print(f"\n⏹️  {tool['name']} interrotto dall'utente")
        except Exception as e:
            print(f"\n❌ Errore nell'esecuzione di {tool['name']}: {e}")
        
        return True
    
    def show_documentation(self):
        """Mostra la documentazione disponibile"""
        self.clear_screen()
        print("📚 DOCUMENTAZIONE DISPONIBILE ARCS-VV")
        print("=" * 50)
        
        docs_dir = self.project_root / "tools"
        readme_files = list(docs_dir.glob("README_*.md"))
        
        if not readme_files:
            print("❌ Nessun file README trovato!")
            return
        
        # Mostra elenco numerato
        print("📖 FILE DI DOCUMENTAZIONE DISPONIBILI:")
        print("-" * 50)
        
        for i, doc_file in enumerate(readme_files, 1):
            print(f"{i:>2}. 📖 {doc_file.name}")
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        print(f"     {first_line}")
                    else:
                        print(f"     {first_line}")
            except:
                print("     (Errore nella lettura)")
        
        print("\n" + "=" * 50)
        print("💡 COSA VUOI FARE?")
        print("   • Inserisci un numero per visualizzare il README")
        print("   • Premi INVIO per tornare al menu principale")
        print("   • Scrivi 'all' per visualizzare tutti i README")
        print("=" * 50)
        
        while True:
            choice = input("\n🎯 Scegli un README da visualizzare (o INVIO per uscire): ").strip()
            
            if not choice:
                print("👋 Ritorno al menu principale...")
                break
            
            if choice.lower() == 'all':
                self.show_all_documentation(readme_files)
                break
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(readme_files):
                    self.show_specific_documentation(readme_files[choice_num - 1])
                    break
                else:
                    print(f"❌ Numero non valido. Scegli tra 1 e {len(readme_files)}")
            except ValueError:
                print("❌ Inserisci un numero valido o premi INVIO per uscire")
    
    def show_specific_documentation(self, doc_file):
        """Mostra un README specifico"""
        self.clear_screen()
        print(f"📖 LETTURA: {doc_file.name}")
        print("=" * 70)
        
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Mostra il contenuto con paginazione
            self.display_content_with_pagination(content, doc_file.name)
            
        except Exception as e:
            print(f"❌ Errore nella lettura del file: {e}")
        
        input("\n⏸️  Premi INVIO per tornare alla lista documentazione...")
    
    def show_all_documentation(self, readme_files):
        """Mostra tutti i README in sequenza"""
        self.clear_screen()
        print("📚 TUTTI I README ARCS-VV")
        print("=" * 70)
        
        for i, doc_file in enumerate(readme_files, 1):
            print(f"\n{'='*70}")
            print(f"📖 {i}/{len(readme_files)}: {doc_file.name}")
            print(f"{'='*70}")
            
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Mostra il contenuto con paginazione
                self.display_content_with_pagination(content, doc_file.name)
                
                if i < len(readme_files):
                    print(f"\n⏭️  Prossimo README: {readme_files[i].name}")
                    input("⏸️  Premi INVIO per continuare...")
                    
            except Exception as e:
                print(f"❌ Errore nella lettura di {doc_file.name}: {e}")
        
        print(f"\n🎉 Visualizzazione completata! {len(readme_files)} README visualizzati.")
        input("⏸️  Premi INVIO per tornare al menu principale...")
    
    def display_content_with_pagination(self, content, filename):
        """Mostra il contenuto con paginazione intelligente"""
        lines = content.split('\n')
        total_lines = len(lines)
        
        if total_lines <= 50:
            # File piccolo, mostra tutto
            print(content)
            return
        
        # File grande, usa paginazione
        page_size = 40
        current_page = 0
        total_pages = (total_lines + page_size - 1) // page_size
        
        while current_page < total_pages:
            start_line = current_page * page_size
            end_line = min(start_line + page_size, total_lines)
            
            self.clear_screen()
            print(f"📖 {filename} - Pagina {current_page + 1}/{total_pages}")
            print("=" * 70)
            
            # Mostra le righe della pagina corrente
            for i in range(start_line, end_line):
                print(lines[i])
            
            print("\n" + "=" * 70)
            print(f"📄 Pagina {current_page + 1}/{total_pages} ({start_line + 1}-{end_line} di {total_lines} righe)")
            
            if current_page < total_pages - 1:
                print("💡 Comandi: 'n' (avanti), 'p' (indietro), 'q' (esci), INVIO (avanti)")
                choice = input("🎯 Scegli: ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice == 'p' and current_page > 0:
                    current_page -= 1
                else:
                    current_page += 1
            else:
                print("🏁 Fine del documento")
                input("⏸️  Premi INVIO per continuare...")
                break
    
    def show_project_info(self):
        """Mostra informazioni sul progetto"""
        self.clear_screen()
        print("🔍 INFORMAZIONI PROGETTO ARCS-VV")
        print("=" * 50)
        
        print(f"\n📁 Directory progetto: {self.project_root}")
        print(f"🔧 Tools disponibili: {len(self.get_available_tools())}")
        
        # Conta file HTML
        html_files = list(self.project_root.rglob("*.html"))
        print(f"📄 Pagine HTML: {len(html_files)}")
        
        # Conta file CSS
        css_files = list(self.project_root.rglob("*.css"))
        print(f"🎨 File CSS: {len(css_files)}")
        
        # Conta file JavaScript
        js_files = list(self.project_root.rglob("*.js"))
        print(f"⚡ File JavaScript: {len(js_files)}")
        
        # Conta immagini
        img_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']
        img_files = []
        for ext in img_extensions:
            img_files.extend(self.project_root.rglob(f"*{ext}"))
        print(f"🖼️  Immagini: {len(img_files)}")
        
        print(f"\n📊 Dimensione progetto: {self.get_dir_size(self.project_root):.1f} MB")
        
        print("\n🎯 FUNZIONALITÀ PRINCIPALI:")
        print("   • Sito web responsive completo")
        print("   • Sistema di gestione news")
        print("   • Gestione pagine statiche")
        print("   • Contatore visite")
        print("   • Menu mobile ottimizzato")
        print("   • Sistema di protezione contenuti")
    
    def get_dir_size(self, path):
        """Calcola la dimensione di una directory in MB"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except:
            pass
        return total_size / (1024 * 1024)  # Converti in MB
    
    def start_http_server(self):
        """Avvia il server HTTP"""
        self.clear_screen()
        print("🚀 AVVIO SERVER HTTP ARCS-VV")
        print("=" * 50)
        
        try:
            # Importa e usa il server manager
            from server_manager import http_server
            
            print("📱 Il server sarà disponibile su:")
            print("   • Desktop: http://localhost:[PORTA]/pages/")
            print("   • Mobile: http://[TUO_IP]:[PORTA]/pages/")
            
            print("\n💡 Per trovare il tuo IP:")
            print("   hostname -I")
            
            print("\n⏹️  Premi Ctrl+C per fermare il server")
            print("-" * 50)
            
            with http_server(port=8003, project_root=self.project_root) as server:
                print(f"✅ Server avviato su porta {server.port}")
                print("🌐 Desktop: http://localhost:{server.port}/pages/")
                print("📱 Mobile: http://[TUO_IP]:{server.port}/pages/")
                
                print("\n⏳ Server attivo, premi Ctrl+C per fermarlo...")
                
                # Mantieni il server attivo
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n⏹️  Interruzione richiesta dall'utente")
                    
        except ImportError:
            print("⚠️  Server manager non disponibile, usando metodo legacy...")
            self.start_http_server_legacy()
        except Exception as e:
            print(f"\n❌ Errore nell'avvio server: {e}")
    
    def start_http_server_legacy(self):
        """Metodo legacy per avviare il server (fallback)"""
        print("🔄 Avvio server con metodo legacy...")
        
        print("📱 Il server sarà disponibile su:")
        print("   • Desktop: http://localhost:8003/pages/")
        print("   • Mobile: http://[TUO_IP]:8003/pages/")
        
        print("\n💡 Per trovare il tuo IP:")
        print("   hostname -I")
        
        print("\n⏹️  Premi Ctrl+C per fermare il server")
        print("-" * 50)
        
        try:
            os.chdir(self.project_root)
            subprocess.run([
                "python3", "-m", "http.server", "8003"
            ], cwd=self.project_root)
        except KeyboardInterrupt:
            print("\n⏹️  Server fermato dall'utente")
        except Exception as e:
            print(f"\n❌ Errore nell'avvio server: {e}")
    
    def run_all_tests(self):
        """Esegue tutti i test disponibili"""
        self.clear_screen()
        print("🧪 ESECUZIONE TUTTI I TEST ARCS-VV")
        print("=" * 50)
        
        # Solo test che si eseguono e terminano automaticamente
        test_tools = [
            ("test_responsive_mobile.py", "Test Responsività Mobile"),
            ("test_page_manager.py", "Test Page Manager"),
            ("test_menu_tools.py", "Test Menu Tools")
        ]
        
        results = []
        for test_file, test_name in test_tools:
            print(f"\n🔍 Esecuzione: {test_name}")
            print("-" * 30)
            
            test_path = self.tools_dir / test_file
            if test_path.exists():
                try:
                    os.chdir(self.project_root)
                    result = subprocess.run([
                        sys.executable, str(test_path)
                    ], cwd=self.project_root, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"✅ {test_name}: SUCCESSO")
                        results.append(("✅", test_name))
                    else:
                        print(f"❌ {test_name}: FALLITO (exit code: {result.returncode})")
                        results.append(("❌", test_name))
                        
                except Exception as e:
                    print(f"❌ {test_name}: ERRORE - {e}")
                    results.append(("❌", test_name))
            else:
                print(f"⚠️  {test_name}: File non trovato")
                results.append(("⚠️", test_name))
        
        # Riepilogo finale
        print("\n" + "=" * 50)
        print("📊 RIEPILOGO TEST:")
        for status, test_name in results:
            print(f"   {status} {test_name}")
        
        success_count = sum(1 for status, _ in results if status == "✅")
        total_count = len(results)
        
        print(f"\n🎯 RISULTATO: {success_count}/{total_count} test superati")
        
        if success_count == total_count:
            print("🎉 Tutti i test automatici sono stati superati!")
        else:
            print("⚠️  Alcuni test hanno fallito. Controlla i log sopra.")
        
        print("\n" + "=" * 50)
        print("💡 TEST INTERATTIVI DISPONIBILI:")
        print("   • Test Mobile Live (Tool 7): Richiede Ctrl+C per terminare")
        print("   • Server HTTP (Tool 18): Gestione automatica server")
        print("   • Altri tool specifici: Usa i numeri dal menu principale")
        
        print("\n🎯 RACCOMANDAZIONI:")
        print("   • I test automatici sono completati")
        print("   • I test interattivi sono disponibili nel menu principale")
        print("   • Usa 'test' per eseguire solo i test automatici")
        print("   • Usa i numeri 6, 7, 8 per test specifici")
        
        return results
    
    def show_help(self):
        """Mostra l'aiuto completo"""
        self.clear_screen()
        print("🆘 AIUTO COMPLETO MENU TOOLS ARCS-VV")
        print("=" * 60)
        
        print("\n🎯 COSA FA QUESTO MENU:")
        print("   Questo è il centro di controllo per tutti gli strumenti")
        print("   del progetto ARCS-VV. Da qui puoi lanciare qualsiasi tool")
        print("   senza dover ricordare i nomi dei file.")
        
        print("\n🔧 COME USARLO:")
        print("   1. Scegli un numero dal menu principale")
        print("   2. Il tool verrà eseguito automaticamente")
        print("   3. Al termine, premi INVIO per tornare al menu")
        print("   4. Usa i comandi speciali per funzioni aggiuntive")
        
        print("\n💡 COMANDI SPECIALI:")
        print("   • docs    - Mostra e visualizza README disponibili")
        print("   • info    - Informazioni dettagliate sul progetto")
        print("   • server  - Avvia server HTTP per test")
        print("   • test    - Esegue tutti i test automatici (non interattivi)")
        print("   • help    - Questo aiuto")
        print("   • exit    - Esci dal menu")
        
        print("\n📱 TOOL PRINCIPALI:")
        print("   • Blog Manager: Gestione completa delle news")
        print("   • Page Manager: Modifica pagine statiche")
        print("   • Visitor Counter: Gestione contatore visite")
        print("   • Test Mobile: Verifica responsività")
        
        print("\n⚠️  NOTE IMPORTANTI:")
        print("   • Assicurati di essere nella directory del progetto")
        print("   • Alcuni tool potrebbero richiedere input interattivo")
        print("   • Usa Ctrl+C per interrompere tool in esecuzione")
        print("   • Controlla sempre i messaggi di output")
        
        print("\n🔗 DOCUMENTAZIONE:")
        print("   • README_NEWS.md: Sistema news")
        print("   • README_PAGE_MANAGER.md: Gestione pagine")
        print("   • README_VISITOR_COUNTER.md: Contatore visite")
        print("   • STRUMENTI_DISPONIBILI.md: Panoramica completa")
    
    def main_loop(self):
        """Loop principale del menu"""
        while True:
            try:
                self.show_main_menu()
                
                choice = input("\n🎯 Scegli un'opzione (o comando speciale): ").strip().lower()
                
                if choice in ['exit', 'quit', 'q', '0']:
                    print("\n👋 Arrivederci! Grazie per aver usato il Menu Tools ARCS-VV!")
                    break
                
                elif choice in ['docs', 'documentazione']:
                    self.show_documentation()
                    input("\n⏸️  Premi INVIO per continuare...")
                
                elif choice in ['info', 'informazioni']:
                    self.show_project_info()
                    input("\n⏸️  Premi INVIO per continuare...")
                
                elif choice in ['server', 'http']:
                    self.start_http_server()
                
                elif choice in ['test', 'tests']:
                    self.run_all_tests()
                    input("\n⏸️  Premi INVIO per continuare...")
                
                elif choice in ['help', 'aiuto', 'h']:
                    self.show_help()
                    input("\n⏸️  Premi INVIO per continuare...")
                
                elif choice.isdigit() and choice in self.get_available_tools():
                    self.run_tool(choice)
                    input("\n⏸️  Premi INVIO per tornare al menu...")
                
                else:
                    print(f"\n❌ Opzione '{choice}' non valida!")
                    print("💡 Usa 'help' per vedere tutti i comandi disponibili")
                    input("\n⏸️  Premi INVIO per continuare...")
                    
            except KeyboardInterrupt:
                print("\n\n⏹️  Interruzione richiesta dall'utente")
                break
            except Exception as e:
                print(f"\n❌ Errore nel menu: {e}")
                input("\n⏸️  Premi INVIO per continuare...")

def main():
    """Funzione principale"""
    print("🛠️  MENU TOOLS ARCS-VV - INIZIALIZZAZIONE...")
    
    try:
        launcher = ToolsLauncher()
        launcher.main_loop()
    except Exception as e:
        print(f"\n❌ Errore fatale: {e}")
        print("💡 Verifica di essere nella directory corretta del progetto")
        sys.exit(1)

if __name__ == "__main__":
    main()
