#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Mobile Live - ARCS-VV
Testa la responsività mobile in tempo reale
"""

import os
import time
import webbrowser
from pathlib import Path
import subprocess

class MobileLiveTester:
    def __init__(self):
        self.project_root = self.get_project_root()
        self.server_port = 8003
        
    def get_project_root(self):
        """Trova la root del progetto ARCS-VV"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "pages" / "index.html").exists():
                return current
            current = current.parent
        return Path("/home/ste/OneDrive_syncro/arcs-vv-nuovo")
    
    def start_server(self):
        """Avvia il server HTTP per test mobile"""
        print("🚀 Avvio server HTTP per test mobile...")
        
        try:
            # Importa e usa il server manager
            from server_manager import http_server
            
            with http_server(port=self.server_port, project_root=self.project_root) as server:
                print(f"📱 Server avviato su porta: {server.port}")
                print("🌐 Apri il browser e vai su:")
                print(f"   http://localhost:{server.port}/pages/")
                print("\n📱 PER TESTARE SU MOBILE:")
                print("1. Trova l'IP del tuo computer:")
                print("   hostname -I")
                print("2. Sul mobile, vai su:")
                print(f"   http://[TUO_IP]:{server.port}/pages/")
                print("\n💡 SUGGERIMENTI TEST:")
                print("• Usa F12 nel browser per simulare mobile")
                print("• Testa su dispositivi reali")
                print("• Verifica orientamento landscape/portrait")
                print("• Controlla navigazione touch")
                print("• Verifica leggibilità testo")
                
                print("\n⏳ Server rimarrà attivo fino a quando premi Ctrl+C...")
                
                # Mantieni il server attivo
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n⏹️  Interruzione richiesta dall'utente")
                    
        except ImportError:
            print("⚠️  Server manager non disponibile, usando metodo legacy...")
            self.start_server_legacy()
        except Exception as e:
            print(f"❌ Errore nell'avvio server: {e}")
    
    def start_server_legacy(self):
        """Metodo legacy per avviare il server (fallback)"""
        print("🔄 Avvio server con metodo legacy...")
        
        # Cambia directory al progetto
        os.chdir(self.project_root)
        
        try:
            print(f"📱 Server avviato su: http://localhost:{self.server_port}")
            print("🌐 Apri il browser e vai su:")
            print(f"   http://localhost:{self.server_port}/pages/")
            
            # Avvia server
            subprocess.run([
                "python3", "-m", "http.server", str(self.server_port)
            ], cwd=self.project_root)
            
        except KeyboardInterrupt:
            print("\n⏹️  Server fermato dall'utente")
        except Exception as e:
            print(f"❌ Errore nell'avvio server: {e}")
    
    def show_mobile_test_guide(self):
        """Mostra guida per test mobile"""
        print("\n" + "="*60)
        print("📱 GUIDA COMPLETA TEST MOBILE ARCS-VV")
        print("="*60)
        
        print("\n🎯 COSA TESTARE:")
        print("1. 📱 Responsività layout")
        print("2. 🍔 Menu mobile")
        print("3. 👆 Elementi touch-friendly")
        print("4. 🖼️  Immagini responsive")
        print("5. 📱 Tipografia mobile")
        print("6. 🔄 Orientamento schermo")
        print("7. ⚡ Performance mobile")
        
        print("\n🔧 STRUMENTI DI TEST:")
        print("• Browser DevTools (F12)")
        print("• Simulatore mobile integrato")
        print("• Dispositivi reali")
        print("• Strumenti online (PageSpeed, GTmetrix)")
        
        print("\n📱 BREAKPOINT DA VERIFICARE:")
        print("• 320px - Smartphone piccoli")
        print("• 480px - Smartphone standard")
        print("• 768px - Tablet/Phablet")
        print("• 900px - Tablet grandi")
        print("• 1024px - Desktop piccoli")
        
        print("\n✅ CHECKLIST COMPLETAMENTO:")
        print("□ Meta viewport presente")
        print("□ CSS responsive implementato")
        print("□ Menu mobile funzionante")
        print("□ Immagini scalabili")
        print("□ Pulsanti touch-friendly")
        print("□ Tipografia leggibile")
        print("□ Performance ottimizzata")
        print("□ Test su dispositivi reali")
        
        print("\n🚀 PROSSIMI PASSI:")
        print("1. Avvia il server con: python3 test_mobile_live.py")
        print("2. Testa su browser desktop (F12)")
        print("3. Testa su dispositivi mobili reali")
        print("4. Verifica tutti i breakpoint")
        print("5. Ottimizza eventuali problemi")
        
        print("\n" + "="*60)
    
    def check_mobile_ready(self):
        """Verifica se il sito è pronto per test mobile"""
        print("\n🔍 VERIFICA PREPARAZIONE MOBILE")
        print("-" * 40)
        
        # Verifica file essenziali
        essential_files = [
            "main.css",
            "mobile-optimizations.css",
            "menu.js",
            "pages/index.html"
        ]
        
        all_ready = True
        for file_path in essential_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} - MANCANTE")
                all_ready = False
        
        if all_ready:
            print("\n🎉 Il sito è pronto per test mobile!")
        else:
            print("\n⚠️  Risolvi i file mancanti prima di testare")
        
        return all_ready

def main():
    """Funzione principale"""
    print("📱 MOBILE LIVE TESTER ARCS-VV")
    print("="*50)
    
    tester = MobileLiveTester()
    
    # Mostra guida
    tester.show_mobile_test_guide()
    
    # Verifica preparazione
    if not tester.check_mobile_ready():
        print("\n❌ Il sito non è pronto per test mobile")
        return
    
    # Chiedi se avviare il server
    print("\n🚀 Vuoi avviare il server per test mobile? (s/n): ", end="")
    try:
        response = input().strip().lower()
        if response in ['s', 'si', 'y', 'yes']:
            tester.start_server()
        else:
            print("👋 Test mobile completato. Avvia il server quando vuoi!")
    except KeyboardInterrupt:
        print("\n👋 Test mobile interrotto")

if __name__ == "__main__":
    main()
