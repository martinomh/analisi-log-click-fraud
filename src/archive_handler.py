import zipfile
import io
import bz2
import gzip
import os

class ArchiveHandler:
    """Classe per gestire diversi tipi di archivi compressi"""
    
    def __init__(self, zip_file, structure_type):
        self.zip_file = zip_file
        self.structure_type = structure_type
    
    def process_archive(self, callback):
        """
        Processa l'archivio in base alla sua struttura
        
        Args:
            callback: Funzione da chiamare per ogni file di log estratto
                     La funzione deve accettare (nome_file, contenuto)
        """
        print(f"Processando archivio {self.zip_file} con struttura {self.structure_type}")
        
        if self.structure_type == "nested_zip":
            self._process_nested_zip(callback)
        elif self.structure_type == "flat_gz":
            self._process_flat_gz(callback)
        elif self.structure_type == "flat_bz2":
            self._process_flat_bz2(callback)
        elif self.structure_type == "flat_log":
            self._process_flat_log(callback)
        elif self.structure_type == "directory":
            self._process_directory(callback)
        else:
            raise ValueError(f"Tipo di struttura non supportato: {self.structure_type}")
    
    def _process_nested_zip(self, callback):
        """Processa un archivio ZIP contenente altri file ZIP"""
        with zipfile.ZipFile(self.zip_file, 'r') as main_zip:
            for name in main_zip.namelist():
                # Salta i file nella cartella __MACOSX
                if '__MACOSX' in name:
                    continue
                    
                if name.endswith('.zip'):
                    print(f"Processando ZIP interno: {name}...")
                    
                    # Leggi il file ZIP interno
                    inner_zip_data = io.BytesIO(main_zip.read(name))
                    try:
                        with zipfile.ZipFile(inner_zip_data, 'r') as inner_zip:
                            for log_filename in inner_zip.namelist():
                                if log_filename.endswith(".log"):
                                    print(f"  Processando log: {log_filename}")
                                    log_content = inner_zip.read(log_filename).decode('utf-8', errors='replace')
                                    callback(log_filename, log_content)
                    except Exception as e:
                        print(f"Errore nel processare {name}: {str(e)}")
    
    def _process_flat_gz(self, callback):
        """Processa un archivio ZIP contenente file GZ"""
        with zipfile.ZipFile(self.zip_file, 'r') as zip_file:
            for name in zip_file.namelist():
                if '__MACOSX' in name:
                    continue
                
                if name.endswith('.gz'):
                    print(f"Processando GZ: {name}...")
                    try:
                        gz_data = zip_file.read(name)
                        log_content = gzip.decompress(gz_data).decode('utf-8', errors='replace')
                        callback(name, log_content)
                    except Exception as e:
                        print(f"Errore nel processare {name}: {str(e)}")
    
    def _process_flat_bz2(self, callback):
        """Processa un archivio ZIP contenente file BZ2"""
        with zipfile.ZipFile(self.zip_file, 'r') as zip_file:
            for name in zip_file.namelist():
                if '__MACOSX' in name:
                    continue
                
                if name.endswith('.bz2'):
                    print(f"Processando BZ2: {name}...")
                    try:
                        bz2_data = zip_file.read(name)
                        log_content = bz2.decompress(bz2_data).decode('utf-8', errors='replace')
                        callback(name, log_content)
                    except Exception as e:
                        print(f"Errore nel processare {name}: {str(e)}")
    
    def _process_flat_log(self, callback):
        """Processa un archivio ZIP contenente direttamente file di log"""
        with zipfile.ZipFile(self.zip_file, 'r') as zip_file:
            for name in zip_file.namelist():
                if '__MACOSX' in name:
                    continue
                
                if name.endswith('.log') or name.endswith('.txt'):
                    print(f"Processando log: {name}...")
                    try:
                        log_content = zip_file.read(name).decode('utf-8', errors='replace')
                        callback(name, log_content)
                    except Exception as e:
                        print(f"Errore nel processare {name}: {str(e)}")
    
    def _process_directory(self, callback):
        """Processa una directory contenente file di log"""
        for root, _, files in os.walk(self.zip_file):
            for file in files:
                if file.endswith('.log') or file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    print(f"Processando log: {file_path}...")
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                            log_content = f.read()
                            callback(file_path, log_content)
                    except Exception as e:
                        print(f"Errore nel processare {file_path}: {str(e)}") 