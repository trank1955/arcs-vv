#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Responsività Mobile - ARCS-VV
Verifica che il sito funzioni correttamente su dispositivi mobili
"""

import os
import re
from pathlib import Path

class MobileResponsivenessTester:
    def __init__(self):
        self.project_root = self.get_project_root()
        self.pages_dir = self.project_root / "pages"
        self.css_file = self.project_root / "main.css"
        
    def get_project_root(self):
        """Trova la root del progetto ARCS-VV"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "pages" / "index.html").exists():
                return current
            current = current.parent
        return Path("/home/ste/OneDrive_syncro/arcs-vv-nuovo")
    
    def test_viewport_meta(self):
        """Testa la presenza del meta viewport nelle pagine HTML"""
        print("🔍 TEST META VIEWPORT")
        print("-" * 40)
        
        issues = []
        for html_file in self.pages_dir.glob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Cerca meta viewport
                viewport_pattern = r'<meta[^>]*viewport[^>]*>'
                viewport_match = re.search(viewport_pattern, content, re.IGNORECASE)
                
                if viewport_match:
                    print(f"✅ {html_file.name}: Meta viewport presente")
                else:
                    print(f"❌ {html_file.name}: Meta viewport MANCANTE")
                    issues.append(f"{html_file.name}: Meta viewport mancante")
                    
            except Exception as e:
                print(f"❌ {html_file.name}: Errore nella lettura - {e}")
                issues.append(f"{html_file.name}: Errore lettura")
        
        return issues
    
    def test_css_media_queries(self):
        """Testa la presenza di media queries per mobile"""
        print("\n📱 TEST MEDIA QUERIES MOBILE")
        print("-" * 40)
        
        if not self.css_file.exists():
            print("❌ File CSS principale non trovato!")
            return []
        
        try:
            with open(self.css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Cerca media queries per mobile
            mobile_queries = re.findall(r'@media\s*\([^)]*max-width[^)]*\)\s*\{', css_content)
            tablet_queries = re.findall(r'@media\s*\([^)]*min-width[^)]*\)\s*\{', css_content)
            
            print(f"📱 Media queries mobile (max-width): {len(mobile_queries)}")
            print(f"📱 Media queries tablet (min-width): {len(tablet_queries)}")
            
            # Mostra le breakpoint principali
            breakpoints = re.findall(r'@media\s*\([^)]*max-width:\s*(\d+)px[^)]*\)', css_content)
            if breakpoints:
                print(f"📱 Breakpoint principali: {', '.join(breakpoints)}px")
            
            # Verifica breakpoint critici
            critical_breakpoints = ['480', '768', '900', '1024']
            missing_breakpoints = []
            
            for bp in critical_breakpoints:
                if not any(bp in query for query in mobile_queries):
                    missing_breakpoints.append(bp)
            
            if missing_breakpoints:
                print(f"⚠️  Breakpoint mancanti: {', '.join(missing_breakpoints)}px")
            
            return []
            
        except Exception as e:
            print(f"❌ Errore nella lettura CSS: {e}")
            return [f"CSS: Errore lettura - {e}"]
    
    def test_mobile_menu(self):
        """Testa la presenza del menu mobile"""
        print("\n🍔 TEST MENU MOBILE")
        print("-" * 40)
        
        issues = []
        
        # Verifica CSS menu mobile
        if self.css_file.exists():
            try:
                with open(self.css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                mobile_menu_selectors = [
                    '.mobile-menu',
                    '.mobile-menu-trigger',
                    '.mobile-menu-overlay'
                ]
                
                for selector in mobile_menu_selectors:
                    if selector in css_content:
                        print(f"✅ CSS: {selector} presente")
                    else:
                        print(f"❌ CSS: {selector} MANCANTE")
                        issues.append(f"CSS: {selector} mancante")
                        
            except Exception as e:
                print(f"❌ Errore nella lettura CSS: {e}")
        
        # Verifica JavaScript menu mobile
        menu_js = self.project_root / "menu.js"
        if menu_js.exists():
            try:
                with open(menu_js, 'r', encoding='utf-8') as f:
                    js_content = f.read()
                
                if 'mobile' in js_content.lower():
                    print("✅ JavaScript: Menu mobile presente")
                else:
                    print("⚠️  JavaScript: Menu mobile non identificato")
                    
            except Exception as e:
                print(f"❌ Errore nella lettura menu.js: {e}")
        else:
            print("❌ File menu.js non trovato")
            issues.append("menu.js: File non trovato")
        
        return issues
    
    def test_responsive_images(self):
        """Testa la responsività delle immagini"""
        print("\n🖼️  TEST IMMAGINI RESPONSIVE")
        print("-" * 40)
        
        issues = []
        
        # Verifica CSS per immagini responsive
        if self.css_file.exists():
            try:
                with open(self.css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                responsive_patterns = [
                    'max-width: 100%',
                    'width: 100%',
                    'height: auto',
                    'object-fit'
                ]
                
                for pattern in responsive_patterns:
                    if pattern in css_content:
                        print(f"✅ CSS: {pattern} presente")
                    else:
                        print(f"⚠️  CSS: {pattern} non identificato")
                        
            except Exception as e:
                print(f"❌ Errore nella lettura CSS: {e}")
        
        return issues
    
    def test_touch_friendly_elements(self):
        """Testa elementi touch-friendly per mobile"""
        print("\n👆 TEST ELEMENTI TOUCH-FRIENDLY")
        print("-" * 40)
        
        issues = []
        
        # Verifica dimensioni minime per elementi touch
        if self.css_file.exists():
            try:
                with open(self.css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                touch_patterns = [
                    'min-height: 44px',
                    'min-width: 44px',
                    'padding: 0.8em',
                    'font-size: 1em'
                ]
                
                for pattern in touch_patterns:
                    if pattern in css_content:
                        print(f"✅ CSS: {pattern} presente")
                    else:
                        print(f"⚠️  CSS: {pattern} non identificato")
                        
            except Exception as e:
                print(f"❌ Errore nella lettura CSS: {e}")
        
        return issues
    
    def test_page_specific_responsiveness(self):
        """Testa la responsività specifica delle pagine"""
        print("\n📄 TEST RESPONSIVITÀ PAGINE SPECIFICHE")
        print("-" * 40)
        
        issues = []
        
        # Testa la home page
        home_page = self.pages_dir / "index.html"
        if home_page.exists():
            try:
                with open(home_page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verifica stili inline responsive
                responsive_styles = [
                    'max-width: 95%',
                    'flex-wrap: wrap',
                    'margin: auto'
                ]
                
                for style in responsive_styles:
                    if style in content:
                        print(f"✅ Home: {style} presente")
                    else:
                        print(f"⚠️  Home: {style} non identificato")
                        
            except Exception as e:
                print(f"❌ Errore nella lettura home: {e}")
        
        return issues
    
    def generate_mobile_css_recommendations(self):
        """Genera raccomandazioni per migliorare la responsività mobile"""
        print("\n💡 RACCOMANDAZIONI PER MOBILE")
        print("-" * 40)
        
        recommendations = [
            "📱 Aggiungi breakpoint per schermi molto piccoli (320px)",
            "📱 Ottimizza la tipografia per mobile (font-size: 16px minimo)",
            "📱 Aggiungi stili per orientamento landscape su mobile",
            "📱 Ottimizza spaziature e padding per touch",
            "📱 Aggiungi stili per dark mode mobile",
            "📱 Ottimizza performance su connessioni lente"
        ]
        
        for rec in recommendations:
            print(rec)
        
        return recommendations
    
    def run_full_test(self):
        """Esegue tutti i test di responsività mobile"""
        print("📱 TEST COMPLETO RESPONSIVITÀ MOBILE ARCS-VV")
        print("="*60)
        
        all_issues = []
        
        # Esegui tutti i test
        issues1 = self.test_viewport_meta()
        issues2 = self.test_css_media_queries()
        issues3 = self.test_mobile_menu()
        issues4 = self.test_responsive_images()
        issues5 = self.test_touch_friendly_elements()
        issues6 = self.test_page_specific_responsiveness()
        
        all_issues.extend(issues1 + issues2 + issues3 + issues4 + issues5 + issues6)
        
        # Genera raccomandazioni
        self.generate_mobile_css_recommendations()
        
        # Riepilogo finale
        print("\n" + "="*60)
        print("📊 RIEPILOGO TEST RESPONSIVITÀ MOBILE")
        print("="*60)
        
        if all_issues:
            print(f"❌ Problemi identificati: {len(all_issues)}")
            for issue in all_issues:
                print(f"  • {issue}")
        else:
            print("✅ Nessun problema critico identificato!")
        
        print("\n🎯 PROSSIMI PASSI:")
        print("1. Testa il sito su dispositivi mobili reali")
        print("2. Usa gli strumenti di sviluppo del browser (F12)")
        print("3. Verifica su diverse dimensioni di schermo")
        print("4. Testa la navigazione touch")
        
        print("\n" + "="*60)
        
        return all_issues

def main():
    """Funzione principale"""
    print("📱 MOBILE RESPONSIVENESS TESTER ARCS-VV")
    print("="*50)
    
    try:
        tester = MobileResponsivenessTester()
        issues = tester.run_full_test()
        
        if issues:
            print(f"\n⚠️  ATTENZIONE: {len(issues)} problemi identificati")
            print("Risolvi questi problemi per garantire una migliore esperienza mobile")
        else:
            print("\n🎉 Eccellente! Il sito sembra ben ottimizzato per mobile")
            
    except Exception as e:
        print(f"\n❌ Errore durante il test: {e}")
        print("Verifica la configurazione del progetto")

if __name__ == "__main__":
    main()
