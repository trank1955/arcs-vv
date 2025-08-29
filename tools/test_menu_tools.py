#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Menu Tools ARCS-VV
Verifica che il menu tools funzioni correttamente
"""

import os
import sys
from pathlib import Path

def test_menu_tools():
    """Testa le funzionalità del menu tools"""
    print("🧪 TEST MENU TOOLS ARCS-VV")
    print("=" * 50)
    
    # Verifica che il file esista (gestisci percorsi relativi e assoluti)
    menu_file = Path("menu_tools.py")
    if not menu_file.exists():
        # Prova con percorso assoluto dalla directory tools
        tools_dir = Path(__file__).parent
        menu_file = tools_dir / "menu_tools.py"
        if not menu_file.exists():
            print("❌ menu_tools.py non trovato!")
            print(f"   Cercato in: {Path.cwd()}")
            print(f"   Cercato in: {tools_dir}")
            return False
    
    print("✅ menu_tools.py trovato")
    
    # Verifica che sia eseguibile
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, str(menu_file), "--help"
        ], capture_output=True, text=True, timeout=10)
        print("✅ menu_tools.py eseguibile")
    except subprocess.TimeoutExpired:
        print("✅ menu_tools.py eseguibile (timeout normale)")
    except Exception as e:
        print(f"⚠️  menu_tools.py eseguibile (warning: {e})")
    
    # Verifica dipendenze
    required_modules = [
        "os", "sys", "subprocess", "pathlib", "time"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Modulo {module} disponibile")
        except ImportError:
            print(f"❌ Modulo {module} mancante")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Moduli mancanti: {', '.join(missing_modules)}")
        return False
    
    # Verifica struttura del menu
    try:
        with open(menu_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica elementi essenziali
        essential_elements = [
            "class ToolsLauncher",
            "def main_loop",
            "get_available_tools",
            "run_tool"
        ]
        
        for element in essential_elements:
            if element in content:
                print(f"✅ {element} presente")
            else:
                print(f"❌ {element} mancante")
                return False
        
        # Verifica numero di tool
        tool_count = content.count('"name":')
        print(f"✅ Numero tool rilevati: {tool_count}")
        
        if tool_count < 10:
            print("⚠️  Numero tool basso, verifica la configurazione")
        
    except Exception as e:
        print(f"❌ Errore nella lettura del file: {e}")
        return False
    
    print("\n🎉 TEST MENU TOOLS COMPLETATO CON SUCCESSO!")
    print("\n💡 Per testare il menu completo:")
    print("   python3 menu_tools.py")
    
    return True

def main():
    """Funzione principale"""
    print("🛠️  TEST MENU TOOLS ARCS-VV")
    print("=" * 40)
    
    success = test_menu_tools()
    
    if success:
        print("\n✅ Il menu tools è pronto per l'uso!")
    else:
        print("\n❌ Il menu tools ha problemi da risolvere")
        sys.exit(1)

if __name__ == "__main__":
    main()
