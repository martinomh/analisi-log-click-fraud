#!/usr/bin/env python3
import os
import argparse
import tarfile
import glob

def setup_geoip_database():
    """Configura il database GeoIP estraendolo dall'archivio se necessario"""
    geoip_dir = "geoip"
    mmdb_file = os.path.join(geoip_dir, "GeoLite2-Country.mmdb")
    tar_file = os.path.join(geoip_dir, "GeoLite2-Country_*.tar.gz")
    
    # Controlla se il database è già presente
    if os.path.exists(mmdb_file):
        print("✓ Database GeoIP già configurato")
        return True
    
    # Cerca il file tar.gz
    tar_files = glob.glob(tar_file)
    if not tar_files:
        print("✗ Errore: File GeoLite2-Country_*.tar.gz non trovato nella cartella geoip/")
        print("  Scarica il database da: https://dev.maxmind.com/geoip/geoip2/geolite2/")
        return False
    
    tar_path = tar_files[0]  # Prendi il primo file trovato
    print(f"📦 Estraendo database GeoIP da {os.path.basename(tar_path)}...")
    
    try:
        with tarfile.open(tar_path, 'r:gz') as tar:
            # Cerca il file .mmdb nell'archivio
            mmdb_member = None
            for member in tar.getmembers():
                if member.name.endswith('GeoLite2-Country.mmdb'):
                    mmdb_member = member
                    break
            
            if mmdb_member:
                # Estrai il file
                tar.extract(mmdb_member, geoip_dir)
                # Rinomina il file estratto
                extracted_path = os.path.join(geoip_dir, mmdb_member.name)
                if os.path.exists(extracted_path) and extracted_path != mmdb_file:
                    os.rename(extracted_path, mmdb_file)
                
                # Pulisci la cartella temporanea se vuota
                temp_dir = os.path.dirname(mmdb_member.name)
                if temp_dir and temp_dir != '.':
                    temp_dir_path = os.path.join(geoip_dir, temp_dir)
                    try:
                        if os.path.exists(temp_dir_path) and not os.listdir(temp_dir_path):
                            os.rmdir(temp_dir_path)
                    except:
                        pass  # Ignora errori nella pulizia
                
                print("✓ Database GeoIP configurato con successo")
                return True
            else:
                print("✗ Errore: File .mmdb non trovato nell'archivio")
                return False
                
    except Exception as e:
        print(f"✗ Errore durante l'estrazione: {str(e)}")
        return False

def create_domain(dominio):
    """Crea la struttura delle cartelle per un nuovo dominio"""
    dominio_dir = os.path.join("clienti", dominio)
    logs_dir = os.path.join(dominio_dir, "logs")
    
    os.makedirs(logs_dir, exist_ok=True)
    
    print(f"✓ Dominio '{dominio}' creato con successo!")
    print("\nPassaggi successivi:")
    print(f"1. Posiziona il file ZIP dei log in 'clienti/{dominio}/logs/'")
    print(f"2. Esegui 'python run_analysis.py {dominio}' per avviare l'analisi")

def main():
    parser = argparse.ArgumentParser(description='Setup del Log Analyzer e creazione di nuovi domini.')
    parser.add_argument('dominio', nargs='?', help='Nome del dominio da analizzare (es. example.com)')
    parser.add_argument('--geoip-only', action='store_true', help='Configura solo il database GeoIP')
    args = parser.parse_args()
    
    print("🔧 Setup Log Analyzer")
    print("=" * 30)
    
    # Setup del database GeoIP
    if not setup_geoip_database():
        print("\n❌ Setup del database GeoIP fallito. Impossibile continuare.")
        return
    
    # Se richiesto solo il setup GeoIP, termina qui
    if args.geoip_only:
        print("\n✅ Setup completato!")
        return
    
    # Se non è specificato un dominio, mostra istruzioni
    if not args.dominio:
        print("\n📋 Per creare un nuovo dominio:")
        print("   python setup.py example.com")
        print("\n📋 Per configurare solo il database GeoIP:")
        print("   python setup.py --geoip-only")
        return
    
    # Crea il dominio
    print(f"\n🌐 Configurazione dominio: {args.dominio}")
    print("-" * 30)
    create_domain(args.dominio)
    
    print("\n✅ Setup completato!")

if __name__ == "__main__":
    main() 