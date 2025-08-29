#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per aggiornare automaticamente la pagina principale delle news
Legge news.json e aggiorna news.html con le nuove news
"""

import json
import re
from pathlib import Path
from datetime import datetime

def update_news_page():
    """Aggiorna la pagina principale delle news con le nuove news dal JSON"""
    
    # Percorsi
    root = Path(__file__).resolve().parent.parent
    news_json_path = root / "pages" / "news" / "news.json"
    news_html_path = root / "pages" / "news.html"
    
    if not news_json_path.exists():
        print(f"❌ File news.json non trovato: {news_json_path}")
        return False
    
    if not news_html_path.exists():
        print(f"❌ File news.html non trovato: {news_html_path}")
        return False
    
    # Leggi le news dal JSON
    try:
        with open(news_json_path, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        print(f"📰 Caricate {len(news_data)} news dal JSON")
    except Exception as e:
        print(f"❌ Errore nella lettura di news.json: {e}")
        return False
    
    # Leggi la pagina HTML esistente
    try:
        with open(news_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print("📄 Pagina news.html caricata")
    except Exception as e:
        print(f"❌ Errore nella lettura di news.html: {e}")
        return False
    
    # Trova la sezione dove inserire le nuove news
    # Per ora, aggiungiamo le nuove news alla fine della tabella esistente
    
    # Ordina le news per data (più recenti in cima) e prendi solo le ultime 5
    news_data_sorted = sorted(news_data, key=lambda x: x['date'], reverse=True)
    recent_news = news_data_sorted[:5] if len(news_data_sorted) > 5 else news_data_sorted
    print(f"📅 News ordinate cronologicamente (più recenti in cima)")
    
    # Crea il contenuto HTML per le nuove news
    new_news_html = ""
    
    for i, news in enumerate(recent_news):
        # Apri una nuova riga se è l'inizio di una coppia
        if i % 2 == 0:
            new_news_html += "      <!-- NUOVA COPPIA -->\n      <tr>\n"
        
        # Determina l'immagine da usare e se c'è un video
        image_src = "../immagini/blog-cover_photo-300.jpeg"  # Default
        video_embed = None
        
        if news.get('image'):
            if 'youtube' in news['image'].lower():
                # Estrai ID video YouTube
                video_id = news['image'].replace('youtube_', '')
                image_src = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                video_embed = f"https://www.youtube.com/embed/{video_id}"
            elif 'vimeo' in news['image'].lower():
                # Estrai ID video Vimeo
                video_id = news['image'].replace('vimeo_', '')
                image_src = f"https://vumbnail.com/{video_id}/hqdefault.jpg"
                video_embed = f"https://player.vimeo.com/video/{video_id}"
            elif 'hqdefault' in news['image']:
                image_src = "https://img.youtube.com/vi/gYX7G39FUbU/hqdefault.jpg"
            elif 'blog-med' in news['image']:
                image_src = f"../immagini/{news['image']}"
            else:
                image_src = f"../immagini/{news['image']}"
        
        # Formatta la data
        try:
            date_obj = datetime.strptime(news['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d %B %Y')
        except:
            formatted_date = news['date']
        
        # Genera il contenuto HTML per la news
        if video_embed:
            # News con video - mostra thumbnail e link al video
            new_news_html += f"""        <td width="50%" valign="top">
          <div class="article-card" style="background: transparent; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="position: relative;">
              <img src="{image_src}" alt="{news['title']}" style="width: 100%; height: 220px; object-fit: cover; display: block;">
              <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.8); border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 24px;">▶️</span>
              </div>
            </div>
            <div style="padding: 1.5em;">
              <div style="color: #666; font-size: 0.9em; margin-bottom: 0.5em;">📅 {formatted_date}</div>
              <h2 style="color: #006699; margin: 0 0 1em 0; font-size: 1.3em; line-height: 1.3;">{news['title']}</h2>
              <p style="color: #555; line-height: 1.6; margin-bottom: 1.5em;">{news.get('summary', 'Nessun riassunto disponibile.')}</p>
              <a href="news/{news['slug']}.html" style="color: #006699; text-decoration: none; font-weight: 600;">🎥 Guarda il video →</a>
            </div>
          </div>
        </td>"""
        else:
            # News normale - mostra immagine e link "leggi tutto"
            new_news_html += f"""        <td width="50%" valign="top">
          <div class="article-card" style="background: transparent; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
            <img src="{image_src}" alt="{news['title']}" style="width: 100%; height: 220px; object-fit: cover; display: block;">
            <div style="padding: 1.5em;">
              <div style="color: #666; font-size: 0.9em; margin-bottom: 0.5em;">📅 {formatted_date}</div>
              <h2 style="color: #006699; margin: 0 0 1em 0; font-size: 1.3em; line-height: 1.3;">{news['title']}</h2>
              <p style="color: #555; line-height: 1.6; margin-bottom: 1.5em;">{news.get('summary', 'Nessun riassunto disponibile.')}</p>
              <a href="news/{news['slug']}.html" style="color: #006699; text-decoration: none; font-weight: 600;">Leggi tutto →</a>
            </div>
          </div>
        </td>"""
        
        # Chiudi la riga se è la fine di una coppia O se è l'ultima news
        if i % 2 == 1:
            # Fine di una coppia completa
            new_news_html += "\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
        elif i == len(recent_news) - 1:
            # Ultima news - completa la riga se necessario
            if i % 2 == 0:
                # Ultima news in posizione pari (riga incompleta)
                new_news_html += "\n        <td width=\"50%\" valign=\"top\"></td>\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
            else:
                # Ultima news in posizione dispari (riga completa)
                new_news_html += "\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
    
    # Crea la nuova tabella completa
    new_table = f"""  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;max-width:900px;">

{new_news_html}
  </table>"""
    
    # Trova la sezione della tabella principale e sostituiscila completamente
    table_start = "  <table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"margin:0 auto;max-width:900px;\">"
    mobile_section = "      <!-- Layout alternativo per MOBILE -->"
    
    if table_start in html_content and mobile_section in html_content:
        # Trova l'inizio della tabella e l'inizio della sezione mobile
        start_pos = html_content.find(table_start)
        mobile_pos = html_content.find(mobile_section)
        
        if start_pos < mobile_pos:
            # Sostituisci tutto il contenuto dalla tabella alla sezione mobile
            html_content = html_content[:start_pos] + new_table + "\n\n      " + html_content[mobile_pos:]
            print("✅ Contenuto dalla tabella alla sezione mobile sostituito completamente")
        else:
            print("❌ Ordine errato: sezione mobile prima della tabella")
            return False
    else:
        print("❌ Tabella principale o sezione mobile non trovata nella pagina HTML")
        return False
    
    # Salva la pagina aggiornata
    try:
        with open(news_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"💾 Pagina news.html aggiornata e salvata")
        return True
    except Exception as e:
        print(f"❌ Errore nel salvataggio di news.html: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Aggiornamento pagina principale delle news...")
    success = update_news_page()
    if success:
        print("✅ Aggiornamento completato con successo!")
    else:
        print("❌ Aggiornamento fallito!")
