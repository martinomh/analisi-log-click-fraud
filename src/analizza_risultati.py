from collections import defaultdict
from datetime import datetime
from urllib.parse import urlparse
import re
import csv
import geoip2.database
import os
import sys

# Aggiungi la directory principale al path per importare i moduli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import GEOIP_DB, DOMAIN, CLIENTE

def get_domain(referrer):
    """Estrae il dominio dal referrer"""
    try:
        if referrer == '-':
            return 'direct'
        parsed = urlparse(referrer)
        return parsed.netloc or 'unknown'
    except:
        return 'unknown'

def get_gclid(request_url):
    """Estrae il parametro gclid dall'URL della richiesta"""
    try:
        if not request_url or request_url == '-':
            return '-'
        # Estrai solo la parte dell'URL con i parametri
        if '?' in request_url:
            query_string = request_url.split('?')[1].split(' ')[0]
            # Dividi i parametri e crea un dizionario
            params = dict(param.split('=') for param in query_string.split('&'))
            return params.get('gclid', '-')
        return '-'
    except:
        return '-'

def get_country(reader, ip):
    """Ottiene il paese da un IP usando GeoLite2"""
    try:
        response = reader.country(ip)
        return response.country.iso_code or 'Unknown'
    except:
        return 'Unknown'

def main():
    """Funzione principale"""
    print(f"Inizio analisi dei risultati per il dominio: {CLIENTE}")
    start_time = datetime.now()
    
    input_file = DOMAIN["output_file"]
    output_file = DOMAIN["stats_file"]
    
    # Verifica se il file di input esiste
    if not os.path.exists(input_file):
        print(f"Errore: File di input non trovato in {input_file}")
        print("Esegui prima l'analisi dei log con 'python src/analisi_log.py'")
        return
    
    # Assicurati che la directory di output esista
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Lista per memorizzare tutte le righe
    hits = []
    
    # Analisi del file
    with geoip2.database.Reader(GEOIP_DB) as reader:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    # Estrai IP e paese
                    ip = line.split()[0]
                    country = get_country(reader, ip)
                    
                    # Estrai la data
                    date_match = re.search(r'\[(.*?)\]', line)
                    if date_match:
                        date_str = date_match.group(1)
                        try:
                            date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S %z')
                            day = date.strftime('%Y-%m-%d')
                            time = date.strftime('%H:%M:%S')
                        except:
                            day = "unknown"
                            time = "unknown"
                    else:
                        day = "unknown"
                        time = "unknown"
                    
                    # Estrai il referrer e l'URL della richiesta
                    parts = line.split('"')
                    request_url = parts[1].split(' ')[1] if len(parts) > 1 else '-'
                    referrer = parts[3] if len(parts) > 3 else '-'
                    domain = get_domain(referrer)
                    gclid = get_gclid(request_url)  # Usa l'URL della richiesta invece del referrer
                    
                    # Aggiungi la riga ai dati
                    hits.append({
                        'data': day,
                        'paese': country,
                        'referrer': domain,
                        'ip': ip,
                        'ora': time,
                        'gclid': gclid
                    })
                except Exception as e:
                    print(f"Errore nel processare una riga: {str(e)}")
                    continue
    
    # Scrivi i risultati in CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['data', 'ora', 'paese', 'referrer', 'ip', 'gclid'])
        writer.writeheader()
        writer.writerows(hits)
    
    # Statistiche di riepilogo
    total_hits = len(hits)
    unique_days = len(set(hit['data'] for hit in hits))

    countries = defaultdict(int)
    referrers = defaultdict(int)
    
    for hit in hits:
        countries[hit['paese']] += 1
        referrers[hit['referrer']] += 1
    
    print(f"\nStatistiche salvate in {output_file}")
    print(f"Totale hit: {total_hits}")
    print(f"Numero di giorni: {unique_days}")
    print("\nTop 5 paesi:")
    for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{country}: {count} hit")
    print("\nTop 5 referrer:")
    for ref, count in sorted(referrers.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{ref}: {count} hit")
    
    print(f"\nAnalisi completata in: {datetime.now() - start_time}")

if __name__ == "__main__":
    main() 