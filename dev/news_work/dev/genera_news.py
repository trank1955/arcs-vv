import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Percorsi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, '../../../templates')
NEWS_JSON = os.path.join(BASE_DIR, '../news.json')
NEWS_PAGES_DIR = os.path.join(BASE_DIR, '../')
NEWS_DETAIL_DIR = os.path.join(NEWS_PAGES_DIR, 'news')

def slugify(title):
    import re
    # Rimuove tutti i caratteri non alfanumerici, spazi o trattini
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def add_new_post(posts):
    print("\n--- Nuovo post news ---")
    title = input("Titolo: ").strip()
    slug = slugify(title)
    date = input(f"Data (YYYY-MM-DD) [default: oggi]: ").strip() or datetime.now().strftime('%Y-%m-%d')
    author = input("Autore [default: ARCS-VV]: ").strip() or "ARCS-VV"
    excerpt = input("Estratto: ").strip()
    print("Inserisci il contenuto HTML (termina con una riga vuota):")
    lines = []
    while True:
        line = input()
        if line == '':
            break
        lines.append(line)
    content = '\n'.join(lines)
    youtube = []
    pdf = []
    if input("Aggiungere video YouTube? (s/n): ").lower() == 's':
        while True:
            url = input("URL (invio per terminare): ").strip()
            if not url:
                break
            youtube.append(url)
    if input("Aggiungere PDF? (s/n): ").lower() == 's':
        while True:
            fname = input("Nome file PDF (invio per terminare): ").strip()
            if not fname:
                break
            pdf.append(fname)
    post = {
        "title": title,
        "slug": slug,
        "date": date,
        "author": author,
        "excerpt": excerpt,
        "content": content,
        "youtube": youtube,
        "pdf": pdf
    }
    posts.insert(0, post)  # inserisce in cima
    print(f"Aggiunto post: {title} (slug: {slug})")

def main():
    os.makedirs(NEWS_DETAIL_DIR, exist_ok=True)
    # Carica i dati dei post
    if os.path.exists(NEWS_JSON):
        with open(NEWS_JSON, encoding='utf-8') as f:
            posts = json.load(f)
    else:
        posts = []

    # Modalità interattiva per aggiungere un nuovo post
    if input("Vuoi aggiungere una nuova news? (s/n): ").lower() == 's':
        add_new_post(posts)
        # Salva news.json aggiornato
        with open(NEWS_JSON, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print("news.json aggiornato.")

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    news_index_template = env.get_template('news.html')  # template per la pagina indice
    news_post_template = env.get_template('news_template.html')  # template per i singoli post

    # Genera la pagina indice delle news
    with open(os.path.join(NEWS_PAGES_DIR, 'news.html'), 'w', encoding='utf-8') as f:
        f.write(news_index_template.render(posts=posts))

    # Genera una pagina per ogni post
    for post in posts:
        out_path = os.path.join(NEWS_DETAIL_DIR, f"{post['slug']}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(news_post_template.render(post=post))

    print("News generate correttamente!")

if __name__ == "__main__":
    main()
