import re
import geoip2.database
import geoip2.errors
from urllib.parse import urlparse
from datetime import datetime
import os
import sys

# Aggiungi la directory principale al path per importare i moduli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.archive_handler import ArchiveHandler
from config.config import GEOIP_DB, DOMAIN, SEARCH_PATTERN, CLIENTE

# Compilazione del pattern regex
search_pattern = re.compile(SEARCH_PATTERN)

# Contatori
total_lines = 0
pattern_matches = 0
non_italian_matches = 0

def get_country_code(reader, ip):
    """Determina il codice paese di un IP."""
    try:
        response = reader.country(ip)
        return response.country.iso_code
    except geoip2.errors.AddressNotFoundError:
        return None
    except Exception as e:
        print(f"Errore nel processare l'IP {ip}: {str(e)}")
        return None

def is_external_referrer(line, domain_name):
    """Verifica se il referrer è vuoto o esterno al dominio specificato"""
    try:
        # Il referrer è tipicamente il campo 11 in un log Apache
        parts = line.split('"')
        if len(parts) < 4:  # Verifica che ci siano abbastanza parti
            return False
        
        referrer = parts[3]
        if referrer == '-' or referrer == '':  # Referrer vuoto
            return True
            
        # Verifica se il referrer è esterno
        if domain_name:
            parsed = urlparse(referrer)
            return domain_name not in parsed.netloc
        return True  # Se non è specificato un dominio, considera tutti i referrer
    except Exception as e:
        print(f"Errore nell'analisi del referrer: {str(e)}")
        return False

def analyze_log_content(log_content, output_file, reader, domain_name):
    """Analizza il contenuto di un file di log"""
    global total_lines, pattern_matches, non_italian_matches
    
    with open(output_file, 'a', encoding='utf-8') as out:
        for line in log_content.splitlines():
            total_lines += 1
            
            # Verifica se la riga corrisponde al pattern e ha un referrer esterno
            if search_pattern.search(line) and is_external_referrer(line, domain_name):
                pattern_matches += 1
                
                # Estrai l'IP (assumendo che sia il primo "token" della riga)
                tokens = line.split()
                if len(tokens) > 0:
                    ip = tokens[0]
                    country = get_country_code(reader, ip)
                    
                    # Filtra gli IP non italiani
                    if country and country != "IT":
                        non_italian_matches += 1
                        out.write(f"{line}\n")

def process_log_file(name, content):
    """Callback per processare ogni file di log"""
    print(f"Analisi del file {name}...")
    with geoip2.database.Reader(GEOIP_DB) as reader:
        analyze_log_content(content, DOMAIN["output_file"], reader, DOMAIN["domain_name"])

def main():
    """Funzione principale"""
    global total_lines, pattern_matches, non_italian_matches
    
    print(f"Inizio analisi dei log per il dominio: {CLIENTE}")
    start_time = datetime.now()
    
    # Verifica se il file ZIP esiste
    if not DOMAIN["zip_file"] or not os.path.exists(DOMAIN["zip_file"]):
        print(f"Errore: File ZIP non trovato in {DOMAIN['zip_file']}")
        print(f"Assicurati di aver messo il file ZIP nella cartella clienti/{CLIENTE}/logs/")
        return
    
    # Assicurati che la directory di output esista
    os.makedirs(os.path.dirname(DOMAIN["output_file"]), exist_ok=True)
    
    # Assicurati che il file di output sia vuoto all'inizio
    with open(DOMAIN["output_file"], 'w') as f:
        pass
    
    # Inizializza il gestore degli archivi
    archive_handler = ArchiveHandler(
        zip_file=DOMAIN["zip_file"],
        structure_type=DOMAIN["zip_structure"]
    )
    
    try:
        # Processa l'archivio
        archive_handler.process_archive(process_log_file)
        
        # Stampa le statistiche
        print("\nAnalisi completata!")
        print(f"Righe totali processate: {total_lines:,}")
        print(f"Match con il pattern: {pattern_matches:,}")
        print(f"Match non italiani: {non_italian_matches:,}")
        print(f"Risultati salvati in: {DOMAIN['output_file']}")
        
    except Exception as e:
        print(f"Errore durante l'elaborazione: {str(e)}")
    finally:
        print(f"Tempo totale: {datetime.now() - start_time}")

if __name__ == "__main__":
    main() 