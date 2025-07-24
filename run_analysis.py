#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Analizza i log per trovare visite non italiane con pattern specifici.')
    parser.add_argument('dominio', nargs='?', help='Nome del dominio da analizzare')
    parser.add_argument('--skip-analysis', action='store_true', help='Salta la fase di analisi dei log')
    parser.add_argument('--skip-stats', action='store_true', help='Salta la fase di generazione delle statistiche')
    parser.add_argument('--zip-structure', choices=['nested_zip', 'flat_gz', 'flat_bz2', 'flat_log', 'directory'],
                        help='Tipo di struttura del file ZIP')
    args = parser.parse_args()
    
    # Costruisci i comandi con gli argomenti appropriati
    analysis_cmd = f"{sys.executable} src/analisi_log.py"
    stats_cmd = f"{sys.executable} src/analizza_risultati.py"
    
    if args.dominio:
        analysis_cmd += f" {args.dominio}"
        stats_cmd += f" {args.dominio}"
    
    start_time = datetime.now()
    print("=== Log Analyzer ===")
    
    if not args.skip_analysis:
        print("\n=== Fase 1: Analisi dei log ===")
        os.system(analysis_cmd)
    
    if not args.skip_stats:
        print("\n=== Fase 2: Generazione delle statistiche ===")
        os.system(stats_cmd)
    
    print(f"\nAnalisi completata in: {datetime.now() - start_time}")

if __name__ == "__main__":
    main() 