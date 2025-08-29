#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visitor Counter per ARCS-VV
Sistema di conteggio visite per il sito web
"""

import json
import os
from datetime import datetime, date
from pathlib import Path

class VisitorCounter:
    def __init__(self):
        self.project_root = self.get_project_root()
        self.data_file = self.project_root / "tools" / "visitor_data.json"
        self.initialize_data()
    
    def get_project_root(self):
        """Trova la root del progetto ARCS-VV"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "pages" / "index.html").exists():
                return current
            current = current.parent
        return Path("/home/ste/OneDrive_syncro/arcs-vv-nuovo")
    
    def initialize_data(self):
        """Inizializza il file dati se non esiste"""
        if not self.data_file.exists():
            initial_data = {
                "total_visits": 0,
                "daily_visits": {},
                "monthly_visits": {},
                "yearly_visits": {},
                "last_visit": None,
                "created_date": datetime.now().isoformat()
            }
            self.save_data(initial_data)
    
    def load_data(self):
        """Carica i dati esistenti"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Errore nel caricamento dati: {e}")
            return self.get_default_data()
    
    def save_data(self, data):
        """Salva i dati"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio dati: {e}")
            return False
    
    def get_default_data(self):
        """Restituisce dati di default"""
        return {
            "total_visits": 0,
            "daily_visits": {},
            "monthly_visits": {},
            "yearly_visits": {},
            "last_visit": None,
            "created_date": datetime.now().isoformat()
        }
    
    def increment_visit(self):
        """Incrementa il contatore di visite"""
        data = self.load_data()
        today = date.today()
        current_month = f"{today.year}-{today.month:02d}"
        current_year = str(today.year)
        
        # Incrementa visite totali
        data["total_visits"] += 1
        
        # Incrementa visite giornaliere
        today_str = today.isoformat()
        data["daily_visits"][today_str] = data["daily_visits"].get(today_str, 0) + 1
        
        # Incrementa visite mensili
        data["monthly_visits"][current_month] = data["monthly_visits"].get(current_month, 0) + 1
        
        # Incrementa visite annuali
        data["yearly_visits"][current_year] = data["yearly_visits"].get(current_year, 0) + 1
        
        # Aggiorna ultima visita
        data["last_visit"] = datetime.now().isoformat()
        
        # Salva i dati
        if self.save_data(data):
            return data
        return None
    
    def get_stats(self):
        """Restituisce le statistiche delle visite"""
        data = self.load_data()
        today = date.today()
        today_str = today.isoformat()
        current_month = f"{today.year}-{today.month:02d}"
        current_year = str(today.year)
        
        stats = {
            "total": data["total_visits"],
            "today": data["daily_visits"].get(today_str, 0),
            "this_month": data["monthly_visits"].get(current_month, 0),
            "this_year": data["yearly_visits"].get(current_year, 0),
            "last_visit": data["last_visit"]
        }
        
        return stats
    
    def generate_html_counter(self):
        """Genera il codice HTML per il contatore"""
        stats = self.get_stats()
        
        # Formatta la data dell'ultima visita
        last_visit_str = "Mai"
        if stats["last_visit"]:
            try:
                last_visit = datetime.fromisoformat(stats["last_visit"])
                last_visit_str = last_visit.strftime("%d/%m/%Y %H:%M")
            except:
                last_visit_str = "Mai"
        
        html = f'''<!-- Contatore Visite ARCS-VV -->
<div class="visitor-counter" style="
  background: linear-gradient(135deg, var(--link-color), #004466);
  color: white;
  padding: 1.5em;
  border-radius: 12px;
  text-align: center;
  margin: 2em auto;
  max-width: 400px;
  box-shadow: 0 4px 15px rgba(0, 102, 153, 0.3);
  position: relative;
  overflow: hidden;
">
  <!-- Elemento decorativo -->
  <div style="
    position: absolute;
    top: -20px;
    right: -20px;
    width: 60px;
    height: 60px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    transform: rotate(45deg);
  "></div>
  
  <!-- Icona -->
  <div style="
    font-size: 2.5em;
    margin-bottom: 0.5em;
    opacity: 0.9;
  ">👥</div>
  
  <!-- Titolo -->
  <h3 style="
    margin: 0 0 1em 0;
    font-size: 1.3em;
    font-weight: 600;
    opacity: 0.95;
  ">Contatore Visite</h3>
  
  <!-- Statistiche -->
  <div style="
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1em;
    margin-bottom: 1.5em;
  ">
    <div style="
      background: rgba(255, 255, 255, 0.15);
      padding: 0.8em;
      border-radius: 8px;
      backdrop-filter: blur(10px);
    ">
      <div style="
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 0.2em;
      ">{stats["total"]:,}</div>
      <div style="
        font-size: 0.9em;
        opacity: 0.9;
      ">Totale</div>
    </div>
    
    <div style="
      background: rgba(255, 255, 255, 0.15);
      padding: 0.8em;
      border-radius: 8px;
      backdrop-filter: blur(10px);
    ">
      <div style="
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 0.2em;
      ">{stats["today"]}</div>
      <div style="
        font-size: 0.9em;
        opacity: 0.9;
      ">Oggi</div>
    </div>
  </div>
  
  <!-- Visite mensili e annuali -->
  <div style="
    display: flex;
    justify-content: space-between;
    margin-bottom: 1em;
    font-size: 0.9em;
    opacity: 0.8;
  ">
    <span>📅 Mese: {stats["this_month"]}</span>
    <span>📊 Anno: {stats["this_year"]}</span>
  </div>
  
  <!-- Ultima visita -->
  <div style="
    font-size: 0.85em;
    opacity: 0.7;
    font-style: italic;
  ">
    Ultima visita: {last_visit_str}</div>
  
  <!-- Pulsante aggiorna -->
  <button onclick="refreshCounter()" style="
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 0.5em 1em;
    border-radius: 6px;
    margin-top: 1em;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9em;
  " onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">
    🔄 Aggiorna
  </button>
</div>

<script>
// Funzione per aggiornare il contatore
function refreshCounter() {{
  // Incrementa il contatore
  fetch('/tools/increment_visits.py', {{
    method: 'POST',
    headers: {{
      'Content-Type': 'application/json',
    }},
    body: JSON.stringify({{'action': 'increment'}})
  }})
  .then(response => response.json())
  .then(data => {{
    if (data.success) {{
      // Ricarica la pagina per mostrare i nuovi dati
      location.reload();
    }}
  }})
  .catch(error => {{
    console.log('Errore nell\\'aggiornamento contatore:', error);
    // Fallback: ricarica comunque la pagina
    location.reload();
  }});
}}

// Incrementa automaticamente al caricamento della pagina
document.addEventListener('DOMContentLoaded', function() {{
  // Incrementa solo se non è già stato fatto in questa sessione
  if (!sessionStorage.getItem('visitCounted')) {{
    refreshCounter();
    sessionStorage.setItem('visitCounted', 'true');
  }}
}});
</script>'''
        
        return html
    
    def create_increment_script(self):
        """Crea lo script per incrementare le visite via HTTP"""
        script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script HTTP per incrementare il contatore visite
