#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esempio di utilizzo del Blog Manager per ARCS-VV
Mostra come creare nuove news e aggiornare il sistema
"""

from blog_manager import create_news_article, generate_news_json_from_html

def main():
    print("=== Esempio di creazione news per ARCS-VV ===\n")
    
    # Esempio 1: Creazione di una news semplice
    print("1. Creazione news semplice...")
    success = create_news_article(
        title="Volontariato estivo 2025",
        summary="Cerchiamo volontari per le nostre attività estive di accoglienza e supporto alle famiglie in difficoltà. Un'opportunità per fare la differenza nella nostra comunità.",
        image="blog-cover_photo-300.jpeg"
    )
    print(f"   ✅ News creata: {success}\n")
    
    # Esempio 2: Creazione di una news con immagine diversa
    print("2. Creazione news con immagine diversa...")
    success = create_news_article(
        title="Collaborazione con scuole locali",
        summary="Abbiamo avviato una collaborazione con le scuole locali per promuovere l'educazione alla solidarietà e all'intercultura. I primi risultati sono molto promettenti.",
        image="blog-med-1200x630-24-690x362.jpeg"
    )
    print(f"   ✅ News creata: {success}\n")
    
    # Esempio 3: Creazione di una news senza immagine
    print("3. Creazione news senza immagine...")
    success = create_news_article(
        title="Aggiornamento statuto associativo",
        summary="Il nostro statuto associativo è stato aggiornato per riflettere meglio i nostri obiettivi e la nostra missione. Le modifiche includono una maggiore attenzione alla sostenibilità e all'innovazione sociale."
    )
    print(f"   ✅ News creata: {success}\n")
    
    # Rigenera il news.json
    print("4. Aggiornamento news.json...")
    count = generate_news_json_from_html()
    print(f"   ✅ Generati {count} articoli in news.json\n")
    
    print("=== Operazione completata! ===")
    print("Ora puoi:")
    print("- Visualizzare le nuove news nella pagina news.html")
    print("- Cliccare sui link 'leggi tutto' per aprire gli articoli")
    print("- Usare lo script per creare altre news in futuro")

if __name__ == "__main__":
    main()
