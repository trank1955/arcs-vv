# Sistema News per ARCS-VV

Questo documento spiega come utilizzare il sistema di gestione delle news per l'associazione ARCS-VV.

> **📚 NUOVO!** Ora disponibile anche il **Page Manager** per gestire le pagine statiche del sito. Vedi [README_PAGE_MANAGER.md](README_PAGE_MANAGER.md) per i dettagli.

## 🎯 **Cosa Fa il Blog Manager**

Il **Blog Manager** è un sistema completo e automatizzato che:

### **📰 Gestione Contenuti:**
- **Crea articoli HTML** automaticamente da titolo e riassunto
- **Genera slug URL-friendly** (es: "Workshop Solidarietà" → "workshop-solidarieta")
- **Gestisce immagini** con percorsi corretti e responsive
- **Mantiene database JSON** sempre aggiornato

### **🎨 Layout Automatico:**
- **Disposizione a griglia 2x2** per tutte le news
- **Design responsive** che si adatta a desktop e mobile
- **Stile uniforme** per tutti gli articoli
- **Spaziatura perfetta** tra le news

### **🔗 Integrazione Sito:**
- **Link "leggi tutto"** funzionanti automaticamente
- **Navigazione bidirezionale** (news → articolo → indietro)
- **Aggiornamento pagina principale** in tempo reale
- **Percorsi corretti** per CSS, JS e immagini

## 📁 Struttura dei File

```
arcs-vv-nuovo/
├── pages/
│   ├── news.html                    # Pagina principale delle news
│   └── news/                        # Directory degli articoli
│       ├── news.json               # Database delle news
│       ├── articolo-1.html         # Articoli individuali
│       ├── articolo-2.html
│       └── ...
├── tools/
│   ├── blog_manager.py             # Script principale per la gestione
│   ├── blog_manager/               # Modulo Python
│   ├── create_news_example.py      # Esempio di utilizzo
│   ├── update_news.py              # Script di aggiornamento
│   └── clean_news.py               # Pulizia e manutenzione
└── immagini/                        # Immagini per le news
    ├── blog-cover_photo-300.jpeg
    ├── YOUTUBE_THUMBNAIL.jpg
    └── ...
```

## 🚀 Come Creare una Nuova News

### Metodo 1: Script Python (Raccomandato)

```python
from tools.blog_manager import create_news_article

# Crea una nuova news
success = create_news_article(
    title="Titolo della news",
    summary="Riassunto della news...",
    image="nome-immagine.jpg"  # Opzionale
)

if success:
    print("News creata con successo!")
```

**Cosa succede automaticamente:**
1. ✅ **Articolo HTML** creato in `pages/news/titolo-slug.html`
2. ✅ **Slug generato** automaticamente dal titolo
3. ✅ **Database aggiornato** (`news.json` rigenerato)
4. ✅ **Pagina principale** aggiornata con la nuova news
5. ✅ **Link funzionanti** immediatamente disponibili

### Metodo 2: Script di Esempio

```bash
cd tools
python3 create_news_example.py
```

### Metodo 3: Script Principale

```bash
cd tools
python3 blog_manager.py
```

## 📝 Formato delle News

Ogni news deve avere:

- **Titolo**: Descrittivo e chiaro
- **Riassunto**: Breve descrizione del contenuto
- **Immagine** (opzionale): Nome file dalla directory `immagini/`
- **Autore**: Automaticamente impostato su "ARCS-VV"
- **Data**: Automaticamente impostata alla data corrente

## 🖼️ Immagini Disponibili

Le seguenti immagini sono disponibili nella directory `immagini/`:

- `blog-cover_photo-300.jpeg` - Immagine generica per news
- `YOUTUBE_THUMBNAIL.jpg` - Per news video/YouTube
- `blog-med-1200x630-24-690x362.jpeg` - Per news speciali
- `banner-solidarieta.png` - Per news di solidarietà

## 🎥 **Sistema Video Embedded**

### **Video Supportati:**
- **YouTube**: Link diretti (es: `https://youtube.com/watch?v=VIDEO_ID`)
- **Vimeo**: Link diretti (es: `https://vimeo.com/VIDEO_ID`)
- **File locali**: MP4, AVI, MOV, MKV

