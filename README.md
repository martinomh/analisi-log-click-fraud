# 📊 Log Analyzer

Strumento per l'analisi automatica di file di log web, con supporto per diverse strutture di archiviazione e generazione di statistiche dettagliate.

## ✨ Caratteristiche

- 🔍 Analisi automatica di file di log compressi (GZ, BZ2, ZIP)
- 📦 Supporto per diverse strutture di archiviazione
- 📈 Generazione di statistiche dettagliate
- 🗂️ Struttura organizzata per cliente/dominio
- 🌍 Geocoding degli IP (richiede database GeoIP)

## 🚀 Utilizzo

### 1. ⚙️ Setup iniziale

Prima di tutto, configura il database GeoIP e crea la struttura per un nuovo dominio:

```bash
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

### ⚙️ Opzioni avanzate

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

Tutto ciò che devi fare è creare una cartella con il nome del dominio, mettere il file ZIP nella sottocartella logs, e lanciare lo script di analisi.

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## ⚠️ Disclaimer

**Utilizzo senza supporto o garanzia**

Questo software viene fornito "così com'è" senza alcuna garanzia di alcun tipo, esplicita o implicita. L'utilizzo di questo script è a rischio dell'utente. Gli autori non forniscono supporto tecnico e non si assumono alcuna responsabilità per eventuali danni diretti, indiretti, incidentali o consequenziali derivanti dall'utilizzo di questo software.

L'utente è responsabile di:
- 🔧 Verificare la compatibilità con il proprio ambiente
- 🧪 Testare il software prima dell'utilizzo in produzione
- 💾 Eseguire backup dei dati prima dell'analisi