"""

import json
import sys
import os
from pathlib import Path

# Aggiungi la directory tools al path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

try:
    from visitor_counter import VisitorCounter
    
    def handle_request():
        """Gestisce la richiesta HTTP"""
        # Leggi l'input
        try:
            input_data = sys.stdin.read()
            if input_data:
                data = json.loads(input_data)
                action = data.get('action', '')
                
                if action == 'increment':
                    counter = VisitorCounter()
                    result = counter.increment_visit()
                    
                    if result:
                        response = {"success": True, "visits": result["total_visits"]}
                    else:
                        response = {"success": False, "error": "Errore nel salvataggio"}
                else:
                    response = {"success": False, "error": "Azione non valida"}
            else:
                response = {"success": False, "error": "Nessun dato ricevuto"}
                
        except json.JSONDecodeError:
            response = {"success": False, "error": "JSON non valido"}
        except Exception as e:
            response = {"success": False, "error": str(e)}
        
        # Output della risposta
        print("Content-Type: application/json")
        print()
        print(json.dumps(response, ensure_ascii=False))
    
    if __name__ == "__main__":
        handle_request()
        
except ImportError as e:
    print("Content-Type: application/json")
    print()
    print(json.dumps({"success": False, "error": f"Import error: {e}"}, ensure_ascii=False))
except Exception as e:
    print("Content-Type: application/json")
    print()
    print(json.dumps({"success": False, "error": f"Unexpected error: {e}"}, ensure_ascii=False))
'''
        
        script_path = self.project_root / "tools" / "increment_visits.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Rendi eseguibile
        os.chmod(script_path, 0o755)
        return script_path
    
    def show_stats(self):
        """Mostra le statistiche attuali"""
        stats = self.get_stats()
        print("📊 STATISTICHE VISITE ARCS-VV")
        print("="*40)
        print(f"👥 Visite totali: {stats['total']:,}")
        print(f"📅 Visite oggi: {stats['today']}")
        print(f"📊 Visite questo mese: {stats['this_month']}")
        print(f"📈 Visite questo anno: {stats['this_year']}")
        if stats['last_visit']:
            try:
                last_visit = datetime.fromisoformat(stats['last_visit'])
                print(f"🕐 Ultima visita: {last_visit.strftime('%d/%m/%Y %H:%M')}")
            except:
                print(f"🕐 Ultima visita: {stats['last_visit']}")
        print("="*40)
    
    def reset_counter(self):
        """Resetta il contatore (solo per amministratori)"""
        confirm = input("⚠️  Sei sicuro di voler resettare il contatore? (s/n): ").strip().lower()
        if confirm == 's':
            data = self.get_default_data()
            if self.save_data(data):
                print("✅ Contatore resettato con successo!")
            else:
                print("❌ Errore nel reset del contatore")
        else:
            print("❌ Reset annullato")

def main():
    """Funzione principale"""
    print("👥 VISITOR COUNTER ARCS-VV")
    print("="*40)
    
    counter = VisitorCounter()
    
    while True:
        print("\n🎯 SCEGLI UN'OPZIONE:")
        print("1. 📊 Mostra statistiche")
        print("2. 🔄 Incrementa visita")
        print("3. 📄 Genera HTML contatore")
        print("4. 📝 Crea script incremento")
        print("5. 🗑️  Reset contatore")
        print("0. 🚪 Esci")
        print("-" * 40)
        
        choice = input("Scelta: ").strip()
        
        if choice == "1":
            counter.show_stats()
        elif choice == "2":
            result = counter.increment_visit()
            if result:
                print(f"✅ Visita incrementata! Totale: {result['total_visits']:,}")
            else:
                print("❌ Errore nell'incremento")
        elif choice == "3":
            html = counter.generate_html_counter()
            print("📄 HTML del contatore generato:")
            print("="*50)
            print(html)
            print("="*50)
        elif choice == "4":
            script_path = counter.create_increment_script()
            print(f"📝 Script creato: {script_path}")
        elif choice == "5":
            counter.reset_counter()
        elif choice == "0":
            print("👋 Arrivederci!")
            break
        else:
            print("❌ Scelta non valida!")

if __name__ == "__main__":
    main()
