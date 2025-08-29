  # 🎯 Blog Creator Avanzato - Sistema Multimediale ARCS-VV
# Versione con supporto per PDF e video YouTube

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
import re
import shutil
from config_paths import *

class BlogCreatorAdvanced:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 ARCS-VV Blog Creator Avanzato")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variabili
        self.title_var = tk.StringVar()
        self.slug_var = tk.StringVar()
        self.author_var = tk.StringVar(value="ARCS-VV")
        self.category_var = tk.StringVar(value="news")
        self.content_var = tk.StringVar()
        
        # Multimedia vars
        self.pdf_files = []
        self.youtube_videos = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Notebook per tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Informazioni Base
        self.setup_basic_tab(notebook)
        
        # Tab 2: Contenuto
        self.image_var = tk.StringVar()
        self.excerpt_var = tk.StringVar()
        self.setup_content_tab(notebook)
        
        # Tab 3: Multimedia
        self.setup_multimedia_tab(notebook)
        
        # Tab 4: Anteprima
        self.setup_preview_tab(notebook)
        
        # Bottoni di controllo
        self.setup_control_buttons()
        
    def setup_basic_tab(self, notebook):
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="📝 Informazioni Base")
        
        # Titolo
        ttk.Label(basic_frame, text="Titolo articolo:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,5))
        title_entry = ttk.Entry(basic_frame, textvariable=self.title_var, font=("Arial", 11), width=80)
        title_entry.pack(fill="x", padx=5, pady=(0,10))
        title_entry.bind('<KeyRelease>', self.update_slug)
        
        # Slug (nome file)
        ttk.Label(basic_frame, text="Nome file (slug):", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,5))
        slug_entry = ttk.Entry(basic_frame, textvariable=self.slug_var, font=("Arial", 11), width=80)
        slug_entry.pack(fill="x", padx=5, pady=(0,10))
        
        # Frame per autore e categoria
        meta_frame = ttk.Frame(basic_frame)
        meta_frame.pack(fill="x", pady=10)
        
        # Autore
        ttk.Label(meta_frame, text="Autore:", font=("Arial", 10)).pack(side="left")
        author_entry = ttk.Entry(meta_frame, textvariable=self.author_var, width=30)
        author_entry.pack(side="left", padx=(5,20))
        
        # Categoria
        ttk.Label(meta_frame, text="Categoria:", font=("Arial", 10)).pack(side="left")
        categories = ["news", "eventi", "progetti", "comunicati", "workshop", "fundraising"]
        category_combo = ttk.Combobox(meta_frame, textvariable=self.category_var, values=categories, width=20)
        category_combo.pack(side="left", padx=5)
        
        # Info
        info_frame = ttk.LabelFrame(basic_frame, text="ℹ️ Informazioni", padding=10)
        info_frame.pack(fill="x", pady=20)
        
        info_text = """✅ Il titolo verrà usato come H1 principale
✅ Lo slug viene generato automaticamente dal titolo
✅ Il file sarà salvato in blog/posts/[slug].html
✅ Puoi modificare manualmente lo slug se necessario"""
        
        ttk.Label(info_frame, text=info_text, font=("Arial", 9)).pack(anchor="w")
        
    def setup_content_tab(self, notebook):
        content_frame = ttk.Frame(notebook)
        notebook.add(content_frame, text="📄 Contenuto")
        
        ttk.Label(content_frame, text="Contenuto dell'articolo:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,5))
        
        # Area di testo per il contenuto
        self.content_text = scrolledtext.ScrolledText(
            content_frame, 
            height=25, 
            font=("Arial", 11),
            wrap=tk.WORD
        )
        self.content_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Suggerimenti
        tips_frame = ttk.LabelFrame(content_frame, text="💡 Suggerimenti Formattazione", padding=10)
        tips_frame.pack(fill="x", pady=10)
        
        tips_text = """🔸 Usa <h2>Titolo Sezione</h2> per i sottotitoli
🔸 Usa <p>testo</p> per i paragrafi
🔸 Usa <strong>testo</strong> per il grassetto
🔸 Usa <em>testo</em> per il corsivo
🔸 Usa <br> per andare a capo"""
        
        ttk.Label(tips_frame, text=tips_text, font=("Arial", 9)).pack(anchor="w")
        
    def setup_multimedia_tab(self, notebook):
        multimedia_frame = ttk.Frame(notebook)
        notebook.add(multimedia_frame, text="🎬 Multimedia")
        
        # Sezione PDF
        pdf_frame = ttk.LabelFrame(multimedia_frame, text="📄 Allegati PDF", padding=10)
        pdf_frame.pack(fill="x", pady=10)
        
        ttk.Button(pdf_frame, text="➕ Aggiungi PDF", command=self.add_pdf).pack(side="left", padx=5)
        ttk.Button(pdf_frame, text="🗑️ Rimuovi Selezionato", command=self.remove_pdf).pack(side="left", padx=5)
        
        # Lista PDF
        self.pdf_listbox = tk.Listbox(pdf_frame, height=6)
        self.pdf_listbox.pack(fill="x", pady=10)
        
        # Sezione YouTube
        youtube_frame = ttk.LabelFrame(multimedia_frame, text="🎥 Video YouTube", padding=10)
        youtube_frame.pack(fill="x", pady=10)
        
        ttk.Label(youtube_frame, text="URL YouTube:").pack(anchor="w")
        self.youtube_entry = ttk.Entry(youtube_frame, width=60)
        self.youtube_entry.pack(fill="x", pady=5)
        
        youtube_buttons = ttk.Frame(youtube_frame)
        youtube_buttons.pack(fill="x", pady=5)
        
        ttk.Button(youtube_buttons, text="➕ Aggiungi Video", command=self.add_youtube).pack(side="left", padx=5)
        ttk.Button(youtube_buttons, text="🗑️ Rimuovi Selezionato", command=self.remove_youtube).pack(side="left", padx=5)
        
        # Lista YouTube
        self.youtube_listbox = tk.Listbox(youtube_frame, height=6)
        self.youtube_listbox.pack(fill="x", pady=10)
        
        # Info multimedia
        info_frame = ttk.LabelFrame(multimedia_frame, text="ℹ️ Informazioni Multimedia", padding=10)
        info_frame.pack(fill="x", pady=10)
        
        info_text = """📄 PDF: Verranno copiati in blog/pdf/ e collegati automaticamente
🎥 YouTube: Inserisci URL completo (es: https://www.youtube.com/watch?v=ABC123)
✅ I contenuti multimediali appariranno alla fine dell'articolo"""
        
        ttk.Label(info_frame, text=info_text, font=("Arial", 9)).pack(anchor="w")
        
    def setup_preview_tab(self, notebook):
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="👁️ Anteprima")
        
        ttk.Label(preview_frame, text="Anteprima HTML:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,5))
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            height=30,
            font=("Courier", 10),
            wrap=tk.WORD
        )
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Button(preview_frame, text="🔄 Aggiorna Anteprima", command=self.update_preview).pack(pady=10)
        
    def setup_control_buttons(self):
        # Bottoni fissati in basso
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        ttk.Button(button_frame, text="🔄 Aggiorna Anteprima", command=self.update_preview).pack(side="left", padx=5)
        ttk.Button(button_frame, text="💾 Salva Articolo", command=self.save_article).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🌐 Salva e Apri", command=self.save_and_open).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Chiudi", command=self.root.quit).pack(side="right", padx=5)
        
    def update_slug(self, event=None):
        """Genera slug automaticamente dal titolo"""
        title = self.title_var.get()
        # Converte in lowercase, sostituisce spazi e caratteri speciali
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        self.slug_var.set(slug)
        
    def add_pdf(self):
        """Aggiunge allegato PDF"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            filename = os.path.basename(file_path)
            self.pdf_files.append({"path": file_path, "name": filename})
            self.pdf_listbox.insert(tk.END, filename)
            
    def remove_pdf(self):
        """Rimuove PDF selezionato"""
        selection = self.pdf_listbox.curselection()
        if selection:
            index = selection[0]
            self.pdf_files.pop(index)
            self.pdf_listbox.delete(index)
            
    def add_youtube(self):
        """Aggiunge video YouTube"""
        url = self.youtube_entry.get().strip()
        if url:
            # Estrae ID video da URL YouTube
            video_id = self.extract_youtube_id(url)
            if video_id:
                title = f"Video YouTube: {video_id}"
                self.youtube_videos.append({"url": url, "id": video_id, "title": title})
                self.youtube_listbox.insert(tk.END, title)
                self.youtube_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "URL YouTube non valido")
                
    def remove_youtube(self):
        """Rimuove video YouTube selezionato"""
        selection = self.youtube_listbox.curselection()
        if selection:
            index = selection[0]
            self.youtube_videos.pop(index)
            self.youtube_listbox.delete(index)
            
    def extract_youtube_id(self, url):
        """Estrae ID video da URL YouTube"""
        patterns = [
            r'youtube\.com/watch\?v=([^&]+)',
            r'youtu\.be/([^?]+)',
            r'youtube\.com/embed/([^?]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
        
    def generate_multimedia_html(self):
        """Genera HTML per contenuti multimediali"""
        html = ""
        
        # Sezione PDF
        if self.pdf_files:
            html += """
    <section class="pdf-attachments">
      <h2>📄 Documenti Allegati</h2>
      <div class="pdf-list">
