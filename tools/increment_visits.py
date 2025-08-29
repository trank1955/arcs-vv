#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script HTTP per incrementare il contatore visite ARCS-VV
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
