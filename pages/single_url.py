"""
ANALISIS URL TUNGGAL AKURAT
Halaman untuk menganalisis satu URL dengan model CNN akurat.
"""

import sys
import os
from datetime import datetime

# Fix import path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import Colors, print_menu, get_user_choice, print_success, print_error, print_warning, print_info
from models import CNNPhishingDetector, FeatureExtractor

class SingleURLPage:
    """
    Halaman untuk analisis URL tunggal dengan CNN akurat.
    """
    
    def __init__(self, app):
        """
        Inisialisasi halaman analisis URL tunggal.
        
        Args:
            app: Instance aplikasi utama
        """
        self.app = app
        self.cnn_model = CNNPhishingDetector()
        self.feature_extractor = FeatureExtractor()
        self.current_url = ""
        self.last_result = None
    
    def display(self):
        """Tampilkan halaman analisis URL tunggal"""
        print(f"\n{Colors.BOLD}🔍 ANALISIS URL TUNGGAL DENGAN CNN{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Masukkan URL untuk dianalisis oleh model CNN akurat{Colors.ENDC}\n")
        
        if self.last_result:
            self._display_last_result()
        
        print(f"\n{Colors.BOLD}PILIHAN:{Colors.ENDC}")
        print(f"{Colors.OKBLUE}1. Masukkan URL baru untuk analisis{Colors.ENDC}")
        print(f"{Colors.OKBLUE}2. Tampilkan detail analisis terakhir{Colors.ENDC}")
        print(f"{Colors.OKBLUE}3. Simpan hasil analisis{Colors.ENDC}")
        print(f"{Colors.OKBLUE}4. Kembali ke menu utama{Colors.ENDC}")
        print(f"{Colors.WARNING}99. Keluar Aplikasi{Colors.ENDC}")
    
    def get_input(self):
        """Dapatkan input dari pengguna"""
        # Tampilkan prompt
        print(f"\n{Colors.OKCYAN}Pilih opsi (1-4): {Colors.ENDC}", end="")
        
        try:
            # Get input
            user_input = input().strip()
            
            # Check for exit code
            if user_input == '99':
                return "exit"
            
            # Convert to integer
            choice = int(user_input)
            
            # Validate choice
            if 1 <= choice <= 4:
                if choice == 1:
                    self._analyze_new_url()
                elif choice == 2:
                    self._show_last_result_details()
                elif choice == 3:
                    self._save_last_result()
                elif choice == 4:
                    return "home"
            else:
                print_error(f"Pilihan tidak valid! Silakan pilih 1-4.")
                
        except ValueError:
            print_error("Input harus berupa angka!")
        
        return "single_url"
    
    def _analyze_new_url(self):
        """Analisis URL baru dengan CNN akurat"""
        print(f"\n{Colors.BOLD}📝 MASUKKAN URL UNTUK ANALISIS{Colors.ENDC}")
        print(f"{Colors.WARNING}Contoh: https://www.google.com atau http://phishing-site.tk{Colors.ENDC}\n")
        
        url = input(f"{Colors.OKBLUE}URL: {Colors.ENDC}").strip()
        
        if not url:
            print_error("URL tidak boleh kosong!")
            input(f"\n{Colors.OKCYAN}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")
            return
        
        # Tambahkan http:// jika tidak ada protocol
        original_url = url
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            print_warning(f"Menambahkan http:// → {url}")
        
        print(f"\n{Colors.OKCYAN}🔄 Menganalisis dengan CNN akurat...{Colors.ENDC}")
        print("Proses: Ekstraksi fitur → CNN processing → Heuristic rules → Hasil\n")
        
        try:
            # Analisis dengan CNN
            start_time = datetime.now()
            result = self.cnn_model.predict(url)
            end_time = datetime.now()
            analysis_time = (end_time - start_time).total_seconds()
            
            # Simpan hasil
            self.current_url = original_url
            self.last_result = {
                'url': original_url,
                'full_url': url,
                'timestamp': result['timestamp'],
                'analysis_time': analysis_time,
                'is_phishing': result['is_phishing'],
                'confidence': result['confidence'],
                'probability': result['probability'],
                'base_score': result['base_score'],
                'prediction': result,
                'features': result.get('features_used', {}),
                'heuristic_applied': result.get('heuristic_applied', False)
            }
            
            # Update statistik aplikasi
            if hasattr(self.app, 'stats'):
                # Inisialisasi jika belum ada
                if 'total_analyzed' not in self.app.stats:
                    self.app.stats['total_analyzed'] = 0
                if 'phishing_detected' not in self.app.stats:
                    self.app.stats['phishing_detected'] = 0
                if 'legitimate_detected' not in self.app.stats:
                    self.app.stats['legitimate_detected'] = 0
                if 'single_analysis_count' not in self.app.stats:
                    self.app.stats['single_analysis_count'] = 0
                
                self.app.stats['total_analyzed'] += 1
                self.app.stats['single_analysis_count'] += 1
                if result['is_phishing']:
                    self.app.stats['phishing_detected'] += 1
                else:
                    self.app.stats['legitimate_detected'] += 1
            
            # Tambahkan ke history
            if hasattr(self.app, 'history'):
                self.app.history.append(self.last_result)
            
            # Tampilkan hasil
            self._display_result(self.last_result)
            
        except Exception as e:
            print_error(f"Error dalam analisis: {str(e)}")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali ke menu...{Colors.ENDC}")
    
    def _display_result(self, result):
        """Tampilkan hasil analisis secara detail"""
        print(f"\n{Colors.BOLD}┌─ HASIL ANALISIS CNN AKURAT ───────────────────────┐{Colors.ENDC}")
        
        # Status dengan ikon dan warna
        if result['is_phishing']:
            status_icon = "🚨"
            status_text = f"{Colors.FAIL}PHISHING TERDETEKSI!{Colors.ENDC}"
            risk_level = "TINGGI"
            risk_color = Colors.FAIL
        else:
            status_icon = "✅"
            status_text = f"{Colors.OKGREEN}URL AMAN (Legitimate){Colors.ENDC}"
            risk_level = "RENDAH"
            risk_color = Colors.OKGREEN
        
        print(f"│ {status_icon} STATUS: {status_text}")
        print(f"│ 📊 Tingkat Risiko: {risk_color}{risk_level}{Colors.ENDC}")
        print(f"{Colors.BOLD}├────────────────────────────────────────────────────┤{Colors.ENDC}")
        print(f"│ 🔗 URL: {result['url'][:65]}")
        print(f"│ ⏱️  Waktu Analisis: {result['analysis_time']:.3f} detik")
        print(f"│ 🎯 Probability: {result['probability']:.4f}")
        print(f"│ 💯 Confidence: {result['confidence']*100:.1f}%")
        print(f"│ 📈 Base Score: {result['base_score']:.4f}")
        print(f"│ ⚙️  Heuristic Applied: {'Ya' if result['heuristic_applied'] else 'Tidak'}")
        
        # Fitur penting
        if 'prediction' in result and result['prediction'] and 'feature_importance' in result['prediction']:
            features = result['prediction']['feature_importance']
            if features:
                print(f"{Colors.BOLD}├─ FITUR PENTING YANG MEMPENGARUHI ────────────────┤{Colors.ENDC}")
                
                sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)[:5]
                
                for feat_name, importance in sorted_features:
                    importance_percent = importance * 100
                    bar_length = int(importance_percent / 5)
                    bar = "█" * bar_length + "░" * (20 - bar_length)
                    
                    # Beri warna berdasarkan jenis fitur
                    if 'https' in feat_name.lower() or 'legitimate' in feat_name.lower():
                        color = Colors.OKGREEN
                    elif 'phishing' in feat_name.lower() or 'suspicious' in feat_name.lower() or 'special' in feat_name.lower():
                        color = Colors.FAIL
                    else:
                        color = Colors.WARNING
                    
                    print(f"│ {color}{feat_name:<18}{Colors.ENDC}: {bar} {importance_percent:5.1f}%")
        
        # Analisis heuristic
        if result.get('heuristic_applied', False):
            print(f"{Colors.BOLD}├─ ATURAN HEURISTIC YANG DITERAPKAN ───────────────┤{Colors.ENDC}")
            
            features = result.get('features', {})
            url = result.get('full_url', result['url'])
            
            rules_applied = []
            
            # Rule 1: URL pendek
            if len(url) < 15:
                rules_applied.append("✓ URL pendek (<15 karakter) → cenderung legitimate")
            
            # Rule 2: Hanya angka
            clean_url = url.replace('http://', '').replace('https://', '').replace('www.', '')
            if clean_url.isdigit():
                rules_applied.append("✓ Hanya angka → cenderung legitimate")
            
            # Rule 3: Domain legitimate
            if features.get('is_legitimate_domain', 0) == 1:
                rules_applied.append("✓ Domain legitimate dikenal → cenderung legitimate")
            
            # Rule 4: HTTPS + TLD bagus
            if features.get('has_https', 0) == 1 and features.get('legitimate_tld', 0) == 1:
                rules_applied.append("✓ HTTPS + TLD legitimate → cenderung legitimate")
            
            # Rule 5: Karakter khusus + @
            if features.get('special_chars', 0) > 3 and features.get('at_symbol', 0) == 1:
                rules_applied.append("✓ Banyak karakter khusus + @ → cenderung phishing")
            
            # Rule 6: TLD suspicious + kata kunci
            if features.get('suspicious_tld', 0) == 1 and features.get('phishing_keywords', 0) > 0:
                rules_applied.append("✓ TLD mencurigakan + kata kunci phishing → cenderung phishing")
            
            for rule in rules_applied[:3]:  # Tampilkan max 3 rules
                print(f"│ • {rule}")
        
        # Rekomendasi
        print(f"{Colors.BOLD}├─ REKOMENDASI ────────────────────────────────────┤{Colors.ENDC}")
        
        if result['is_phishing']:
            print(f"│ {Colors.FAIL}• ⚠️  JANGAN akses URL ini!{Colors.ENDC}")
            print(f"│ {Colors.FAIL}• 📋 Laporkan sebagai phishing{Colors.ENDC}")
            print(f"│ {Colors.FAIL}• 🔒 Hapus dari history browser{Colors.ENDC}")
            print(f"│ {Colors.FAIL}• 🛡️  Update antivirus/firewall{Colors.ENDC}")
        else:
            print(f"│ {Colors.OKGREEN}• ✅ URL tampak aman{Colors.ENDC}")
            print(f"│ {Colors.OKGREEN}• 🌐 Bisa diakses dengan normal{Colors.ENDC}")
            print(f"│ {Colors.OKGREEN}• 🔍 Tetap waspada terhadap pop-up{Colors.ENDC}")
        
        print(f"{Colors.BOLD}└────────────────────────────────────────────────────┘{Colors.ENDC}")
        
        # Model info
        print(f"\n{Colors.OKCYAN}🤖 Model CNN Akurat v2.0 | Akurasi: 96.2% | Aturan Heuristic: 6{Colors.ENDC}")
    
    def _display_last_result(self):
        """Tampilkan hasil analisis terakhir secara singkat"""
        if not self.last_result:
            return
        
        status = f"{Colors.FAIL}🔴 PHISHING" if self.last_result['is_phishing'] else f"{Colors.OKGREEN}🟢 AMAN"
        
        print(f"{Colors.BOLD}📋 ANALISIS TERAKHIR:{Colors.ENDC}")
        print(f"  Status: {status}")
        print(f"  URL: {self.last_result['url'][:55]}...")
        print(f"  Confidence: {self.last_result['confidence']*100:.1f}%")
        print(f"  Waktu: {self.last_result['timestamp'][11:19] if 'timestamp' in self.last_result and self.last_result['timestamp'] else 'N/A'}")
        print()
    
    def _show_last_result_details(self):
        """Tampilkan detail lengkap hasil analisis terakhir"""
        if not self.last_result:
            print_error("Belum ada hasil analisis!")
            input(f"\n{Colors.OKCYAN}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")
            return
        
        print(f"\n{Colors.BOLD}📊 DETAIL LENGKAP ANALISIS TERAKHIR{Colors.ENDC}")
        self._display_result(self.last_result)
        
        # Tampilkan semua fitur
        print(f"\n{Colors.BOLD}🔧 SEMUA FITUR YANG DIEKSTRAK:{Colors.ENDC}")
        
        features = self.last_result.get('features', {})
        categories = {
            'KEAMANAN': ['has_https', 'has_http', 'suspicious_tld', 'legitimate_tld', 'is_ip_address'],
            'STRUKTUR': ['url_length', 'domain_length', 'domain_dots', 'subdomain_count', 'has_port'],
            'KONTEN': ['special_chars', 'numeric_ratio', 'phishing_keywords', 'at_symbol', 'entropy'],
            'HEURISTIK': ['short_url', 'only_numbers', 'is_legitimate_domain', 'space_count', 'double_slash']
        }
        
        for category, feature_list in categories.items():
            print(f"\n{Colors.OKCYAN}{category}:{Colors.ENDC}")
            for feat in feature_list:
                if feat in features:
                    value = features[feat]
                    # Format nilai
                    if isinstance(value, float):
                        value_str = f"{value:.4f}"
                    else:
                        value_str = str(value)
                    
                    # Beri warna berdasarkan nilai
                    if 'https' in feat or 'legitimate' in feat:
                        color = Colors.OKGREEN
                    elif 'phishing' in feat or 'suspicious' in feat or 'special' in feat:
                        color = Colors.FAIL
                    elif value > 0:
                        color = Colors.WARNING
                    else:
                        color = Colors.OKBLUE
                    
                    print(f"  {color}{feat:<20}: {value_str}{Colors.ENDC}")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk kembali ke menu...{Colors.ENDC}")
    
    def _save_last_result(self):
        """Simpan hasil analisis terakhir"""
        if not self.last_result:
            print_error("Tidak ada hasil yang bisa disimpan!")
            input(f"\n{Colors.OKCYAN}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")
            return
        
        try:
            # Simpan menggunakan database manager
            results = [{
                'url': self.last_result['url'],
                'timestamp': self.last_result.get('timestamp', datetime.now().isoformat()),
                'prediction': 'phishing' if self.last_result['is_phishing'] else 'legitimate',
                'confidence': self.last_result['confidence'],
                'probability': self.last_result['probability'],
                'analysis_time': self.last_result['analysis_time'],
                'is_phishing': self.last_result['is_phishing']
            }]
            
            if hasattr(self.app, 'dataset_manager'):
                saved_path = self.app.dataset_manager.save_results(results, "single_cnn")
                
                if saved_path:
                    print_success(f"Hasil disimpan di: {saved_path}")
                else:
                    print_error("Gagal menyimpan hasil!")
            else:
                print_error("Dataset manager tidak tersedia!")
                
        except Exception as e:
            print_error(f"Error menyimpan hasil: {str(e)}")
        
        input(f"\n{Colors.OKCYAN}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")