### **🎬 Funzionalità Video:**
- **Thumbnail con Play**: Mostra un'anteprima con icona play ▶️
- **Video Embedded**: I video si riproducono **direttamente nella pagina**
- **Link Speciale**: "🎥 Guarda il video →" invece di "Leggi tutto →"
- **Responsive**: I video si adattano automaticamente alla larghezza
- **Nessun Redirect**: L'utente rimane sempre sul sito

### **Formato Nome File:**
- **YouTube**: `youtube_VIDEO_ID` (es: `youtube_dQw4w9WgXcQ`)
- **Vimeo**: `vimeo_VIDEO_ID` (es: `vimeo_123456789`)
- **Locali**: `video_TIMESTAMP.ext` (es: `video_20250101_120000.mp4`)

### **Come Caricare Video:**
1. Nel menu principale scegli "2. Carica filmato/YouTube/Vimeo"
2. Scegli il tipo (YouTube, Vimeo o file locale)
3. Inserisci l'URL o il percorso del file
4. Il sistema estrae automaticamente l'ID e genera il thumbnail

## 🔧 Script Disponibili

### `news_manager.py` ⭐ **SCRIPT INTERATTIVO COMPLETO**
Script interattivo con menu per gestire tutto:
- **📰 Crea/Modifica/Cancella news** con interfaccia
- **🖼️ Carica immagini, filmati, PDF** automaticamente
- **🎥 Supporto YouTube** con thumbnail automatici
- **📊 Statistiche complete** del database
- **🧹 Pulizia e manutenzione** automatica

**Come usarlo:**
```bash
cd tools
python3 news_manager.py
```

### `blog_manager.py` ⭐ **MODULO PRINCIPALE**
Modulo Python con funzioni per la gestione delle news:
- **Genera `news.json`** dai file HTML esistenti
- **Crea nuovi articoli** con layout automatico
- **Aggiorna il database** e la pagina principale
- **Gestisce la griglia 2x2** per tutte le news
- **Mantiene percorsi corretti** per link e risorse

**Funzioni principali:**
- `create_news_article()` - Crea nuova news
- `generate_news_json_from_html()` - Rigenera database
- `update_news_page()` - Aggiorna pagina principale
- `slugify()` - Converte titoli in URL-friendly

### `create_news_example.py`
Script di esempio che mostra come creare multiple news:
- Crea 3 news di esempio
- Mostra diversi tipi di contenuto
- Aggiorna automaticamente il database

### `update_news_page.py` ⭐ **AGGIORNAMENTO PAGINA**
Script specializzato per aggiornare la pagina principale:
- **Inserisce nuove news** nella pagina `news.html`
- **Mantiene layout a griglia** 2x2 perfetto
- **Gestisce disposizione responsive** per mobile
- **Aggiorna solo le ultime 5 news** per performance

### `update_news.py`
Script per aggiornare il sistema:
- Rigenera `news.json`
- Deploy su directory pubbliche

### `clean_news.py`
Script per la pulizia e manutenzione:
- Rimuove duplicati
- Rimuove post di test
- Normalizza i dati

## 📊 Database News (news.json)

Il file `news.json` contiene tutte le informazioni delle news:

```json
[
  {
    "title": "Titolo della news",
    "slug": "slug-url-friendly",
    "author": "ARCS-VV",
    "date": "2025-08-28",
    "image": "nome-immagine.jpg",
    "summary": "Riassunto della news..."
  }
]
```

## 🌐 Integrazione con il Sito

Dopo aver creato una news:

1. **Articolo HTML**: Viene creato automaticamente in `pages/news/`
2. **Database**: `news.json` viene aggiornato automaticamente
3. **Pagina News**: I link "leggi tutto" funzionano immediatamente
4. **Navigazione**: L'articolo è accessibile dalla pagina principale

### **🎨 Layout Automatico della Griglia**

Il sistema genera automaticamente una **griglia perfetta 2x2** con **ordinamento cronologico**:

