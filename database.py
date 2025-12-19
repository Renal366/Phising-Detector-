"""
MANAJEMEN DATASET - PENYIMPANAN DAN PEMBACAAN
Modul untuk mengelola dataset CSV dan hasil analisis.
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd

class DatasetManager:
    """
    Manajer dataset untuk mengelola file CSV dan hasil analisis.
    """
    
    def __init__(self, data_dir: str = "datasets"):
        """
        Inisialisasi manajer dataset.
        
        Args:
            data_dir: Direktori untuk menyimpan dataset
        """
        self.data_dir = data_dir
        self.results_dir = "results"
        
        # Buat direktori jika belum ada
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Dataset yang sedang aktif
        self.active_dataset = None
        self.datasets = {}
    
    def list_datasets(self) -> List[str]:
        """
        List semua dataset yang tersedia.
        
        Returns:
            List nama file dataset
        """
        datasets = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.csv'):
                datasets.append(file)
        return datasets
    
    def load_dataset(self, filename: str) -> Optional[pd.DataFrame]:
        """
        Load dataset dari file CSV.
        
        Args:
            filename: Nama file dataset
            
        Returns:
            DataFrame berisi dataset atau None jika error
        """
        try:
            filepath = os.path.join(self.data_dir, filename)
            
            # Validasi file
            if not os.path.exists(filepath):
                print(f"File {filename} tidak ditemukan!")
                return None
            
            # Load CSV dengan pandas
            df = pd.read_csv(filepath)
            
            # Validasi kolom yang diperlukan
            if 'url' not in df.columns:
                print("Dataset harus memiliki kolom 'url'!")
                return None
            
            # Simpan sebagai dataset aktif
            self.active_dataset = {
                'filename': filename,
                'data': df,
                'size': len(df),
                'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Cache dataset
            self.datasets[filename] = self.active_dataset
            
            print(f"Dataset '{filename}' berhasil dimuat ({len(df)} baris)")
            return df
            
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            return None
    
    def create_dataset(self, filename: str, data: List[Dict]) -> bool:
        """
        Buat dataset baru dari data.
        
        Args:
            filename: Nama file output
            data: List dictionary berisi data
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            filepath = os.path.join(self.data_dir, filename)
            
            # Validasi data
            if not data:
                print("Data tidak boleh kosong!")
                return False
            
            # Tentukan kolom-kolom
            fieldnames = data[0].keys()
            
            # Tulis ke CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"Dataset berhasil dibuat: {filename}")
            return True
            
        except Exception as e:
            print(f"Error creating dataset: {str(e)}")
            return False
    
    def create_template(self) -> bool:
        """
        Buat template dataset untuk pengguna.
        
        Returns:
            True jika berhasil, False jika gagal
        """
        template_data = [
            {'url': 'https://www.google.com', 'label': 'legitimate'},
            {'url': 'https://www.facebook.com', 'label': 'legitimate'},
            {'url': 'https://www.github.com', 'label': 'legitimate'},
            {'url': 'http://g00gle-login.tk', 'label': 'phishing'},
            {'url': 'http://faceb00k-verify.ml', 'label': 'phishing'},
            {'url': 'https://secure.banking.com', 'label': 'legitimate'},
            {'url': 'http://paypa1-confirm.ga', 'label': 'phishing'},
            {'url': 'https://www.amazon.com', 'label': 'legitimate'},
            {'url': 'http://amaz0n-login.tk', 'label': 'phishing'},
            {'url': 'https://www.reddit.com', 'label': 'legitimate'},
            {'url': 'http://secure-payment.update.cc', 'label': 'phishing'},
            {'url': 'https://docs.python.org', 'label': 'legitimate'}
        ]
        
        filename = f"phishing_dataset_template_{datetime.now().strftime('%Y%m%d')}.csv"
        return self.create_dataset(filename, template_data)
    
    def save_results(self, results: List[Dict], analysis_type: str = "batch") -> str:
        """
        Simpan hasil analisis ke file.
        
        Args:
            results: List dictionary berisi hasil
            analysis_type: Tipe analisis (single/batch)
            
        Returns:
            Path file yang disimpan
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"results_{analysis_type}_{timestamp}"
            
            # Simpan sebagai CSV
            csv_filename = f"{filename}.csv"
            csv_path = os.path.join(self.results_dir, csv_filename)
            
            if results:
                fieldnames = results[0].keys()
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
            
            # Simpan sebagai JSON untuk data lengkap
            json_filename = f"{filename}.json"
            json_path = os.path.join(self.results_dir, json_filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"Hasil disimpan sebagai:")
            print(f"  - CSV: {csv_filename}")
            print(f"  - JSON: {json_filename}")
            
            return csv_path
            
        except Exception as e:
            print(f"Error saving results: {str(e)}")
            return ""
    
    def get_dataset_stats(self, filename: str) -> Dict[str, Any]:
        """
        Dapatkan statistik dataset.
        
        Args:
            filename: Nama file dataset
            
        Returns:
            Dictionary berisi statistik
        """
        try:
            if filename not in self.datasets:
                df = self.load_dataset(filename)
                if df is None:
                    return {}
            
            dataset = self.datasets[filename]['data']
            
            stats = {
                'total_rows': len(dataset),
                'columns': list(dataset.columns),
                'phishing_count': 0,
                'legitimate_count': 0,
                'unknown_count': 0
            }
            
            # Hitung distribusi label jika ada kolom label
            if 'label' in dataset.columns:
                label_counts = dataset['label'].value_counts()
                stats['phishing_count'] = label_counts.get('phishing', 0)
                stats['legitimate_count'] = label_counts.get('legitimate', 0)
                stats['unknown_count'] = len(dataset) - stats['phishing_count'] - stats['legitimate_count']
            
            # Hitung statistik URL
            if 'url' in dataset.columns:
                url_lengths = dataset['url'].apply(len)
                stats['avg_url_length'] = url_lengths.mean()
                stats['max_url_length'] = url_lengths.max()
                stats['min_url_length'] = url_lengths.min()
            
            return stats
            
        except Exception as e:
            print(f"Error getting dataset stats: {str(e)}")
            return {}
    
    def get_active_dataset(self) -> Optional[Dict]:
        """
        Dapatkan dataset yang sedang aktif.
        
        Returns:
            Dataset aktif atau None
        """
        return self.active_dataset
    
    def get_all_datasets(self) -> List[str]:
        """
        Dapatkan semua dataset yang telah dimuat.
        
        Returns:
            List nama dataset
        """
        return list(self.datasets.keys())
    
    def clear_active_dataset(self):
        """Clear dataset yang aktif"""
        self.active_dataset = None