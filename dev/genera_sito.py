from jinja2 import Environment, FileSystemLoader
import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Dati menu centralizzato
MENU = [
    {"title": "Home", "url": "index.html"},
    {"title": "Attività", "url": "attivita.html"},
    {"title": "Chi siamo", "url": "chi-siamo.html"},
    {"title": "Dove siamo", "url": "dove-siamo.html"},
    {"title": "Donazioni", "url": "donazioni.html"},
    {"title": "Contatti", "url": "contatti.html"},
]

# Dati di tutte le pagine principali
PAGES = [
    {"filename": "index.html", "template": "index.html"},
    {"filename": "attivita.html", "template": "attivita.html"},
    {"filename": "chi-siamo.html", "template": "chi-siamo.html"},
    {"filename": "dove-siamo.html", "template": "dove-siamo.html"},
    {"filename": "donazioni.html", "template": "donazioni.html"},
    {"filename": "iscriviti.html", "template": "iscriviti.html"},
    {"filename": "news.html", "template": "news.html"},
    {"filename": "statuto.html", "template": "statuto.html"},
    {"filename": "contatti.html", "template": "contatti.html"},
    {"filename": "404.html", "template": "404.html"},
    {"filename": "thankyou.html", "template": "thankyou.html"},
]
# Genera tutte le pagine usando il template specifico
output_dir = os.path.join("..", "pages")
os.makedirs(output_dir, exist_ok=True)
for page in PAGES:
    template = env.get_template(page["template"])
    output = template.render()
    out_path = os.path.join(output_dir, page["filename"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Pagina generata: {out_path}")
