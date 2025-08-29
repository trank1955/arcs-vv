# 📚 PAGE MANAGER ARCS-VV - Documentazione Completa

## 🎯 **COSA FA IL PAGE MANAGER**

Il **Page Manager** è uno strumento completo per gestire le pagine statiche del sito ARCS-VV. Permette a terzi autorizzati di modificare facilmente il contenuto delle pagine esistenti senza dover conoscere HTML o CSS avanzati.

### 🛡️ **PROTEZIONE AUTOMATICA DEI CONTENUTI**

**NUOVO!** Il Page Manager ora identifica e protegge automaticamente elementi importanti come:
- **🔘 Pulsanti** (class="button", <button>)
- **📝 Form** completi
- **📜 Script** inline
- **🎨 Elementi personalizzati** (custom-box, visitor-counter, cta-buttons)
- **🆔 Elementi con ID specifici**

Questi elementi vengono **PRESERVATI** durante la rigenerazione della pagina, garantendo che funzionalità importanti non vengano mai perse.

### ✨ **FUNZIONALITÀ PRINCIPALI:**

- **📝 Modifica contenuto testuale** con supporto per tag HTML comuni
- **🖼️  Gestione immagini** con ottimizzazione automatica
- **🎥 Inserimento video** (YouTube, Vimeo, file locali)
- **📄 Gestione PDF** con anteprima e download
- **🔄 Rigenerazione completa** delle pagine HTML
- **📋 Riepilogo modifiche** in tempo reale

---

## 🚀 **COME UTILIZZARLO**

### **1. AVVIO DELLO SCRIPT**

```bash
cd /home/ste/OneDrive_syncro/arcs-vv-nuovo/tools
python3 page_manager.py
```

### **2. FLUSSO DI LAVORO**

1. **Selezione pagina** da modificare
2. **Caricamento contenuto** esistente
3. **Modifiche multiple** nell'ordine preferito
4. **Rigenerazione** della pagina HTML
5. **Verifica** del risultato

---

## 📋 **MENU PRINCIPALE**

```
🌐 PAGE MANAGER ARCS-VV - MENU PRINCIPALE
============================================================
1. 📝 Modifica contenuto testuale
2. 🖼️  Aggiungi immagine
3. 🎥 Aggiungi video
4. 📄 Aggiungi PDF
5. 🔄 Rigenera pagina
6. 📋 Mostra riepilogo modifiche
7. 🔄 Cambia pagina
8. 🛡️  Mostra elementi protetti
0. 🚪 Esci
============================================================
```

---

## 🔧 **DETTAGLIO FUNZIONI**

### **1. 📝 MODIFICA CONTENUTO TESTUALE**

**Cosa fa:**
- Carica il contenuto attuale della pagina
- Mostra i tag HTML supportati
- Permette di inserire nuovo contenuto con formattazione

**Tag HTML supportati:**
- `<strong>` o `<b>` per il **grassetto**
- `<em>` o `<i>` per il *corsivo*
- `<u>` per il <u>sottolineato</u>
- `<h2>`, `<h3>` per i titoli
- `<ul>`, `<li>` per le liste
- `<p>` per i paragrafi
- `<br>` per le interruzioni di riga
- `<a href='...'>` per i link

**Esempio di utilizzo:**
```html
<h2>La nostra missione</h2>
<p>ARCS-VV promuove <strong>iniziative concrete</strong> per l'integrazione e il supporto dei migranti nel territorio di <em>Vittorio Veneto</em>.</p>

<h3>Servizi offerti</h3>
<ul>
  <li>Sportello di orientamento legale e linguistico</li>
  <li>Laboratori culturali e creativi</li>
  <li>Gruppi di supporto psicologico</li>
</ul>
```

### **2. 🖼️  AGGIUNTA IMMAGINE**

**Cosa fa:**
- Mostra le immagini già presenti nel progetto
- Permette di selezionare un'immagine esterna
- Ottimizza automaticamente (ridimensionamento, compressione)
- Salva nel progetto con nome personalizzato
- Richiede testo alternativo e didascalia opzionale

**Caratteristiche:**
- **Formati supportati:** JPG, JPEG, PNG
- **Ottimizzazione automatica:** Max 1200px, qualità 85%
- **Conversione automatica:** RGBA → RGB se necessario
- **Salvataggio intelligente:** Evita duplicati

