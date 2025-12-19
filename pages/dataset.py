"""
MANAJEMEN DATASET
Halaman untuk mengelola dataset CSV (upload, buat, lihat).
"""

import os
import pandas as pd
from utils import Colors, print_menu, get_user_choice, print_success, print_error, print_table, print_warning, print_info
from database import DatasetManager

class DatasetPage:
    """
    Halaman untuk manajemen dataset.
    Mendukung upload, pembuatan, dan penampilan dataset.
    """
    
    def __init__(self, app):
        """
        Inisialisasi halaman manajemen dataset.
        
        Args:
            app: Instance aplikasi utama
        """
        self.app = app
        self.dataset_manager = app.dataset_manager
    
    def display(self):
        """Tampilkan halaman manajemen dataset"""
        print(f"\n{Colors.BOLD}📁 MANAJEMEN DATASET{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Kelola dataset CSV untuk analisis batch{Colors.ENDC}\n")
        
        # Tampilkan dataset yang aktif
        self._display_active_dataset()
        
        # Tampilkan menu MANUAL tanpa menggunakan print_menu
        print(f"{Colors.BOLD}┌─ OPSI DATASET ──────────────────────────────────────┐{Colors.ENDC}")
        print(f"{Colors.OKBLUE}│ 1. Upload Dataset CSV{Colors.ENDC}")
        print(f"{Colors.OKBLUE}│ 2. Buat Dataset Baru{Colors.ENDC}")
        print(f"{Colors.OKBLUE}│ 3. Buat Template Dataset{Colors.ENDC}")
        print(f"{Colors.OKBLUE}│ 4. Lihat Dataset Tersedia{Colors.ENDC}")
        print(f"{Colors.OKBLUE}│ 5. Hapus Dataset{Colors.ENDC}")
        print(f"{Colors.OKBLUE}│ 6. Informasi Dataset{Colors.ENDC}")
        print(f"{Colors.OKBLUE}│ 7. Kembali ke Menu Utama{Colors.ENDC}")
        print(f"{Colors.WARNING}│ 99. Keluar Aplikasi{Colors.ENDC}")
        print(f"{Colors.BOLD}└─────────────────────────────────────────────────────┘{Colors.ENDC}")
    
    def get_input(self):
        """Dapatkan input dari pengguna"""
        try:
            choice_input = input(f"\n{Colors.OKCYAN}Pilih opsi (1-7): {Colors.ENDC}").strip()
            
            if choice_input == '99':
                return "exit"
            
            choice = int(choice_input)
            
            if 1 <= choice <= 7:
                if choice == 1:
                    self._upload_dataset()
                elif choice == 2:
                    self._create_dataset()
                elif choice == 3:
                    self._create_template()
                elif choice == 4:
                    self._list_datasets()
                elif choice == 5:
                    self._delete_dataset()
                elif choice == 6:
                    self._show_dataset_info()
                elif choice == 7:
                    return "home"
            else:
                print_error(f"Pilihan tidak valid! Silakan pilih 1-7.")
        except ValueError:
            print_error("Input harus berupa angka!")
        
        return "dataset"
    
    def _display_active_dataset(self):
        """Tampilkan dataset yang sedang aktif"""
        active_dataset = self.dataset_manager.get_active_dataset()
        
        if active_dataset:
            print(f"{Colors.BOLD}📂 DATASET AKTIF:{Colors.ENDC}")
            print(f"  Nama: {Colors.OKBLUE}{active_dataset['filename']}{Colors.ENDC}")
            print(f"  Ukuran: {active_dataset['size']} baris")
            print(f"  Dimuat pada: {active_dataset['loaded_at']}")
            print()
        else:
            print_warning("Tidak ada dataset yang aktif. Silakan upload atau buat dataset.")
            print()
    
    def _upload_dataset(self):
        """Upload dataset dari file CSV"""
        print(f"\n{Colors.BOLD}📤 UPLOAD DATASET CSV{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Format yang didukung: CSV dengan kolom 'url' dan 'label'{Colors.ENDC}\n")
        
        # Tampilkan dataset yang tersedia
        available_datasets = self.dataset_manager.list_datasets()
        
        if available_datasets:
            print(f"{Colors.BOLD}Dataset yang tersedia:{Colors.ENDC}")
            for i, dataset in enumerate(available_datasets, 1):
                print(f"  {i}. {dataset}")
            print()
        
        print(f"{Colors.WARNING}Petunjuk:{Colors.ENDC}")
        print(f"  1. Letakkan file CSV di folder 'datasets/'")
        print(f"  2. Masukkan nama file (contoh: phishing_data.csv)")
        print(f"  3. Tekan Enter untuk memuat\n")
        
        filename = input(f"{Colors.OKBLUE}Nama file CSV: {Colors.ENDC}").strip()
        
        if not filename:
            print_error("Nama file tidak boleh kosong!")
            return
        
        # Tambahkan ekstensi .csv jika tidak ada
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Cek apakah file ada
        filepath = os.path.join("datasets", filename)
        if not os.path.exists(filepath):
            print_error(f"File '{filename}' tidak ditemukan di folder 'datasets/'!")
            return
        
        # Load dataset
        print(f"\n{Colors.OKCYAN}🔄 Memuat dataset...{Colors.ENDC}")
        df = self.dataset_manager.load_dataset(filename)
        
        if df is not None:
            print_success(f"Dataset '{filename}' berhasil dimuat!")
            
            # Tampilkan preview
            print(f"\n{Colors.BOLD}📋 PREVIEW DATASET (5 baris pertama):{Colors.ENDC}")
            print(df.head().to_string())
            print()
            
            # Tampilkan statistik menggunakan method baru
            stats = self._calculate_dataset_stats(df, filename)
            self._display_dataset_stats(stats)
        
        else:
            print_error(f"Gagal memuat dataset '{filename}'!")
    
    def _calculate_dataset_stats(self, df, filename):
        """Hitung statistik dataset secara lokal"""
        stats = {
            'filename': filename,
            'total_rows': len(df),
            'columns': df.columns.tolist(),
            'phishing_count': 0,
            'legitimate_count': 0,
            'unknown_count': 0,
            'avg_url_length': 0,
            'max_url_length': 0,
            'min_url_length': 0
        }
        
        # Hitung statistik label
        if 'label' in df.columns:
            for label in df['label']:
                label_str = str(label).lower()
                if 'phishing' in label_str:
                    stats['phishing_count'] += 1
                elif 'legitimate' in label_str or 'benign' in label_str or 'good' in label_str:
                    stats['legitimate_count'] += 1
                else:
                    stats['unknown_count'] += 1
        else:
            stats['unknown_count'] = len(df)
        
        # Hitung statistik panjang URL
        if 'url' in df.columns:
            url_lengths = df['url'].str.len()
            stats['avg_url_length'] = url_lengths.mean() if len(url_lengths) > 0 else 0
            stats['max_url_length'] = url_lengths.max() if len(url_lengths) > 0 else 0
            stats['min_url_length'] = url_lengths.min() if len(url_lengths) > 0 else 0
        
        return stats
    
    def _display_dataset_stats(self, stats):
        """Tampilkan statistik dataset"""
        print(f"\n{Colors.BOLD}📊 STATISTIK DATASET:{Colors.ENDC}")
        print(f"  Total baris: {stats['total_rows']}")
        print(f"  Kolom: {', '.join(stats['columns'])}")
        
        if 'label' in stats['columns']:
            print(f"  Phishing: {stats['phishing_count']} ({stats['phishing_count']/stats['total_rows']*100:.1f}%)")
            print(f"  Legitimate: {stats['legitimate_count']} ({stats['legitimate_count']/stats['total_rows']*100:.1f}%)")
            print(f"  Tidak diketahui: {stats['unknown_count']} ({stats['unknown_count']/stats['total_rows']*100:.1f}%)")
        else:
            print(f"  Semua URL: {stats['total_rows']} (label tidak tersedia)")
        
        if stats['avg_url_length'] > 0:
            print(f"\n{Colors.BOLD}📏 STATISTIK PANJANG URL:{Colors.ENDC}")
            print(f"  Rata-rata: {stats['avg_url_length']:.1f} karakter")
            print(f"  Maksimum: {stats['max_url_length']} karakter")
            print(f"  Minimum: {stats['min_url_length']} karakter")
    
    def _create_dataset(self):
        """Buat dataset baru secara manual"""
        print(f"\n{Colors.BOLD}🆕 BUAT DATASET BARU{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Buat dataset CSV dengan memasukkan URL satu per satu{Colors.ENDC}\n")
        
        filename = input(f"{Colors.OKBLUE}Nama file untuk dataset baru: {Colors.ENDC}").strip()
        
        if not filename:
            print_error("Nama file tidak boleh kosong!")
            return
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        print(f"\n{Colors.WARNING}Format: Masukkan URL dan label (phishing/legitimate){Colors.ENDC}")
        print(f"Ketik 'selesai' untuk menyelesaikan, 'batal' untuk membatalkan\n")
        
        data = []
        url_count = 0
        
        while True:
            print(f"\n{Colors.BOLD}Entri ke-{url_count + 1}{Colors.ENDC}")
            url = input(f"{Colors.OKBLUE}URL: {Colors.ENDC}").strip()
            
            if url.lower() == 'selesai':
                break
            elif url.lower() == 'batal':
                print_warning("Pembuatan dataset dibatalkan!")
                return
            
            if not url:
                print_error("URL tidak boleh kosong!")
                continue
            
            label = input(f"{Colors.OKBLUE}Label (phishing/legitimate): {Colors.ENDC}").strip().lower()
            
            if label not in ['phishing', 'legitimate']:
                print_warning("Label harus 'phishing' atau 'legitimate'. Menggunakan 'unknown'")
                label = 'unknown'
            
            data.append({'url': url, 'label': label})
            url_count += 1
        
        if url_count == 0:
            print_error("Dataset kosong! Tidak ada yang disimpan.")
            return
        
        # Simpan dataset
        success = self.dataset_manager.create_dataset(filename, data)
        
        if success:
            print_success(f"Dataset '{filename}' berhasil dibuat dengan {url_count} URL!")
        else:
            print_error("Gagal membuat dataset!")
    
    def _create_template(self):
        """Buat template dataset"""
        print(f"\n{Colors.BOLD}📝 BUAT TEMPLATE DATASET{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Membuat template dataset dengan contoh URL{Colors.ENDC}\n")
        
        success = self.dataset_manager.create_template()
        
        if success:
            print_success("Template dataset berhasil dibuat!")
            print(f"\n{Colors.WARNING}File template tersedia di folder 'datasets/'")
            print("Anda dapat mengedit file ini dan menguploadnya kembali.")
        else:
            print_error("Gagal membuat template dataset!")
    
    def _list_datasets(self):
        """Tampilkan semua dataset yang tersedia"""
        print(f"\n{Colors.BOLD}📋 DAFTAR DATASET{Colors.ENDC}")
        
        datasets = self.dataset_manager.list_datasets()
        
        if not datasets:
            print_warning("Tidak ada dataset yang tersedia di folder 'datasets/'")
            return
        
        # Tampilkan dalam tabel
        headers = ["No", "Nama File", "Ukuran", "Status"]
        rows = []
        
        for i, dataset in enumerate(datasets, 1):
            filepath = os.path.join("datasets", dataset)
            
            # Dapatkan ukuran file
            try:
                size_bytes = os.path.getsize(filepath)
                size_str = self._format_file_size(size_bytes)
            except:
                size_str = "Unknown"
            
            # Tentukan status
            active_dataset = self.dataset_manager.get_active_dataset()
            if active_dataset and dataset == active_dataset['filename']:
                status = f"{Colors.OKGREEN}Aktif{Colors.ENDC}"
            else:
                status = "Tersedia"
            
            rows.append([str(i), dataset, size_str, status])
        
        print_table(headers, rows, "Dataset Tersedia")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
    
    def _delete_dataset(self):
        """Hapus dataset"""
        print(f"\n{Colors.BOLD}🗑️  HAPUS DATASET{Colors.ENDC}")
        
        datasets = self.dataset_manager.list_datasets()
        
        if not datasets:
            print_warning("Tidak ada dataset yang tersedia!")
            return
        
        # Tampilkan dataset
        print(f"{Colors.BOLD}Dataset yang tersedia:{Colors.ENDC}")
        for i, dataset in enumerate(datasets, 1):
            print(f"  {i}. {dataset}")
        
        print(f"\n{Colors.FAIL}⚠ PERINGATAN: Penghapusan tidak dapat dibatalkan!{Colors.ENDC}")
        choice = input(f"\n{Colors.OKBLUE}Pilih dataset yang akan dihapus (0 untuk batal): {Colors.ENDC}").strip()
        
        if choice == '0':
            print_warning("Penghapusan dibatalkan!")
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(datasets):
                filename = datasets[idx]
                
                # Konfirmasi
                confirm = input(f"{Colors.FAIL}Yakin ingin menghapus '{filename}'? (y/n): {Colors.ENDC}").strip().lower()
                
                if confirm == 'y':
                    filepath = os.path.join("datasets", filename)
                    
                    if os.path.exists(filepath):
                        # Hapus dari cache jika ada
                        if filename in self.dataset_manager.datasets:
                            del self.dataset_manager.datasets[filename]
                        
                        # Hapus file
                        os.remove(filepath)
                        
                        print_success(f"Dataset '{filename}' berhasil dihapus!")
                    else:
                        print_error("File tidak ditemukan!")
                else:
                    print_warning("Penghapusan dibatalkan!")
            else:
                print_error("Pilihan tidak valid!")
        except ValueError:
            print_error("Masukkan angka yang valid!")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
    
    def _show_dataset_info(self):
        """Tampilkan informasi detail dataset"""
        active_dataset = self.dataset_manager.get_active_dataset()
        
        if not active_dataset:
            print_warning("Tidak ada dataset yang aktif!")
            input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}📊 INFORMASI DATASET LENGKAP{Colors.ENDC}")
        print(f"Dataset: {active_dataset['filename']}")
        print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")
        
        df = active_dataset['data']
        
        # Hitung statistik lokal
        stats = self._calculate_dataset_stats(df, active_dataset['filename'])
        
        # Tampilkan informasi lengkap
        print(f"\n{Colors.BOLD}📋 INFORMASI UMUM:{Colors.ENDC}")
        print(f"  Nama File: {stats['filename']}")
        print(f"  Total Baris: {stats['total_rows']}")
        print(f"  Total Kolom: {len(stats['columns'])}")
        print(f"  Kolom: {', '.join(stats['columns'])}")
        
        # Distribusi label
        print(f"\n{Colors.BOLD}🎯 DISTRIBUSI LABEL:{Colors.ENDC}")
        if 'label' in stats['columns']:
            print(f"  Phishing: {stats['phishing_count']} ({stats['phishing_count']/stats['total_rows']*100:.1f}%)")
            print(f"  Legitimate: {stats['legitimate_count']} ({stats['legitimate_count']/stats['total_rows']*100:.1f}%)")
            print(f"  Tidak diketahui: {stats['unknown_count']} ({stats['unknown_count']/stats['total_rows']*100:.1f}%)")
            
            # Tampilkan nilai label unik
            unique_labels = df['label'].unique()[:5]
            print(f"  Label unik: {', '.join([str(l) for l in unique_labels])}")
            if len(df['label'].unique()) > 5:
                print(f"             ... dan {len(df['label'].unique()) - 5} lainnya")
        else:
            print(f"  {Colors.WARNING}⚠ Dataset tidak memiliki kolom 'label'{Colors.ENDC}")
        
        # Statistik URL
        print(f"\n{Colors.BOLD}🔗 ANALISIS URL:{Colors.ENDC}")
        if 'url' in stats['columns']:
            print(f"  Panjang rata-rata: {stats['avg_url_length']:.1f} karakter")
            print(f"  Panjang minimum: {stats['min_url_length']} karakter")
            print(f"  Panjang maksimum: {stats['max_url_length']} karakter")
            
            # Analisis protocol
            https_count = df['url'].str.startswith('https://', na=False).sum()
            http_count = df['url'].str.startswith('http://', na=False).sum()
            no_protocol = len(df) - https_count - http_count
            
            print(f"\n  HTTPS: {https_count} ({https_count/len(df)*100:.1f}%)")
            print(f"  HTTP: {http_count} ({http_count/len(df)*100:.1f}%)")
            print(f"  Tanpa protocol: {no_protocol} ({no_protocol/len(df)*100:.1f}%)")
        else:
            print(f"  {Colors.WARNING}⚠ Dataset tidak memiliki kolom 'url'{Colors.ENDC}")
        
        # Tampilkan preview
        print(f"\n{Colors.BOLD}👁️  PREVIEW DATA (3 baris pertama):{Colors.ENDC}")
        print(f"{'-'*80}")
        
        if len(df) > 0:
            for i in range(min(3, len(df))):
                row = df.iloc[i]
                url = str(row.get('url', 'N/A'))[:60] + "..." if len(str(row.get('url', 'N/A'))) > 60 else str(row.get('url', 'N/A'))
                label = str(row.get('label', 'N/A')) if 'label' in df.columns else 'N/A'
                print(f"{i+1:2d}. {url:<65} [{label}]")
        else:
            print("  Dataset kosong")
        
        print(f"{'-'*80}")
        
        # Tampilkan memori usage
        import sys
        memory_usage = df.memory_usage(deep=True).sum() / 1024  # KB
        print(f"\n{Colors.BOLD}💾 PENGGUNAAN MEMORI:{Colors.ENDC}")
        print(f"  Memory usage: {memory_usage:.1f} KB")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
    
    def _format_file_size(self, size_bytes):
        """Format ukuran file menjadi string yang mudah dibaca"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"