```html
<!-- COPPIA 1 - News più recenti in cima -->
<tr>
  <td>News 28 Aug 2025</td>  <!-- Prima news della riga -->
  <td>News 28 Aug 2025</td>  <!-- Seconda news della riga -->
</tr>

<!-- COPPIA 2 -->
<tr>
  <td>News 28 Aug 2025</td>  <!-- Prima news della riga -->
  <td>News 28 Aug 2025</td>  <!-- Seconda news della riga -->
</tr>

<!-- COPPIA 3 -->
<tr>
  <td>News 09 Aug 2025</td>  <!-- Prima news della riga -->
  <td>News 09 Aug 2025</td>  <!-- Seconda news della riga -->
</tr>

<!-- Se l'ultima news è in posizione dispari, si completa la riga -->
<tr>
  <td>News 09 Aug 2025</td>  <!-- Ultima news -->
  <td></td>                   <!-- Cella vuota per completare -->
</tr>
```

**Risultato:** Layout uniforme, responsive e **ordinato cronologicamente** (più recenti in cima)! 🎯📅

## ⚠️ Note Importanti

- **Percorsi**: Tutti i percorsi sono relativi e funzionano correttamente
- **Encoding**: Usa sempre UTF-8 per caratteri speciali italiani
- **Backup**: Fai sempre un backup prima di modifiche importanti
- **Test**: Testa sempre le nuove news nel browser

### **🔗 Percorsi Corretti Generati Automaticamente**

Il sistema gestisce automaticamente tutti i percorsi:

- **Link "leggi tutto"**: `href="news/nome-articolo.html"` ✅
- **CSS e JS**: `../../main.css` e `../../menu.js` ✅
- **Immagini**: `../../immagini/nome-immagine.jpg` ✅
- **Link "torna indietro"**: `../news.html` ✅
- **Favicon**: `../../icons/favicon.ico` ✅

**Non devi preoccuparti dei percorsi - il sistema li gestisce tutto!** 🚀

## 🐛 Risoluzione Problemi

### Errore "Directory news non trovata"
- Assicurati di eseguire gli script dalla root del progetto
- Verifica che la directory `pages/news/` esista

### Link "leggi tutto" non funzionano
- **Soluzione automatica**: Usa `update_news_page.py` per correggere i percorsi
- **Verifica**: I link devono essere `href="news/nome-articolo.html"` (non `../news/`)
- **Controllo**: Assicurati che i file HTML siano in `pages/news/`
- **Rigenerazione**: Esegui `python3 tools/blog_manager.py` per aggiornare tutto

### Layout a griglia non uniforme
- **Soluzione**: Usa sempre `update_news_page()` per aggiornare la pagina
- **Verifica**: Ogni riga deve avere esattamente 2 `<td>` o completarsi con celle vuote
- **Controllo**: Cerca i commenti `<!-- NUOVA COPPIA -->` per verificare la struttura

### Immagini non si caricano
- Verifica che i file immagine esistano
- Controlla i percorsi relativi negli articoli HTML
- Assicurati che i nomi file corrispondano esattamente

## 📞 Supporto

Per problemi o domande:
1. Controlla i log degli script Python
2. Verifica la struttura delle directory
3. Controlla i percorsi nei file di configurazione
4. Testa nel browser per verificare il funzionamento

## 🚀 **Workflow Completo di Creazione News**

### **1. Creazione News**
```bash
cd tools
python3 -c "
from blog_manager import create_news_article
success = create_news_article(
    title='Titolo della tua news',
    summary='Riassunto dettagliato...',
    image='blog-cover_photo-300.jpeg'
)
print(f'✅ News creata: {success}')
"
```

### **2. Aggiornamento Pagina Principale**
```bash
python3 update_news_page.py
```

### **3. Verifica nel Browser**
- Apri `pages/news.html`
- Controlla che la nuova news sia nella griglia
- Clicca "leggi tutto" per verificare il link
- Verifica che l'articolo si apra correttamente

---

**Sistema News ARCS-VV** - Versione 2.0  
*Gestione automatica delle news con layout a griglia perfetto* 🎯
