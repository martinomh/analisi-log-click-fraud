import os
import sys

# Ottieni il nome del cliente/dominio dalla riga di comando o usa un valore predefinito
if len(sys.argv) > 1:
    CLIENTE = sys.argv[1]
else:
    CLIENTE = "example.com"  # Cliente/dominio predefinito

# Percorsi base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENTI_DIR = os.path.join(BASE_DIR, "clienti")
GEOIP_DIR = os.path.join(BASE_DIR, "geoip")

# Assicurati che le cartelle base esistano
os.makedirs(CLIENTI_DIR, exist_ok=True)
os.makedirs(GEOIP_DIR, exist_ok=True)

# Configurazione generale
GEOIP_DB = os.path.join(GEOIP_DIR, "GeoLite2-Country.mmdb")

# Assicurati che la cartella del cliente esista
CLIENTE_DIR = os.path.join(CLIENTI_DIR, CLIENTE)
LOGS_DIR = os.path.join(CLIENTE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Trova automaticamente il primo file ZIP nella cartella logs del cliente
def trova_zip():
    if os.path.exists(LOGS_DIR):
        for file in os.listdir(LOGS_DIR):
            if file.endswith(('.zip', '.gz', '.bz2')):
                return os.path.join(LOGS_DIR, file)
    return None

# Configurazione del dominio da analizzare
DOMAIN = {
    "zip_file": trova_zip() or os.path.join(LOGS_DIR, "logs.zip"),  # Trova automaticamente il file ZIP o usa un nome predefinito
    "output_file": os.path.join(CLIENTE_DIR, "risultati.txt"),  # File di output per i risultati
    "stats_file": os.path.join(CLIENTE_DIR, "stats.csv"),  # File di output per le statistiche
    "domain_name": CLIENTE,  # Il nome del dominio è lo stesso nome della cartella
    "zip_structure": "flat_gz"  # Tipo di struttura: nested_zip, flat_gz, flat_bz2, flat_log, directory
}

# Pattern di ricerca
SEARCH_PATTERN = r'gclid=[^&\s]+'  # Pattern regex per cercare gclid 