**Esempio di output HTML:**
```html
<div style="text-align: center; margin: 2em 0;">
  <img src="../immagini/volontari.jpg" alt="Volontari al lavoro" style="max-width: 100%; height: auto; border-radius: 8px;">
  <p style="font-style: italic; color: #666; margin-top: 0.5em;">I nostri volontari durante un laboratorio</p>
</div>
```

### **3. 🎥 AGGIUNTA VIDEO**

**Tipi supportati:**

#### **YouTube**
- Estrazione automatica dell'ID del video
- Supporto per tutti i formati URL YouTube
- Embed responsive con controlli completi

#### **Vimeo**
- Estrazione automatica dell'ID del video
- Supporto per URL Vimeo standard
- Embed responsive con controlli completi

#### **File Locali**
- Copia automatica nel progetto
- Supporto per tutti i formati video
- Player HTML5 nativo con controlli

**Esempio di output HTML:**
```html
<!-- YouTube -->
<div style="text-align: center; margin: 2em 0;">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="Video YouTube" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="max-width:100%; border-radius:8px;"></iframe>
</div>

<!-- File locale -->
<div style="text-align: center; margin: 2em 0;">
  <video width="560" height="315" controls style="max-width:100%; border-radius:8px;">
    <source src="../immagini/presentazione.mp4" type="video/mp4">
    Il tuo browser non supporta il tag video.
  </video>
</div>
```

### **4. 📄 AGGIUNTA PDF**

**Cosa fa:**
- Copia il PDF nel progetto
- Crea un riquadro elegante con anteprima
- Fornisce pulsanti per visualizzare e scaricare
- Richiede titolo e descrizione opzionale

**Esempio di output HTML:**
```html
<div style="text-align: center; margin: 2em 0; padding: 1.5em; border: 2px solid #e0e0e0; border-radius: 8px; background: #f9f9f9;">
  <h3>📄 Statuto ARCS-VV</h3>
  <p>Documento ufficiale dell'associazione</p>
  <div style="margin-top: 1em;">
    <a href="../immagini/statuto.pdf" target="_blank" class="button" style="margin-right: 1em;">👁️  Visualizza PDF</a>
    <a href="../immagini/statuto.pdf" download class="button">⬇️  Scarica PDF</a>
  </div>
</div>
```

### **5. 🔄 RIGENERAZIONE PAGINA**

**Cosa fa:**
- Mostra riepilogo completo delle modifiche
- Richiede conferma prima della sovrascrittura
- Genera HTML completo e ottimizzato
- Mantiene struttura e stile del sito
- Salva la pagina modificata

**⚠️  ATTENZIONE:**
- La pagina viene **ricreata da zero**
- Il contenuto esistente viene **sostituito completamente**
- **Sempre fare backup** prima di procedere

### **6. 📋 MOSTRA RIEPILOGO MODIFICHE**

**Informazioni mostrate:**
- Nome della pagina corrente
- Titolo della pagina
- Lunghezza del contenuto testuale
- Numero di immagini, video e PDF
- Dettagli di ogni elemento multimediale

### **7. 🔄 CAMBIA PAGINA**

**Cosa fa:**
- Permette di passare a un'altra pagina
- Carica automaticamente il contenuto esistente
- Mantiene le modifiche non salvate in memoria

### **8. 🛡️  MOSTRA ELEMENTI PROTETTI**

**Cosa fa:**
- Visualizza tutti gli elementi identificati e protetti
- Mostra anteprima di pulsanti, form, script e elementi personalizzati
- Conferma che questi elementi saranno preservati durante la rigenerazione

---

## 🎨 **STRUTTURA HTML GENERATA**

### **Template Base:**
```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TITOLO – ARCS-VV</title>
  <link rel="icon" type="image/x-icon" href="../icons/favicon.ico">
  <link rel="stylesheet" href="../main.css?v=1080&t=20250803135018">
  <div id="menu-inject"></div>
  <script src="../menu.js"></script>
</head>
<body class="page-NOME_PAGINA">
  <h1 class="page-title NOME_PAGINA-title">
    <img src="../icons/NOME_PAGINA-icon.svg" alt="TITOLO"> TITOLO
  </h1>
  
  <div class="page-wrapper">
    <main>
      <section class="NOME_PAGINA">
        <!-- CONTENUTO PRINCIPALE -->
        <!-- IMMAGINI -->
        <!-- VIDEO -->
        <!-- PDF -->
      </section>
    </main>
  </div>
  
  <footer>...</footer>
</body>
</html>
```