"""
            for pdf in self.pdf_files:
                html += f"""        <div class="pdf-item">
          <a href="../pdf/{pdf['name']}" target="_blank" class="pdf-link">
            <span class="pdf-icon">📄</span>
            <span class="pdf-name">{pdf['name']}</span>
            <span class="pdf-action">Scarica PDF</span>
          </a>
        </div>
"""
            html += """      </div>
    </section>
"""
        
        # Sezione YouTube
        # Mostra i video solo se non sono YouTube (es. altri embed, non il primo YouTube)
        if self.youtube_videos:
            # Prendi l'ID del primo video YouTube
            first_youtube_id = None
            first_video = self.youtube_videos[0]
            if isinstance(first_video, dict) and 'id' in first_video:
                first_youtube_id = first_video['id']
            # Se ci sono altri video (non YouTube), mostra solo quelli
            other_videos = [v for v in self.youtube_videos if not (isinstance(v, dict) and v.get('id') == first_youtube_id)]
            if other_videos:
                html += """
    <section class="youtube-videos">
      <h2>🎥 Video</h2>
      <div class="video-list">
"""
                for video in other_videos:
                    html += f"""        <div class="video-item">
          <div class="video-wrapper">
            <iframe 
              src="https://www.youtube.com/embed/{video['id']}" 
              frameborder="0" 
              allowfullscreen
              class="youtube-embed">
            </iframe>
          </div>
        </div>
