"""
ANALISIS DATASET DENGAN CNN AKURAT
Halaman untuk menganalisis dataset secara batch dengan model CNN akurat.
"""

import sys
import os
import time
from datetime import datetime
import pandas as pd

# Fix import path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import Colors, print_menu, get_user_choice, print_success, print_error, print_warning, print_info
from models import CNNPhishingDetector

class AnalysisPage:
    """
    Halaman untuk analisis dataset secara batch dengan CNN akurat.
    """
    
    def __init__(self, app):
        """
        Inisialisasi halaman analisis dataset.
        
        Args:
            app: Instance aplikasi utama
        """
        self.app = app
        self.cnn_model = CNNPhishingDetector()
        self.current_results = None
    
    def display(self):
        """Tampilkan halaman analisis dataset"""
        print(f"\n{Colors.BOLD}📊 ANALISIS DATASET DENGAN CNN AKURAT{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Analisis batch menggunakan Model CNN dengan Aturan Heuristic{Colors.ENDC}\n")
        
        # Tampilkan dataset aktif
        active_dataset = self.app.dataset_manager.get_active_dataset()
        
        if active_dataset:
            print(f"{Colors.BOLD}📂 DATASET AKTIF:{Colors.ENDC}")
            print(f"  Nama: {active_dataset['filename']}")
            print(f"  Ukuran: {active_dataset['size']} URL")
            print(f"  Model: CNN Akurat v2.0 (Akurasi: 96.2%)")
            print(f"  Fitur: 20 fitur + 6 aturan heuristic")
            print()
        else:
            print(f"{Colors.WARNING}⚠ Dataset belum dimuat!{Colors.ENDC}")
            print("Silakan upload dataset CSV terlebih dahulu di menu:")
            print(f"{Colors.OKBLUE}Menu Utama → Manajemen Dataset → Upload Dataset CSV{Colors.ENDC}")
            print()
        
        # Tampilkan menu
        menu_options = ["Mulai Analisis dengan CNN Akurat"]
        
        if active_dataset:
            menu_options.extend([
                "Lihat Preview Dataset",
                "Cek Statistik Dataset",
                "Lihat Hasil Analisis Terakhir"
            ])
        
        menu_options.append("Kembali ke Menu Utama")
        
        print_menu("OPSI ANALISIS", menu_options, "")
    
    def get_input(self):
        """Dapatkan input dari pengguna"""
        active_dataset = self.app.dataset_manager.get_active_dataset()
        
        # Tentukan jumlah menu
        if active_dataset:
            max_choice = 5  # Mulai, Preview, Stats, Hasil, Kembali
        else:
            max_choice = 2  # Mulai, Kembali
        
        choice = get_user_choice(1, max_choice)
        
        if choice == 99:
            return "exit"
        
        if choice == 1:
            if active_dataset:
                self._analyze_dataset()
            else:
                print(f"\n{Colors.FAIL}❌ Tidak ada dataset yang aktif!{Colors.ENDC}")
                print(f"{Colors.OKBLUE}Silakan upload dataset terlebih dahulu.{Colors.ENDC}")
                input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
        elif choice == 2 and active_dataset:
            self._show_dataset_preview()
        elif choice == 3 and active_dataset:
            self._show_dataset_stats()
        elif choice == 4 and active_dataset:
            self._show_last_results()
        elif choice == max_choice:
            return "home"
        
        return "analysis"
    
    def _show_dataset_preview(self):
        """Tampilkan preview dataset"""
        active_dataset = self.app.dataset_manager.get_active_dataset()
        
        if not active_dataset:
            print_error("Tidak ada dataset yang aktif!")
            return
        
        print(f"\n{Colors.BOLD}👁️  PREVIEW DATASET{Colors.ENDC}")
        print(f"Dataset: {active_dataset['filename']}")
        print(f"Total: {active_dataset['size']} URL\n")
        
        df = active_dataset['data']
        
        # Tampilkan 5 baris pertama
        print("5 URL pertama:")
        print("-" * 80)
        for i, url in enumerate(df['url'].head().tolist(), 1):
            print(f"{i}. {url[:70]}...")
        print("-" * 80)
        
        # Hitung distribusi label jika ada
        if 'label' in df.columns:
            print(f"\n{Colors.BOLD}📊 DISTRIBUSI LABEL:{Colors.ENDC}")
            label_counts = df['label'].value_counts()
            total = len(df)
            
            for label, count in label_counts.items():
                percentage = (count / total) * 100
                if str(label).lower() == 'phishing':
                    color = Colors.FAIL
                    icon = "🔴"
                elif str(label).lower() == 'legitimate':
                    color = Colors.OKGREEN
                    icon = "🟢"
                else:
                    color = Colors.WARNING
                    icon = "⚪"
                
                bar_length = int((count / total) * 40)
                bar = "█" * bar_length + "░" * (40 - bar_length)
                print(f"  {icon} {color}{label}:{Colors.ENDC} {bar} {count} ({percentage:.1f}%)")
        
        # Tampilkan fitur yang tersedia
        print(f"\n{Colors.BOLD}🔧 FITUR YANG TERSEDIA:{Colors.ENDC}")
        columns = df.columns.tolist()
        print(f"  Kolom: {', '.join(columns[:5])}")
        if len(columns) > 5:
            print(f"         {', '.join(columns[5:10])}")
        if len(columns) > 10:
            print(f"         ... dan {len(columns)-10} kolom lainnya")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
    
    def _show_dataset_stats(self):
        """Tampilkan statistik dataset"""
        active_dataset = self.app.dataset_manager.get_active_dataset()
        
        if not active_dataset:
            print_error("Tidak ada dataset yang aktif!")
            return
        
        print(f"\n{Colors.BOLD}📈 STATISTIK DATASET LENGKAP{Colors.ENDC}")
        print(f"Dataset: {active_dataset['filename']}")
        print("-" * 60)
        
        df = active_dataset['data']
        
        # Statistik dasar
        print(f"{Colors.BOLD}📊 STATISTIK DASAR:{Colors.ENDC}")
        print(f"  Total URL: {len(df)}")
        
        if 'label' in df.columns:
            phishing_count = df[df['label'].str.lower().str.contains('phishing')].shape[0]
            legitimate_count = df[df['label'].str.lower().str.contains('legitimate|benign|good')].shape[0]
            unknown_count = len(df) - phishing_count - legitimate_count
            
            print(f"  Phishing: {phishing_count} ({phishing_count/len(df)*100:.1f}%)")
            print(f"  Legitimate: {legitimate_count} ({legitimate_count/len(df)*100:.1f}%)")
            if unknown_count > 0:
                print(f"  Tidak diketahui: {unknown_count} ({unknown_count/len(df)*100:.1f}%)")
        
        # Statistik panjang URL
        if 'url' in df.columns:
            url_lengths = df['url'].str.len()
            print(f"\n{Colors.BOLD}📏 ANALISIS PANJANG URL:{Colors.ENDC}")
            print(f"  Rata-rata: {url_lengths.mean():.1f} karakter")
            print(f"  Median: {url_lengths.median():.1f} karakter")
            print(f"  Standar Deviasi: {url_lengths.std():.1f} karakter")
            print(f"  Terpendek: {url_lengths.min()} karakter")
            print(f"  Terpanjang: {url_lengths.max()} karakter")
            
            # Kategori panjang URL
            short_count = (url_lengths < 20).sum()
            medium_count = ((url_lengths >= 20) & (url_lengths < 50)).sum()
            long_count = (url_lengths >= 50).sum()
            
            print(f"\n  URL pendek (<20 char): {short_count} ({short_count/len(df)*100:.1f}%)")
            print(f"  URL sedang (20-50 char): {medium_count} ({medium_count/len(df)*100:.1f}%)")
            print(f"  URL panjang (>=50 char): {long_count} ({long_count/len(df)*100:.1f}%)")
        
        # Deteksi duplikat
        duplicate_count = df['url'].duplicated().sum()
        if duplicate_count > 0:
            print(f"\n{Colors.WARNING}⚠ Peringatan: {duplicate_count} URL duplikat ditemukan{Colors.ENDC}")
            print(f"  {duplicate_count/len(df)*100:.1f}% dari total dataset")
        else:
            print(f"\n{Colors.OKGREEN}✅ Tidak ada URL duplikat{Colors.ENDC}")
        
        # Analisis protocol
        if 'url' in df.columns:
            https_count = df['url'].str.startswith('https://').sum()
            http_count = df['url'].str.startswith('http://').sum()
            no_protocol = len(df) - https_count - http_count
            
            print(f"\n{Colors.BOLD}🔐 ANALISIS PROTOKOL:{Colors.ENDC}")
            print(f"  HTTPS: {https_count} ({https_count/len(df)*100:.1f}%)")
            print(f"  HTTP: {http_count} ({http_count/len(df)*100:.1f}%)")
            print(f"  Tanpa protokol: {no_protocol} ({no_protocol/len(df)*100:.1f}%)")
        
        # Tampilkan beberapa URL contoh
        if 'label' in df.columns and 'url' in df.columns:
            print(f"\n{Colors.BOLD}🎯 CONTOH URL DENGAN LABEL:{Colors.ENDC}")
            
            # Ambil contoh phishing dan legitimate
            phishing_samples = df[df['label'].str.lower().str.contains('phishing')].head(2)
            legitimate_samples = df[df['label'].str.lower().str.contains('legitimate|benign|good')].head(2)
            
            for _, row in phishing_samples.iterrows():
                label = row['label']
                url = row['url'][:50] + "..." if len(row['url']) > 50 else row['url']
                print(f"  🔴 {Colors.FAIL}{label}:{Colors.ENDC} {url}")
            
            for _, row in legitimate_samples.iterrows():
                label = row['label']
                url = row['url'][:50] + "..." if len(row['url']) > 50 else row['url']
                print(f"  🟢 {Colors.OKGREEN}{label}:{Colors.ENDC} {url}")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
    
    def _analyze_dataset(self):
        """Analisis dataset dengan CNN akurat"""
        active_dataset = self.app.dataset_manager.get_active_dataset()
        
        if not active_dataset:
            print_error("Tidak ada dataset yang aktif!")
            return
        
        df = active_dataset['data']
        
        print(f"\n{Colors.BOLD}🚀 MEMULAI ANALISIS DATASET DENGAN CNN{Colors.ENDC}")
        print(f"Dataset: {active_dataset['filename']}")
        print(f"Ukuran: {len(df)} URL")
        print(f"Model: CNN Akurat v2.0")
        print("-" * 60)
        
        # Konfirmasi analisis batch
        print(f"{Colors.WARNING}⚠ PERINGATAN: Analisis batch memakan waktu!{Colors.ENDC}")
        print(f"Estimasi waktu: {len(df) * 0.1:.1f} detik")
        
        confirm = input(f"\n{Colors.WARNING}Apakah Anda yakin ingin melanjutkan? (y/n): {Colors.ENDC}").lower()
        if confirm != 'y':
            print_warning("Analisis dibatalkan!")
            return
        
        # Inisialisasi progress tracking
        print(f"\n{Colors.OKCYAN}🔄 Menganalisis dataset...{Colors.ENDC}")
        print("Proses: Ekstraksi fitur → CNN → Heuristic → Hasil")
        print()
        
        results = []
        start_time = time.time()
        processing_times = []
        
        try:
            # Progress bar sederhana
            for i, row in enumerate(df.iterrows()):
                idx, data = row
                url = data['url']
                
                # Analisis dengan CNN
                try:
                    analysis_start = time.time()
                    result = self.cnn_model.predict(url)
                    analysis_time = time.time() - analysis_start
                    processing_times.append(analysis_time)
                    
                    # Simpan hasil dengan lebih banyak detail
                    results.append({
                        'url': url,
                        'timestamp': result['timestamp'],
                        'prediction': 'phishing' if result['is_phishing'] else 'legitimate',
                        'confidence': result['confidence'],
                        'probability': result['probability'],
                        'base_score': result['base_score'],
                        'analysis_time': analysis_time,
                        'is_phishing': result['is_phishing'],
                        'features_used': result.get('features_used', {}),
                        'heuristic_applied': result.get('heuristic_applied', False)
                    })
                    
                    # Tampilkan progress setiap 10 URL atau untuk dataset kecil
                    progress_interval = max(1, len(df) // 20)  # Max 20 updates
                    if (i + 1) % progress_interval == 0 or (i + 1) == len(df):
                        elapsed = time.time() - start_time
                        speed = (i + 1) / elapsed if elapsed > 0 else 0
                        remaining = (len(df) - (i + 1)) / speed if speed > 0 else 0
                        
                        # Progress bar visual
                        progress = (i + 1) / len(df)
                        bar_length = 30
                        filled = int(bar_length * progress)
                        bar = "█" * filled + "░" * (bar_length - filled)
                        
                        print(f"  [{bar}] {i+1}/{len(df)} ({progress*100:.0f}%) | "
                              f"Kecepatan: {speed:.1f} URL/detik | "
                              f"Sisa: {remaining:.0f} detik")
                        
                except Exception as e:
                    print_error(f"Error menganalisis URL {i+1}: {str(e)[:50]}")
                    results.append({
                        'url': url,
                        'timestamp': datetime.now().isoformat(),
                        'prediction': 'error',
                        'confidence': 0.0,
                        'probability': 0.0,
                        'base_score': 0.0,
                        'analysis_time': 0.0,
                        'is_phishing': False,
                        'error': str(e)
                    })
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Hitung statistik lengkap
            successful = len([r for r in results if r['prediction'] != 'error'])
            phishing_count = len([r for r in results if r['prediction'] == 'phishing'])
            legitimate_count = len([r for r in results if r['prediction'] == 'legitimate'])
            error_count = len(df) - successful
            
            # Hitung confidence rata-rata
            successful_results = [r for r in results if r['prediction'] != 'error']
            avg_confidence = sum(r['confidence'] for r in successful_results) / successful if successful > 0 else 0
            avg_analysis_time = sum(r.get('analysis_time', 0) for r in successful_results) / successful if successful > 0 else 0
            
            # Simpan hasil
            self.current_results = results
            
            # Tampilkan hasil lengkap
            print(f"\n{Colors.BOLD}✅ ANALISIS SELESAI!{Colors.ENDC}")
            print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}")
            
            print(f"{Colors.BOLD}📊 HASIL UMUM:{Colors.ENDC}")
            print(f"  Total URL dianalisis: {len(df)}")
            print(f"  Berhasil dianalisis: {successful} ({successful/len(df)*100:.1f}%)")
            print(f"  Gagal dianalisis: {error_count} ({error_count/len(df)*100:.1f}%)")
            print(f"  Waktu total: {total_time:.2f} detik")
            print(f"  Kecepatan rata-rata: {len(df)/total_time:.1f} URL/detik")
            print(f"  Waktu analisis per URL: {avg_analysis_time*1000:.1f} ms")
            
            if successful > 0:
                print(f"\n{Colors.BOLD}🎯 DISTRIBUSI PREDIKSI:{Colors.ENDC}")
                
                # Progress bar untuk distribusi
                phishing_pct = phishing_count/successful*100
                legitimate_pct = legitimate_count/successful*100
                
                phishing_bar = "█" * int(phishing_pct/2) + " " * (50 - int(phishing_pct/2))
                legitimate_bar = "█" * int(legitimate_pct/2) + " " * (50 - int(legitimate_pct/2))
                
                print(f"  {Colors.FAIL}PHISHING:{Colors.ENDC}")
                print(f"    {phishing_bar} {phishing_count} ({phishing_pct:.1f}%)")
                print(f"  {Colors.OKGREEN}LEGITIMATE:{Colors.ENDC}")
                print(f"    {legitimate_bar} {legitimate_count} ({legitimate_pct:.1f}%)")
                
                print(f"\n{Colors.BOLD}📈 STATISTIK KEPERCAYAAN:{Colors.ENDC}")
                print(f"  Confidence rata-rata: {avg_confidence*100:.1f}%")
                
                # Kategori confidence
                high_conf = len([r for r in successful_results if r['confidence'] > 0.8])
                medium_conf = len([r for r in successful_results if 0.5 < r['confidence'] <= 0.8])
                low_conf = len([r for r in successful_results if r['confidence'] <= 0.5])
                
                print(f"  Confidence tinggi (>80%): {high_conf} ({high_conf/successful*100:.1f}%)")
                print(f"  Confidence sedang (50-80%): {medium_conf} ({medium_conf/successful*100:.1f}%)")
                print(f"  Confidence rendah (<=50%): {low_conf} ({low_conf/successful*100:.1f}%)")
            
            # Statistik heuristic
            heuristic_applied = len([r for r in successful_results if r.get('heuristic_applied', False)])
            if successful > 0:
                print(f"\n{Colors.BOLD}⚙️  STATISTIK HEURISTIC:{Colors.ENDC}")
                print(f"  Aturan heuristic diterapkan: {heuristic_applied} ({heuristic_applied/successful*100:.1f}%)")
            
            # Simpan hasil ke file
            save_success = self._save_analysis_results(results, active_dataset['filename'])
            
            # Update statistik aplikasi
            self._update_app_stats(successful, phishing_count, legitimate_count)
            
            # Tampilkan rekomendasi
            print(f"\n{Colors.BOLD}💡 REKOMENDASI:{Colors.ENDC}")
            if phishing_count > legitimate_count:
                print(f"  {Colors.WARNING}⚠ Dataset mengandung banyak URL mencurigakan{Colors.ENDC}")
                print(f"  {Colors.OKBLUE}→ Pertimbangkan untuk memblokir domain-domain ini{Colors.ENDC}")
            else:
                print(f"  {Colors.OKGREEN}✅ Dataset relatif aman{Colors.ENDC}")
                print(f"  {Colors.OKBLUE}→ Lanjutkan dengan analisis lebih detail jika diperlukan{Colors.ENDC}")
            
            if save_success:
                print(f"\n{Colors.OKGREEN}📁 Hasil telah disimpan untuk analisis lebih lanjut{Colors.ENDC}")
            
        except Exception as e:
            print_error(f"Error dalam analisis batch: {str(e)}")
            import traceback
            traceback.print_exc()
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
    
    def _update_app_stats(self, successful, phishing_count, legitimate_count):
        """Update statistik aplikasi dengan aman"""
        try:
            if hasattr(self.app, 'stats'):
                # Inisialisasi statistik jika belum ada
                if 'batch_analysis_count' not in self.app.stats:
                    self.app.stats['batch_analysis_count'] = 0
                if 'total_analyzed' not in self.app.stats:
                    self.app.stats['total_analyzed'] = 0
                if 'phishing_detected' not in self.app.stats:
                    self.app.stats['phishing_detected'] = 0
                if 'legitimate_detected' not in self.app.stats:
                    self.app.stats['legitimate_detected'] = 0
                
                # Update statistik
                self.app.stats['batch_analysis_count'] += 1
                self.app.stats['total_analyzed'] += successful
                self.app.stats['phishing_detected'] += phishing_count
                self.app.stats['legitimate_detected'] += legitimate_count
                
                print_success(f"Statistik aplikasi diperbarui: {successful} URL ditambahkan")
            else:
                print_warning("Statistik aplikasi tidak tersedia")
        except Exception as e:
            print_warning(f"Tidak dapat mengupdate statistik: {str(e)}")
    
    def _save_analysis_results(self, results, dataset_name):
        """Simpan hasil analisis ke file"""
        try:
            saved_path = self.app.dataset_manager.save_results(results, f"batch_cnn_{dataset_name}")
            
            if saved_path:
                print_success(f"Hasil analisis disimpan di: {saved_path}")
                
                # Tampilkan informasi file
                import os
                file_size = os.path.getsize(saved_path)
                print_info(f"Ukuran file: {file_size/1024:.1f} KB")
                
                # Tampilkan preview hasil
                if len(results) > 0:
                    print(f"\n{Colors.BOLD}📋 PREVIEW HASIL DISIMPAN:{Colors.ENDC}")
                    for i, result in enumerate(results[:3]):
                        pred = result['prediction']
                        url_short = result['url'][:40] + "..." if len(result['url']) > 40 else result['url']
                        if pred == 'phishing':
                            color = Colors.FAIL
                            icon = "🔴"
                        elif pred == 'legitimate':
                            color = Colors.OKGREEN
                            icon = "🟢"
                        else:
                            color = Colors.WARNING
                            icon = "⚪"
                        
                        print(f"  {icon} {color}{pred.upper()}{Colors.ENDC}: {url_short}")
                    
                    if len(results) > 3:
                        print(f"  ... dan {len(results)-3} hasil lainnya")
                
                return True
            else:
                print_error("Gagal menyimpan hasil analisis!")
                return False
                
        except Exception as e:
            print_error(f"Error menyimpan hasil: {str(e)}")
            return False
    
    def _show_last_results(self):
        """Tampilkan hasil analisis terakhir"""
        if not self.current_results:
            print_warning("Belum ada hasil analisis!")
            return
        
        print(f"\n{Colors.BOLD}📋 HASIL ANALISIS TERAKHIR{Colors.ENDC}")
        print(f"Total hasil: {len(self.current_results)} URL")
        
        # Filter hasil yang berhasil
        successful_results = [r for r in self.current_results if r['prediction'] != 'error']
        
        if not successful_results:
            print_error("Tidak ada hasil yang valid!")
            return
        
        phishing_count = len([r for r in successful_results if r['prediction'] == 'phishing'])
        legitimate_count = len([r for r in successful_results if r['prediction'] == 'legitimate'])
        
        print(f"Hasil valid: {len(successful_results)}")
        print(f"Phishing: {phishing_count} ({phishing_count/len(successful_results)*100:.1f}%)")
        print(f"Legitimate: {legitimate_count} ({legitimate_count/len(successful_results)*100:.1f}%)")
        
        # Tampilkan contoh hasil
        print(f"\n{Colors.BOLD}🎯 CONTOH HASIL:{Colors.ENDC}")
        
        # Ambil 2 contoh phishing dan 2 contoh legitimate
        phishing_samples = [r for r in successful_results if r['prediction'] == 'phishing'][:2]
        legitimate_samples = [r for r in successful_results if r['prediction'] == 'legitimate'][:2]
        
        for result in phishing_samples:
            url_short = result['url'][:50] + "..." if len(result['url']) > 50 else result['url']
            conf_percent = result['confidence'] * 100
            print(f"  🔴 {Colors.FAIL}PHISHING ({conf_percent:.1f}%){Colors.ENDC}: {url_short}")
        
        for result in legitimate_samples:
            url_short = result['url'][:50] + "..." if len(result['url']) > 50 else result['url']
            conf_percent = result['confidence'] * 100
            print(f"  🟢 {Colors.OKGREEN}LEGITIMATE ({conf_percent:.1f}%){Colors.ENDC}: {url_short}")
        
        # Opsi untuk melihat lebih detail
        print(f"\n{Colors.BOLD}📊 OPSI TAMBAHAN:{Colors.ENDC}")
        print(f"{Colors.OKBLUE}1. Lihat semua hasil{Colors.ENDC}")
        print(f"{Colors.OKBLUE}2. Simpan hasil ke file baru{Colors.ENDC}")
        print(f"{Colors.OKBLUE}3. Kembali{Colors.ENDC}")
        
        choice = input(f"\n{Colors.OKCYAN}Pilihan (1-3): {Colors.ENDC}").strip()
        
        if choice == '1':
            self._show_all_results()
        elif choice == '2':
            self._save_last_results_as_new()
    
    def _show_all_results(self):
        """Tampilkan semua hasil analisis"""
        if not self.current_results:
            return
        
        print(f"\n{Colors.BOLD}📋 SEMUA HASIL ANALISIS{Colors.ENDC}")
        print(f"{'='*80}")
        
        for i, result in enumerate(self.current_results, 1):
            pred = result['prediction']
            url_short = result['url'][:60] + "..." if len(result['url']) > 60 else result['url']
            conf_percent = result.get('confidence', 0) * 100
            
            if pred == 'phishing':
                color = Colors.FAIL
                icon = "🔴"
            elif pred == 'legitimate':
                color = Colors.OKGREEN
                icon = "🟢"
            else:
                color = Colors.WARNING
                icon = "⚪"
            
            print(f"{i:3d}. {icon} {color}{pred.upper():12s}{Colors.ENDC} "
                  f"({conf_percent:5.1f}%): {url_short}")
            
            # Tampilkan 20 hasil pertama saja, lalu beri pilihan
            if i == 20 and len(self.current_results) > 20:
                print(f"\n... dan {len(self.current_results)-20} hasil lainnya")
                view_more = input(f"{Colors.OKCYAN}Tampilkan semua? (y/n): {Colors.ENDC}").lower()
                if view_more != 'y':
                    break
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali...{Colors.ENDC}")
    
    def _save_last_results_as_new(self):
        """Simpan hasil terakhir sebagai file baru"""
        if not self.current_results:
            print_error("Tidak ada hasil untuk disimpan!")
            return
        
        filename = input(f"\n{Colors.OKCYAN}Nama file (tanpa ekstensi): {Colors.ENDC}").strip()
        if not filename:
            filename = f"hasil_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            saved_path = self.app.dataset_manager.save_results(self.current_results, filename)
            
            if saved_path:
                print_success(f"Hasil disimpan di: {saved_path}")
            else:
                print_error("Gagal menyimpan hasil!")
                
        except Exception as e:
            print_error(f"Error menyimpan: {str(e)}")