---

## 🔒 **SICUREZZA E PERMESSI**

### **Accesso Autorizzato:**
- Solo utenti autorizzati possono utilizzare il tool
- Richiede accesso alla directory del progetto
- Permessi di lettura/scrittura sui file HTML

### **🛡️  Protezione Automatica:**
- **Elementi importanti** vengono identificati e protetti automaticamente
- **Pulsanti, form e script** sono sempre preservati
- **Funzionalità del sito** non vengono mai compromesse
- **Controllo completo** di cosa viene preservato

### **Backup Automatico:**
- **SEMPRE** fare backup prima di modificare
- Il tool sovrascrive completamente le pagine
- Non esiste sistema di rollback automatico

---

## 🚨 **TROUBLESHOOTING**

### **Problema: "Impossibile caricare la pagina"**
**Soluzione:** Verificare i permessi del file e la codifica UTF-8

### **Problema: "Errore nell'elaborazione dell'immagine"**
**Soluzione:** Verificare che PIL/Pillow sia installato: `pip3 install Pillow`

### **Problema: "File non trovato"**
**Soluzione:** Verificare i percorsi assoluti e i permessi di accesso

### **Problema: "Errore nella generazione della pagina"**
**Soluzione:** Verificare i permessi di scrittura nella directory pages

### **Problema: "Elementi protetti non identificati"**
**Soluzione:** Usare l'opzione 8 per verificare cosa viene protetto automaticamente

### **Problema: "Pulsanti/form scomparsi dopo rigenerazione"**
**Soluzione:** Verificare che gli elementi abbiano classi o ID riconosciuti dal sistema

---

## 📦 **REQUISITI TECNICI**

### **Dipendenze Python:**
```bash
pip3 install Pillow
```

### **Struttura Directory:**
```
arcs-vv-nuovo/
├── pages/           # Pagine HTML
├── immagini/        # Media files
├── icons/          # Icone e logo
├── tools/          # Script di gestione
└── main.css        # Stili del sito
```

---

## 🔄 **WORKFLOW COMPLETO**

### **Esempio di Modifica Pagina "Chi Siamo":**

1. **Avvio script:** `python3 page_manager.py`
2. **Selezione pagina:** Scegli "chi-siamo.html"
3. **Caricamento:** Contenuto esistente caricato
4. **Modifiche:**
   - Aggiorna testo con nuovi servizi
   - Aggiungi foto dei volontari
   - Inserisci video YouTube di presentazione
   - Aggiungi PDF dello statuto
5. **Rigenerazione:** Conferma e genera nuova pagina
6. **Verifica:** Controlla il risultato nel browser

---

## 📝 **NOTE IMPORTANTI**

### **Prima di Iniziare:**
- ✅ Fare backup della pagina da modificare
- ✅ Preparare tutti i testi in formato HTML
- ✅ Avere pronti i file media (immagini, video, PDF)
- ✅ Conoscere i percorsi completi dei file

### **Durante la Modifica:**
- ✅ Salvare le modifiche prima di uscire
- ✅ Testare la pagina dopo la rigenerazione
- ✅ Verificare che tutti i link funzionino
- ✅ Controllare la responsività su mobile

### **Dopo la Modifica:**
- ✅ Testare la pagina nel browser
- ✅ Verificare che il menu funzioni
- ✅ Controllare che i media si carichino
- ✅ Testare su dispositivi diversi

---

## 🆘 **SUPPORTO**

### **In caso di Problemi:**
1. Controllare i messaggi di errore
2. Verificare i permessi dei file
3. Controllare la struttura delle directory
4. Verificare le dipendenze Python

### **Log e Debug:**
- Il tool mostra messaggi informativi per ogni operazione
- In caso di errore, viene mostrato il dettaglio completo
- Controllare sempre la console per informazioni

---

**Versione:** 1.1  
**Data:** 29 Agosto 2025  
**Autore:** Claudio (AI Assistant)  
**Progetto:** ARCS-VV Website Management System  
**Aggiornamento:** Sistema di protezione automatica dei contenuti