"""
                html += """      </div>
    </section>
"""
        
        return html
        
    def generate_multimedia_css(self):
        """Genera CSS per multimedia"""
        return """
    /* === MULTIMEDIA STYLES === */
    .pdf-attachments, .youtube-videos {
      margin: 2rem 0;
      padding: 1.5rem;
      background: #f8f9fa;
      border-radius: 8px;
      border-left: 4px solid #007bff;
    }
    
    .pdf-list, .video-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    
    .pdf-item {
      background: white;
      border-radius: 6px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: transform 0.2s ease;
    }
    
    .pdf-item:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .pdf-link {
      display: flex;
      align-items: center;
      padding: 1rem;
      text-decoration: none;
      color: #333;
      gap: 1rem;
    }
    
    .pdf-icon {
      font-size: 1.5rem;
    }
    
    .pdf-name {
      flex: 1;
      font-weight: 500;
    }
    
    .pdf-action {
      background: #007bff;
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      font-size: 0.9rem;
    }
    
    .video-wrapper {
      position: relative;
      padding-bottom: 56.25%; /* 16:9 aspect ratio */
      height: 0;
      overflow: hidden;
      background: #000;
      border-radius: 8px;
    }
    
    .youtube-embed {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border-radius: 8px;
    }
    
    @media (max-width: 768px) {
      .pdf-attachments, .youtube-videos {
        padding: 1rem;
      }
      
      .pdf-link {
        padding: 0.75rem;
        gap: 0.75rem;
      }
      
      .pdf-action {
        padding: 0.4rem 0.8rem;
        font-size: 0.85rem;
      }
    }
"""
        
    def update_preview(self):
        """Aggiorna anteprima HTML"""
        html = self.generate_article_html()
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, html)
        
    def generate_article_html(self):
        """Genera HTML completo dell'articolo"""
        title = self.title_var.get() or "Titolo Articolo"
        author = self.author_var.get() or "ARCS-VV"
        content = self.content_text.get(1.0, tk.END).strip()
        multimedia_html = self.generate_multimedia_html()
        multimedia_css = self.generate_multimedia_css()
        current_date = datetime.now().strftime("%d/%m/%Y")
        # YouTube embed in fondo
        youtube_embed = ""
        if self.youtube_videos:
            youtube_url = self.youtube_videos[0]['url'] if isinstance(self.youtube_videos[0], dict) else self.youtube_videos[0]
            match = re.search(r'(?:v=|youtu\.be/)([\w-]+)', youtube_url)
            if match:
                video_id = match.group(1)
                youtube_embed = f'<div class="blog-youtube" style="margin-top:2em;text-align:center;"><iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video" frameborder="0" allowfullscreen></iframe></div>'
        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} – ARCS-VV</title>
  <link rel="icon" type="image/x-icon" href="../../icons/favicon.ico">
  <link rel="icon" type="image/png" href="../../icons/favicon.ico">
  <link rel="shortcut icon" href="../../icons/favicon.ico">
  <link rel="stylesheet" href="../../main.css?v=1000">
  <style>
    .logo-title {{
      margin-left: -10px !important;
    }}
    nav ul li a {{
      text-align: left !important;
      display: flex !important;
      align-items: flex-start !important;
      justify-content: flex-start !important;
      line-height: 1.1 !important;
    }}
    {multimedia_css}
  </style>
