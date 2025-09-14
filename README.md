# 📊 Log Analyzer - Click Fraud Detection

Strumento specializzato per il rilevamento di **click fraud** nei log dei siti che utilizzano Google Ads. Analizza automaticamente i file di log web per identificare visite sospette provenienti dal network di Google Ads ma originarie da paesi diversi dall'Italia.

## 🎯 Scopo

Questo analizzatore è progettato per individuare attività di **click fraud** specificamente da:
- ✅ Visite con parametro `gclid` (Google Click ID)
- ✅ Provenienti da IP non italiani
- ✅ Con referrer esterno al dominio analizzato

## ✨ Caratteristiche

- 🔍 Analisi automatica di file di log compressi (GZ, BZ2, ZIP)
- 📦 Supporto per diverse strutture di archiviazione
- 📈 Generazione di statistiche dettagliate per click fraud
- 🗂️ Struttura organizzata per cliente/dominio
- 🌍 Geocoding degli IP per identificazione geografica
- 🚨 Rilevamento automatico di pattern sospetti

## 🚀 Utilizzo

### 1. 📥 Download e Setup del progetto

#### Clona il repository:
```bash
git clone https://github.com/martinomh/analisi-log-click-fraud.git
cd analisi-log-click-fraud
```

#### Configura l'ambiente:
```bash
# Installa le dipendenze Python
pip install -r requirements.txt

# Configura il database GeoIP e crea la struttura per un nuovo dominio
python setup.py example.com
```

Questo comando:
- 🔧 Configura automaticamente il database GeoIP (se necessario)
- 📁 Crea la cartella `clienti/example.com/logs/` dove inserirai i file di log da analizzare

**Nota**: Se vuoi configurare solo il database GeoIP senza creare un dominio:
```bash
python setup.py --geoip-only
```

### 2. 📊 Analisi dei log

1. 📂 Posiziona il file ZIP dei log nella cartella `clienti/example.com/logs/`
2. ▶️ Esegui l'analisi:

```bash
python run_analysis.py example.com
```

Questo comando esegue l'analisi dei log e genera le statistiche.

#### 🔍 Cosa analizza lo script:

- **Pattern di ricerca**: Cerca righe contenenti `gclid=` (Google Click ID)
- **Filtro geografico**: Filtra solo IP non italiani
- **Filtro referrer**: Considera solo visite con referrer esterno
- **Output**: Genera file con le righe sospette e statistiche CSV

#### 📈 Risultati generati:

- `risultati.txt`: Log delle visite sospette (non italiane con gclid)
- `stats.csv`: Statistiche dettagliate per paese, referrer, data, ecc.

### 3. ⚙️ Opzioni avanzate

Per analizzare solo i log o solo le statistiche:

```bash
python run_analysis.py example.com --skip-stats
python run_analysis.py example.com --skip-analysis
```

Per specificare un tipo di struttura ZIP diverso:

```bash
python run_analysis.py example.com --zip-structure flat_bz2
```

## 📦 Strutture ZIP supportate
- `flat_gz`: Archivio ZIP contenente file GZ
- `flat_bz2`: Archivio ZIP contenente file BZ2
- `nested_zip`: Archivio ZIP contenente altri file ZIP
- `flat_log`: Archivio ZIP contenente direttamente file di log
- `directory`: Directory contenente file di log (non compressi)

## 🌍 Database GeoIP

Questo progetto include il database GeoLite2 per il geocoding degli IP. Il database viene configurato automaticamente durante il setup.

**Attribuzione**: Questo progetto utilizza GeoLite2 creato da MaxMind, disponibile su [https://www.maxmind.com](https://www.maxmind.com)

## ✅ Vantaggi della struttura
Questa struttura è molto semplice e intuitiva:
- 🏷️ Il nome della cartella è lo stesso del dominio
- ⚙️ Non è necessario configurare manualmente il nome del dominio
- 🔍 Il file ZIP viene trovato automaticamente
- 💾 I risultati vengono salvati direttamente nella cartella del dominio
- 🚨 Rilevamento automatico di click fraud sospetti

Tutto ciò che devi fare è creare una cartella con il nome del dominio, mettere il file ZIP nella sottocartella logs, e lanciare lo script di analisi per identificare potenziali attività di click fraud.

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## ⚠️ Disclaimer

**Utilizzo senza supporto o garanzia**

Questo software viene fornito "così com'è" senza alcuna garanzia di alcun tipo, esplicita o implicita. L'utilizzo di questo script è a rischio dell'utente. Gli autori non forniscono supporto tecnico e non si assumono alcuna responsabilità per eventuali danni diretti, indiretti, incidentali o consequenziali derivanti dall'utilizzo di questo software.

L'utente è responsabile di:
- 🔧 Verificare la compatibilità con il proprio ambiente
- 🧪 Testare il software prima dell'utilizzo in produzione
- 💾 Eseguire backup dei dati prima dell'analisi


## ✍️ Crediti

![Search Foundry](https://github.com/Search-Foundry/seo-tool-skeleton/raw/master/screenshots/SearchFoundryLogo.svg)


- A cura di [Martino Mosna](https://www.martinomosna.com), parte del collettivo [Search Foundry](https://www.searchfoundry.pro)

## Licenza

Questo progetto è distribuito con licenza [MIT](LICENSE).

---
© 2025 Martino Mosna - Founding member of Search Foundry

Made with ❤️ and 🤖

Questo progetto è rilasciato a scopo didattico e sperimentale.

Se ti è stato utile, lascia una ⭐️ su GitHub!
