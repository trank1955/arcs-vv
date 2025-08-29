# 🚀 ARCS-VV Nuovo - Progetto Ottimizzato

## 📋 Panoramica
Sito web statico per ARCS-VV (organizzazione no-profit) con sistema di generazione automatica e gestione news ottimizzata.

## ✨ Nuove Funzionalità

### 🔧 Script di Manutenzione
- **`tools/clean_news.py`** - Pulizia automatica database news
- **`tools/maintenance.py`** - Manutenzione completa del progetto
- **`dev/genera_sito_optimized.py`** - Generazione sito con logging avanzato

### 🧹 Sistema di Pulizia News
- Rimozione automatica duplicati
- Eliminazione post di test
- Normalizzazione titoli e slug
- Backup automatico prima della pulizia

### 📊 Generazione Sito Migliorata
- Logging dettagliato con emoji
- Gestione errori robusta
- Validazione file generati
- Statistiche complete

## 🚀 Utilizzo Rapido

### 1. Manutenzione Completa
```bash
python3 tools/maintenance.py
```

### 2. Pulizia News
```bash
python3 tools/clean_news.py
```

### 3. Generazione Sito
```bash
python3 dev/genera_sito_optimized.py
```

## 📁 Struttura Progetto

```
arcs-vv-nuovo/
├── dev/                          # Script di sviluppo
│   ├── genera_sito.py           # Generatore originale
│   ├── genera_sito_optimized.py # Generatore ottimizzato
│   ├── news.json                # Database news pulito
│   └── news_backup_*.json       # Backup automatici
├── tools/                        # Script di manutenzione
│   ├── clean_news.py            # Pulizia news
│   ├── maintenance.py           # Manutenzione completa
│   └── update_news.py           # Aggiornamento news
├── templates/                    # Template Jinja2
├── pages/                        # Pagine generate
│   ├── news/                     # Sistema news
│   └── *.html                    # Pagine principali
├── css/                          # Stili
├── js/                           # JavaScript
└── backups/                      # Backup automatici
```

## 🔍 Funzionalità Principali

### 📰 Sistema News
- **7 news attive** (pulite da duplicati e test)
- Gestione automatica slug e titoli
- Backup automatico prima delle modifiche

### 🌐 Generazione Sito
- **11 pagine generate** automaticamente
- Template Jinja2 per consistenza
- Validazione automatica dei file

### 🛠️ Manutenzione
- Backup automatico del progetto
- Pulizia database news
- Validazione integrità file
- Report dettagliati

## 📊 Statistiche Attuali

- **Pagine totali:** 11
- **News attive:** 7
- **Template:** Jinja2
- **CSS:** 34KB ottimizzato
- **JavaScript:** Menu responsive

## 🎯 Prossimi Passi

1. **Deploy automatico** su server web
2. **Sistema di preview** per le news
3. **Integrazione CMS** per gestione contenuti
4. **Ottimizzazione SEO** e performance

## 🚨 Risoluzione Problemi

### Errore Template
```bash
# Verifica che la directory templates esista
ls -la templates/
```

### Errore Dipendenze
```bash
# Installa Jinja2
pip install jinja2
```

### Backup Manuale
```bash
# Crea backup manuale
python3 tools/maintenance.py
```

## 📞 Supporto

Per problemi o domande:
1. Controlla i log degli script
2. Verifica la struttura delle directory
3. Esegui `tools/maintenance.py` per diagnostica completa

---

**🔄 Ultimo aggiornamento:** 28 Agosto 2025  
**✅ Stato:** Ottimizzato e funzionante  
**🎯 Versione:** 2.0 - Sistema di manutenzione completo
