# 🛠️ STRUMENTI DISPONIBILI - ARCS-VV WEBSITE

## 📋 **PANORAMICA COMPLETA**

Questo documento elenca tutti gli strumenti disponibili per la gestione completa del sito web ARCS-VV.

---

## 🎯 **GESTIONE NEWS (Sistema Principale)**

### **🛠️ Menu Tools** - `menu_tools.py`
**Centro di controllo unificato** per tutti gli strumenti del progetto.
**Funzionalità:**
- ✅ Menu interattivo per tutti i tool
- ✅ Organizzazione per categoria
- ✅ Comandi speciali (docs, info, server, test)
- ✅ Esecuzione automatica dei tool
- ✅ Gestione errori e feedback

**Avvio:**
```bash
python3 menu_tools.py
```

**Documentazione:** [README_MENU_TOOLS.md](README_MENU_TOOLS.md)

---

### **📰 News Manager** - `news_manager.py`
**Scopo:** Gestione completa e interattiva delle news
**Funzionalità:**
- ✅ Creazione nuove news
- ✅ Caricamento immagini e video
- ✅ Gestione PDF e documenti
- ✅ Modifica e cancellazione
- ✅ Aggiornamento pagina principale
- ✅ Statistiche e pulizia database

**Avvio:**
```bash
python3 news_manager.py
```

**Documentazione:** [README_NEWS.md](README_NEWS.md)

---

## 🌐 **GESTIONE PAGINE STATICHE (NUOVO!)**

### **📄 Page Manager** - `page_manager.py`
**Scopo:** Modifica completa delle pagine statiche del sito
**Funzionalità:**
- ✅ Modifica contenuto testuale con HTML
- ✅ Gestione immagini con ottimizzazione
- ✅ Inserimento video (YouTube, Vimeo, locale)
- ✅ Gestione PDF con anteprima
- ✅ Rigenerazione completa delle pagine
- ✅ Supporto per terzi autorizzati

**Avvio:**
```bash
python3 page_manager.py
```

**Documentazione:** [README_PAGE_MANAGER.md](README_PAGE_MANAGER.md)

---

## 🔧 **STRUMENTI DI SUPPORTO**

### **📚 Blog Manager** - `blog_manager.py`
**Scopo:** Modulo Python per la gestione delle news
**Funzionalità:**
- ✅ Classe `NewsArticle`
- ✅ Funzioni di estrazione e generazione
- ✅ Gestione JSON e HTML
- ✅ Sistema video embedded

**Utilizzo:** Importato da altri script

---

### **🔄 Regenerate News Page** - `regenerate_news_page.py`
**Scopo:** Rigenerazione completa della pagina news.html
**Funzionalità:**
- ✅ Ricostruzione griglia 2x2
- ✅ Ordinamento cronologico
- ✅ Gestione video e immagini
- ✅ Eliminazione duplicati

**Avvio:**
```bash
python3 regenerate_news_page.py
```

---

### **📝 Update News Page** - `update_news_page.py`
**Scopo:** Aggiornamento incrementale della pagina news
**Funzionalità:**
- ✅ Aggiornamento selettivo
- ✅ Mantenimento layout esistente
- ✅ Gestione video embedded

**Avvio:**
```bash
python3 update_news_page.py
```

---

## 🧪 **STRUMENTI DI TEST**

### **🔍 Test Page Manager** - `test_page_manager.py`
**Scopo:** Verifica funzionalità base del page manager
**Funzionalità:**
- ✅ Test configurazione progetto
- ✅ Verifica estrazione ID video
- ✅ Controllo struttura directory

**Avvio:**
```bash
python3 test_page_manager.py
```

---

### **📖 Esempio Page Manager** - `esempio_page_manager.py`
**Scopo:** Dimostrazione pratica del page manager
**Funzionalità:**
- ✅ Esempio modifica pagina chi-siamo
- ✅ Preparazione contenuto HTML
- ✅ Aggiunta media di esempio

**Avvio:**
```bash
python3 esempio_page_manager.py
```

---

### **🛡️  Esempio Protezione Contenuti** - `esempio_protezione_contenuti.py`
**Scopo:** Dimostrazione del sistema di protezione automatica
**Funzionalità:**
- ✅ Identificazione elementi protetti
- ✅ Mostra cosa viene preservato automaticamente
- ✅ Spiegazione del funzionamento della protezione

**Avvio:**
```bash
python3 esempio_protezione_contenuti.py
```

---

### **👥 Visitor Counter** - `visitor_counter.py`
**Scopo:** Sistema completo di conteggio visite per il sito
**Funzionalità:**
- ✅ Conteggio automatico delle visite
- ✅ Statistiche dettagliate (giornaliere, mensili, annuali)
- ✅ Interfaccia elegante integrata nel sito
- ✅ Gestione dati persistente in JSON
- ✅ Aggiornamento in tempo reale

