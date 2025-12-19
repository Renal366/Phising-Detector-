"""
HALAMAN UTAMA - DASHBOARD APLIKASI
Halaman utama dengan menu navigasi ke semua fitur aplikasi.
"""
import os
import sys
from utils import Colors, print_menu, get_user_choice 

# Tambahkan parent directory ke sys.path agar bisa import dari root
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Sekarang bisa import dari root
from utils import Colors, print_menu, get_user_choice, print_success, print_error, print_warning


class HomePage:
    """
    Halaman utama/dashboard aplikasi.
    Menyediakan navigasi ke semua fitur yang tersedia.
    """
    
    def __init__(self, app):
        """
        Inisialisasi halaman utama.
    
        Args:
        app: Instance aplikasi utama
        """
        self.app = app
        self.menu_options = [
        "🔍 Analisis URL Tunggal (CNN)",
        "📁 Upload Dataset CSV", 
        "🤖 Analisis Dataset dengan CNN",
        "📊 Informasi Model CNN",
        "🆘 Cara Kerja Sistem",
        
    ]
    def display(self):
        # Tampilkan statistik singkat
        self._display_quick_stats()
        
        # Tampilkan menu
        print_menu("MENU NAVIGASI", self.menu_options)
    
    def get_input(self):
        """Dapatkan input dari pengguna"""
        choice = get_user_choice(1, len(self.menu_options))
        
        if choice == 99:
            return "exit"
        
        page_mapping = {
        1: "single_url",     # Analisis URL Tunggal (CNN)
        2: "dataset",        # Upload Dataset CSV
        3: "analysis",       # Analisis Dataset dengan CNN  
        4: "cnn_info",       # Informasi Model CNN
        5: "cnn_info"  
        }
        
        if choice in page_mapping:
            return page_mapping[choice]
        
        return "home"
    
    def _display_quick_stats(self):
        """Tampilkan statistik cepat aplikasi"""
        stats = self.app.stats
        
        print(f"{Colors.BOLD}STATISTIK CEPAT:{Colors.ENDC}")
        print(f"  • URL yang dianalisis: {Colors.OKBLUE}{stats['total_analyzed']}{Colors.ENDC}")
        print(f"  • Phishing terdeteksi: {Colors.FAIL}{stats['phishing_detected']}{Colors.ENDC}")
        print(f"  • URL legitimate: {Colors.OKGREEN}{stats['legitimate_detected']}{Colors.ENDC}")
        print(f"  • Dataset dimuat: {Colors.OKCYAN}{stats['datasets_loaded']}{Colors.ENDC}")
        
        if stats['total_analyzed'] > 0:
            phishing_rate = (stats['phishing_detected'] / stats['total_analyzed']) * 100
            print(f"  • Rasio phishing: {Colors.WARNING}{phishing_rate:.1f}%{Colors.ENDC}")
        
        print()