</head>
<body>

  <!-- Menu statico -->
  <nav>
    <div class="logo-container">
      <a href="../../index.html">
        <img src="../../icons/favicon.ico" alt="ARCS-VV" class="logo">
      </a>
      <div class="logo-title">
        Associazione Rete di<br>Cittadinanza Solidale
      </div>
    </div>
    <ul>
      <li><a href="../../index.html">Home</a></li>
      <li><a href="../../pagine/attivita.html">Le nostre<br>attività</a></li>
      <li><a href="../../pagine/dove-siamo.html">Dove siamo</a></li>
      <li><a href="../../pagine/chi-siamo.html">Chi siamo</a></li>
      <li><a href="../../pagine/statuto.html">Statuto</a></li>
      <li><a href="../../pagine/news.html">News</a></li>
      <li><a href="../../pagine/contatti.html">Contatti</a></li>
      <li><a href="../../pagine/iscriviti.html">Iscriviti</a></li>
      <li><a href="../../pagine/donazioni.html">Donazioni</a></li>
    </ul>
  </nav>

  <!-- Contenuto della pagina -->
  <div class="blog-container">
    <article class="blog-post">
      <header class="blog-header">
        <h1>{title}</h1>
        <div class="blog-meta">
          <span class="author">Di: {author}</span>
          <span class="date">Pubblicato: {current_date}</span>
        </div>
      </header>
      <div class="blog-content">
        {content}
      </div>
      {multimedia_html}
      {youtube_embed}
      <footer class="blog-footer">
        <div class="back-link">
          <a href="../../pagine/news.html">← Torna alle News</a>
        </div>
      </footer>
    </article>
  </div>

  <!-- Footer -->
  <footer>
    <p>&copy; 2025 ARCS-VV - Associazione Rete di Cittadinanza Solidale</p>
  </footer>

</body>
</html>"""
        return html
        
    def save_article(self):
        """Salva l'articolo e aggiorna la pagina news"""
        if not self.title_var.get():
            messagebox.showerror("Errore", "Il titolo è obbligatorio")
            return

        if not self.slug_var.get():
            messagebox.showerror("Errore", "Lo slug è obbligatorio")
            return

        try:
            # Copia file PDF se presenti
            if self.pdf_files:
                os.makedirs(PDF_DIR, exist_ok=True)
                for pdf in self.pdf_files:
                    dest_path = os.path.join(PDF_DIR, pdf['name'])
                    shutil.copy2(pdf['path'], dest_path)
                    print(f"✅ PDF copiato: {pdf['name']}")

            # Salva articolo HTML
            filename = f"{self.slug_var.get()}.html"
            file_path = os.path.join(POSTS_DIR, filename)

            html_content = self.generate_article_html()

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Aggiorna la pagina delle news
            try:
                # Import dinamico se non già importata
                try:
                    from blog_creator_simple import update_news_page
                except ImportError:
                    from blog_deleter import update_news_page
                # Recupera dati per la news
                title = self.title_var.get()
                date_str = datetime.now().strftime("%d/%m/%Y")
                image_path = self.image_var.get() if hasattr(self, 'image_var') else "images/blog-cover_photo-300.jpeg"
                # Se è stato inserito un video YouTube, aggiungi il link all'excerpt
                excerpt = self.excerpt_var.get() if hasattr(self, 'excerpt_var') else ""
                if self.youtube_videos:
                    # Prendi il primo video inserito
                    youtube_url = self.youtube_videos[0]['url'] if isinstance(self.youtube_videos[0], dict) else self.youtube_videos[0]
                    excerpt += f"\nYouTube: {youtube_url}"
                update_news_page(title, date_str, image_path, excerpt, filename)
                print("✅ Pagina news aggiornata con la miniatura del nuovo post")
                messagebox.showinfo("Successo", f"Articolo salvato: {filename}\nLa pagina news è stata aggiornata.")
            except Exception as e:
                print(f"⚠️ Errore aggiornamento pagina news: {e}")
                messagebox.showwarning("Attenzione", f"Articolo salvato, ma la pagina news NON è stata aggiornata.\nErrore: {e}")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {str(e)}")
            
    def save_and_open(self):
        """Salva, aggiorna news e apre l'articolo"""
        self.save_article()
        filename = f"{self.slug_var.get()}.html"
        file_path = os.path.join(POSTS_DIR, filename)
        if os.path.exists(file_path):
            os.startfile(file_path)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("🎯 Avvio Blog Creator Avanzato...")
    app = BlogCreatorAdvanced()
    app.run()