**Avvio:**
```bash
python3 visitor_counter.py
```

**Documentazione:** [README_VISITOR_COUNTER.md](README_VISITOR_COUNTER.md)

---

## 📁 **STRUTTURA COMPLETA**

```
arcs-vv-nuovo/tools/
├── 🎯 news_manager.py              # Gestione news interattiva
├── 🌐 page_manager.py              # Gestione pagine statiche
├── 📚 blog_manager.py              # Modulo Python news
├── 🔄 regenerate_news_page.py      # Rigenerazione completa news
├── 📝 update_news_page.py          # Aggiornamento incrementale
├── 🧪 test_page_manager.py         # Test page manager
├── 📖 esempio_page_manager.py      # Esempio pratico
├── 🛡️  esempio_protezione_contenuti.py  # Esempio protezione contenuti
├── ⚙️  page_config.json            # Configurazione page manager
├── 👥 visitor_counter.py            # Sistema contatore visite
├── 🔄 increment_visits.py          # Script incremento visite
├── 📚 README_NEWS.md               # Documentazione news
├── 📚 README_PAGE_MANAGER.md       # Documentazione page manager
├── 📚 README_VISITOR_COUNTER.md    # Documentazione contatore
├── 🚀 ISTRUZIONI_RAPIDE.md         # Guida rapida
└── 🛠️  STRUMENTI_DISPONIBILI.md    # Questo file
```

---

## 🎯 **SCELTA DELLO STRUMENTO**

### **Per Gestire le News:**
```bash
python3 news_manager.py
```

### **Per Modificare Pagine Statiche:**
```bash
python3 page_manager.py
```

### **Per Rigenerare Completamente le News:**
```bash
python3 regenerate_news_page.py
```

### **Per Testare il Page Manager:**
```bash
python3 test_page_manager.py
```

---

## 🔒 **SICUREZZA E PERMESSI**

### **Accesso Autorizzato:**
- Solo utenti autorizzati possono utilizzare i tool
- Richiede accesso alla directory del progetto
- Permessi di lettura/scrittura sui file

### **Backup:**
- **SEMPRE** fare backup prima di modificare
- I tool sovrascrivono completamente i file
- Non esiste sistema di rollback automatico

---

## 📦 **REQUISITI TECNICI**

### **Dipendenze Python:**
```bash
pip3 install Pillow
```

### **Sistema Operativo:**
- ✅ Linux (testato su Ubuntu)
- ✅ macOS (compatibile)
- ✅ Windows (con WSL o Git Bash)

---

## 🆘 **SUPPORTO E TROUBLESHOOTING**

### **Problemi Comuni:**
1. **Permessi file:** Verificare accesso in lettura/scrittura
2. **Dipendenze:** Installare Pillow per gestione immagini
3. **Percorsi:** Verificare struttura directory del progetto
4. **Codifica:** Assicurarsi che i file siano in UTF-8

### **Log e Debug:**
- Tutti i tool mostrano messaggi informativi
- In caso di errore, viene mostrato il dettaglio completo
- Controllare sempre la console per informazioni

---

## 🚀 **WORKFLOW COMPLETO**

### **Gestione Sito Completo:**
1. **📰 News:** Usa `news_manager.py` per aggiornamenti frequenti
2. **🌐 Pagine Statiche:** Usa `page_manager.py` per modifiche strutturali
3. **🔄 Manutenzione:** Usa `regenerate_news_page.py` per pulizia
4. **🧪 Test:** Usa script di test per verifiche

### **Per Terzi Autorizzati:**
- **News:** Accesso completo tramite `news_manager.py`
- **Pagine:** Accesso limitato tramite `page_manager.py`
- **Documentazione:** Guide complete per ogni strumento

---

## 📈 **ROADMAP FUTURA**

### **Funzionalità Pianificate:**
- 🔄 Sistema di backup automatico
- 📊 Dashboard web per gestione
- 🔐 Sistema di autenticazione utenti
- 📱 App mobile per gestione rapida
- 🌍 Supporto multilingua

---

## 📞 **CONTATTI E SUPPORTO**

### **Per Problemi Tecnici:**
1. Controllare la documentazione specifica
2. Eseguire script di test
3. Verificare configurazione progetto
4. Controllare log e messaggi di errore

### **Per Nuove Funzionalità:**
- Documentare richieste
- Specificare casi d'uso
- Fornire esempi pratici

---

**Versione:** 2.0  
**Data:** 29 Agosto 2025  
**Autore:** Claudio (AI Assistant)  
**Progetto:** ARCS-VV Website Management System  
**Stato:** Sistema completo e funzionante
