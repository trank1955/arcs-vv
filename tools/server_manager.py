#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server Manager ARCS-VV
Context manager per la gestione automatica del server HTTP
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path
from contextlib import contextmanager

class ServerManager:
    def __init__(self, port=8003, project_root=None):
        self.port = port
        self.project_root = project_root or self.get_project_root()
        self.server_process = None
        self.original_sigint = None
        
    def get_project_root(self):
        """Trova la root del progetto ARCS-VV"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "pages" / "index.html").exists():
                return current
            current = current.parent
        return Path("/home/ste/OneDrive_syncro/arcs-vv-nuovo")
    
    def find_free_port(self, start_port=8003, max_attempts=10):
        """Trova una porta libera partendo da start_port"""
        import socket
        
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        
        # Se non trova porte libere, usa una porta casuale
        import random
        return random.randint(8000, 9000)
    
    def start_server(self):
        """Avvia il server HTTP"""
        # Trova una porta libera
        self.port = self.find_free_port(self.port)
        
        print(f"🚀 Avvio server HTTP su porta {self.port}...")
        
        try:
            # Cambia directory al progetto
            os.chdir(self.project_root)
            
            # Avvia il server
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "http.server", str(self.port)
            ], cwd=self.project_root)
            
            # Aspetta che il server sia pronto
            time.sleep(2)
            
            if self.server_process.poll() is None:
                print(f"✅ Server avviato con successo!")
                print(f"🌐 Desktop: http://localhost:{self.port}/pages/")
                print(f"📱 Mobile: http://[TUO_IP]:{self.port}/pages/")
                print(f"💡 Per trovare il tuo IP: hostname -I")
                return True
            else:
                print(f"❌ Errore nell'avvio del server")
                return False
                
        except Exception as e:
            print(f"❌ Errore nell'avvio del server: {e}")
            return False
    
    def stop_server(self):
        """Ferma il server HTTP"""
        if self.server_process and self.server_process.poll() is None:
            print(f"\n⏹️  Arresto server HTTP su porta {self.port}...")
            
            try:
                # Termina il processo
                self.server_process.terminate()
                
                # Aspetta che si chiuda
                try:
                    self.server_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Se non si chiude, forza la chiusura
                    self.server_process.kill()
                    self.server_process.wait()
                
                print("✅ Server arrestato con successo")
                
            except Exception as e:
                print(f"⚠️  Errore nell'arresto del server: {e}")
            
            finally:
                self.server_process = None
    
    def setup_signal_handlers(self):
        """Configura i gestori di segnali per Ctrl+C"""
        def signal_handler(sig, frame):
            print(f"\n⏹️  Interruzione richiesta dall'utente (Ctrl+C)")
            self.stop_server()
            sys.exit(0)
        
        # Salva il gestore originale
        self.original_sigint = signal.signal(signal.SIGINT, signal_handler)
    
    def restore_signal_handlers(self):
        """Ripristina i gestori di segnali originali"""
        if self.original_sigint:
            signal.signal(signal.SIGINT, self.original_sigint)
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_signal_handlers()
        if self.start_server():
            return self
        else:
            raise RuntimeError("Impossibile avviare il server")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_server()
        self.restore_signal_handlers()
        
        # Se c'è stata un'eccezione, la rilanciamo
        if exc_type is not None:
            return False
        
        return True

@contextmanager
def http_server(port=8003, project_root=None):
    """
    Context manager per la gestione automatica del server HTTP.
    
    Esempio di utilizzo:
    ```python
    with http_server(port=8003) as server:
        print("Server attivo, esegui i tuoi test...")
        time.sleep(10)  # Simula lavoro
        print("Test completati")
    # Server si chiude automaticamente qui
    ```
    """
    server = ServerManager(port, project_root)
    try:
        yield server
    finally:
        server.stop_server()
        server.restore_signal_handlers()

def start_server_for_tool(port=8003, project_root=None):
    """
    Avvia il server per un tool specifico.
    Restituisce l'oggetto server che deve essere fermato manualmente.
    
    Esempio di utilizzo:
    ```python
    server = start_server_for_tool()
    try:
        # Esegui il tool
        print("Tool in esecuzione...")
        time.sleep(10)
    finally:
        server.stop_server()
    ```
    """
    server = ServerManager(port, project_root)
    if server.start_server():
        return server
    else:
        raise RuntimeError("Impossibile avviare il server")

if __name__ == "__main__":
    # Test del context manager
    print("🧪 TEST SERVER MANAGER ARCS-VV")
    print("=" * 50)
    
    try:
        with http_server(port=8003) as server:
            print(f"\n🎯 Server attivo su porta {server.port}")
            print("⏳ Server rimarrà attivo per 10 secondi...")
            print("💡 Premi Ctrl+C per interrompere il test")
            
            # Simula lavoro del tool
            for i in range(10, 0, -1):
                print(f"⏰ Chiusura automatica tra {i} secondi...")
                time.sleep(1)
            
            print("✅ Test completato con successo!")
            
    except KeyboardInterrupt:
        print("\n⏹️  Test interrotto dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante il test: {e}")
    
    print("\n🎉 Test completato!")
