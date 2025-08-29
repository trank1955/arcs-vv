#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per rigenerare completamente la pagina news.html dal database JSON
Risolve i problemi di duplicati e griglia non allineata
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def regenerate_news_page():
    """Rigenera completamente la pagina news.html dal database JSON"""
    
    # Percorsi
    root = Path(__file__).resolve().parent.parent
    news_json_path = root / "pages" / "news" / "news.json"
    news_html_path = root / "pages" / "news.html"
    backup_path = root / "pages" / "news.html.backup"
    
    print("🔄 Rigenerazione completa della pagina news.html...")
    
    # Crea backup della pagina esistente
    if news_html_path.exists():
        shutil.copy2(news_html_path, backup_path)
        print(f"💾 Backup creato: {backup_path}")
    
    # Leggi le news dal JSON
    try:
        with open(news_json_path, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        print(f"📰 Caricate {len(news_data)} news dal JSON")
    except Exception as e:
        print(f"❌ Errore nella lettura di news.json: {e}")
        return False
    
    # Ordina le news per data (più recenti in cima)
    news_data_sorted = sorted(news_data, key=lambda x: x['date'], reverse=True)
    print(f"📅 News ordinate cronologicamente (più recenti in cima)")
    
    # Crea il contenuto HTML per tutte le news
    news_html = ""
    
    for i, news in enumerate(news_data_sorted):
        # Apri una nuova riga se è l'inizio di una coppia
        if i % 2 == 0:
            news_html += "  <!-- COPPIA " + str((i // 2) + 1) + " -->\n      <tr>\n"
        
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
                image_src = f"https://vumbnail.com/{video_id}.jpg"
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
            news_html += f"""        <td width="50%" valign="top">
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
            news_html += f"""        <td width="50%" valign="top">
          <div class="article-card" style="width: 100%; height: 220px; object-fit: cover; display: block;">
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
            news_html += "\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
        elif i == len(news_data) - 1:
            # Ultima news - completa la riga se necessario
            if i % 2 == 0:
                # Ultima news in posizione pari (riga incompleta)
                news_html += "\n        <td width=\"50%\" valign=\"top\"></td>\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
            else:
                # Ultima news in posizione dispari (riga completa)
                news_html += "\n      </tr>\n      <tr><td colspan=\"2\" style=\"height:2em\"></td></tr>\n"
    
    # Crea la nuova tabella completa
    new_table = f"""  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;max-width:900px;">

{news_html}
  </table>"""
    
    # Crea la pagina HTML completa
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>News – ARCS-VV</title>
  <link rel="icon" type="image/x-icon" href="../icons/favicon.ico">
  <link rel="stylesheet" href="../main.css?v=1080">
</head>
<body class="page-news">
  <h1 class="page-title news-title"><img src="../icons/news-icon.svg" alt="News" style="height:32px;width:32px;vertical-align:middle;margin-right:10px;">News</h1>
  
{new_table}

      <!-- Layout alternativo per MOBILE -->
      <div class="mobile-blog-container" style="display: none;">
        <!-- Articoli mobile verranno generati dinamicamente -->
      </div>

      <br>
      <!-- Invito all'azione -->
      <div style="text-align: center; margin: 3em 0 2em 0; padding: 2em; background: #f5e9d8; border-radius: 8px;">
        <h3>💡 Vuoi essere sempre aggiornato?</h3>
        <p>Seguici sui social media o <a href="contatti.html">contattaci</a> per ricevere tutte le novità sulle nostre attività.</p>
        <div style="margin-top: 1.5em;">
          <a href="iscriviti.html" class="button">Iscriviti come volontario</a>
          <a href="statuto.html" class="button" style="margin-left: 1em;">sostieni le nostre attività</a>
        </div>
      </div>
    
    <!-- Spazio aggiuntivo per evitare sovrapposizioni con il footer -->
    <div style="height: 120px; width: 100%; clear: both;"></div>
    
  </div>

  <footer style="background:#f2f2f2; width:100%; position:fixed; bottom:0; left:0; right:0; text-align:center; padding:1rem 0; margin:0; display:block; z-index:1000;">
    <div style="width:100%; text-align:center; max-width:100%;">
      <p style="font-style:italic; font-size:0.85em; margin:0 auto; display:inline-block; text-align:center;">&copy; 2025 ARCS-VV - Associazione Rete di Cittadinanza Solidale. Tutti i diritti riservati.</p>
    </div>
  </footer>

  <!-- Include JavaScript per il menu mobile -->
  <script src="../main.js"></script>
</body>
</html>"""
    
    # Salva la nuova pagina
    try:
        with open(news_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"💾 Pagina news.html rigenerata e salvata")
        print(f"✅ Griglia creata con {len(news_data)} news in layout 2x2 perfetto")
        return True
    except Exception as e:
        print(f"❌ Errore nel salvataggio di news.html: {e}")
        return False

if __name__ == "__main__":
    success = regenerate_news_page()
    if success:
        print("🎉 Rigenerazione completata con successo!")
        print("📱 Ora puoi aprire la pagina nel browser e vedere la griglia perfetta!")
    else:
        print("❌ Rigenerazione fallita!")
