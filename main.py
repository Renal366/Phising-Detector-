"""
MAIN APLIKASI - DETEKSI URL PHISHING DENGAN CNN
Aplikasi utama yang mengkoordinasikan semua halaman dan komponen sistem.
"""
import os
import sys
import time
from utils import Colors, clear_screen, print_banner 
from pages.home import HomePage
from pages.single_url import SingleURLPage
from pages.dataset import DatasetPage
from pages.analysis import AnalysisPage
from pages.results import ResultsPage
from database import DatasetManager
from pages.cnn_info import CNNInfoPage

class PhishingDetectorApp:
    """Kelas utama aplikasi deteksi phishing"""
    
    def __init__(self):

        """Inisialisasi aplikasi dengan semua halaman yang diperlukan"""
        self.current_page = "home"
        self.dataset_manager = DatasetManager()
        self.history = []
        
        # Inisialisasi semua halaman
        self.pages = {
            "home": HomePage(self),
            "single_url": SingleURLPage(self),
            "dataset": DatasetPage(self),
            "analysis": AnalysisPage(self),
            "cnn_info": CNNInfoPage(self)
            
        }
        
        # Status aplikasi
        self.stats = {
            'total_analyzed': 0,
            'phishing_detected': 0,
            'legitimate_detected': 0,
            'datasets_loaded': 0
        }
        
        self._show_ready_message()
    def main():
        """Fungsi utama untuk menjalankan aplikasi"""
    
    # Inisialisasi aplikasi setelah loading
        app = PhishingDetectorApp()
    
    # Jalankan aplikasi
        app.run()

    def show_startup_loading():
        """Tampilkan loading screen saat startup"""
    try:
        # Import loading screen dari pages
        from pages.loading import LoadingScreen
        
        # Buat instance dan tampilkan
        loader = LoadingScreen()
        print(f"{Colors.OKCYAN}🚀 Memuat loading screen...{Colors.ENDC}")
        loader.display()
        
    except Exception as e:
        # Fallback loading sederhana
        print(f"{Colors.WARNING}⚠️  Loading screen error: {str(e)}{Colors.ENDC}")
    
    def simple_loading():

        """Loading sederhana jika yang utama error"""
    clear_screen()
    print(f"{Colors.BOLD}{Colors.OKCYAN}", end="", flush=True)
    
    banner = """
                                         @@@@@@@@@@@@@@@@@@                                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@                                    
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                 
                              n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@n                              
                             @@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@                             
                           @@@ @   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @ @@@                           
                          @@@ @@  @@@@@@@@@@@@@@ @@ n@@@@@@@@@@@@@  @@ @@@                          
                         @  @@ @@@@@@@@@@@@@@@@@@@ @@@@@@@@@@@@@@@@@@ @@  @                         
                        @@  @@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@  @@                        
                        @ @   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @ @                        
                        @ @ @  @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@  @ @ @                        
                        @  @  @@@@@@@@@@@      @@@@@@      @@@@@@@@@@@  @  @                        
                        @ @  @ @@@@@@@@@       @@  @@       @@@@@@@@@ @  @ @                        
                        @  @ @  @@@@@@@         @  @         @@@@@@@  @ @  @                        
                         @@  @  @@@@@@@                      @@@@@@@  @  @@                         
                          @ @@  @  @@@@                      @@@@  @  @@ @                          
                           @@   @@ @ @@                      @@ @ @@   @@                           
                             @n@    n                          n    @n@                             
                              n@@                                  @@n                              
                                 @@ @@@@@                  @@@@@ @@                                 
                                    @@@@@@@              @@@@@@@                                    
                                         @                @                                         
                        ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗   
                        ██╔══██╗██║  ██║██║██╔════╝██║  ██║██║████╗  ██║██╔════╝   
                        ██████╔╝███████║██║███████╗███████║██║██╔██╗ ██║██║  ███╗  
                        ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║██║╚██╗██║██║   ██║  
                        ██║     ██║  ██║██║███████║██║  ██║██║██║ ╚████║╚██████╔╝  
                        ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝   
                                                                     
                                SISTEM DETEKSI PHISHING BERBASIS CNN
                                                                             
    """
    for char in banner:
            print(char, end='', flush=True)
            time.sleep(0.005)  # Delay untuk efek mesin ketik
        
    
    print(f"{Colors.ENDC}")
    
    print(f"\n{Colors.OKGREEN}🔄 Memuat aplikasi...{Colors.ENDC}\n")
    
    # Animasi loading
    for i in range(20):
        print(f"\r{Colors.OKCYAN}[{'█' * (i+1)}{'░' * (19-i)}] {(i+1)*5}%{Colors.ENDC}", end="", flush=True)
        time.sleep(0.10)
    
    print(f"\n\n{Colors.OKGREEN}✅ Aplikasi siap!{Colors.ENDC}")
    time.sleep(3)
    clear_screen()
    
    def _show_ready_message(self):
        """Tampilkan pesan hak cipta singkat"""
    from datetime import datetime
    
    clear_screen()
    # Banner hak cipta
    print(f"{Colors.BOLD}{Colors.OKCYAN}", end="", flush=True)
    banner = """
  _  _   _   _  __   ___ ___ ___ _____ _     __       ___ _  _ ___ ___  ___ __  __   _   ___ ___    
 | || | /_\ | |/ /  / __|_ _| _ \_   _/_\   / _|___  |_ _| \| | __/ _ \| _ \  \/  | /_\ / __|_ _|    
 | __ |/ _ \| ' <  | (__ | ||  _/ | |/ _ \  > _|_ _|  | || .` | _| (_) |   / |\/| |/ _ \\__ \| |     
 |_||_/_/ \_\_|\_\  \___|___|_|   |_/_/ \_\ \_____|  |___|_|\_|_| \___/|_|_\_|  |_/_/ \_\___/___| 
                                                                                                                                           
                              
    """
    for char in banner:
            print(char, end='', flush=True)
            time.sleep(0.005)  # Delay untuk efek mesin ketik
    print(f"{Colors.ENDC}")
    
    # Konten hak cipta
    print(f"\n{Colors.BOLD}© 2025 SISTEM DETEKSI PHISHING BERBASIS CNN{Colors.ENDC}")
    print(f"{Colors.WARNING}{'─'*50}{Colors.ENDC}")
    
    info = [
        f"{Colors.OKGREEN}• Pengembang:{Colors.ENDC} Tim Riset Keamanan Siber",
        f"{Colors.OKGREEN}• Institusi:{Colors.ENDC} [Untad: Untad Entod]",
        f"{Colors.OKGREEN}• Tujuan:{Colors.ENDC} Penelitian & Edukasi",
        f"{Colors.OKGREEN}• Model:{Colors.ENDC} CNN Deep Learning ",
        f"{Colors.OKGREEN}• Akurasi:{Colors.ENDC} 96.7%",
        f"{Colors.OKGREEN}• Lisensi:{Colors.ENDC} Academic Use Only",
        f"{Colors.OKGREEN}• Kontak:{Colors.ENDC} nandur@phishingdetector.id"
    ]
    
    for line in info:
        print(f"  {line}")
    
    print(f"\n{Colors.WARNING}{'─'*50}{Colors.ENDC}")
    
    # Fitur aplikasi
    print(f"\n{Colors.BOLD}🎯 FITUR APLIKASI:{Colors.ENDC}")
    print("  1. Analisis URL Tunggal")
    print("  2. Manajemen Dataset CSV")
    print("  3. Analisis Batch Processing")
    print("  4. Informasi Model CNN")
    print("  5. Edukasi Keamanan Phishing")
    
    # Footer
    print(f"\n{Colors.WARNING}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.BOLD}⚡ HAllo Juragan Aplikasi siap digunakan!{Colors.ENDC}")
    print(f"{Colors.WARNING}{'='*50}{Colors.ENDC}")
    
    input(f"\n{Colors.OKBLUE}Tekan ENTER untuk melanjutkan...{Colors.ENDC}")
    clear_screen()
    
    def run(self):
        """Jalankan aplikasi utama"""
        try:
            while True:
                from utils import print_banner
                print_banner(self.current_page)
                # Tampilkan halaman saat ini
                current_page = self.pages[self.current_page]
                current_page.display()
            
                # Proses input pengguna
                choice = current_page.get_input()
                
                # Navigasi antar halaman
                if choice == "back":
                    self.current_page = "home"
                elif choice in self.pages:
                    self.current_page = choice
                elif choice == "exit":
                    self.exit_app()
                
                # Update statistik jika diperlukan
                self.update_stats()
                
        except KeyboardInterrupt:
            self.exit_app()
    
    def update_stats(self):
        """Update statistik aplikasi"""
        self.stats['datasets_loaded'] = len(self.dataset_manager.get_all_datasets())
    
    def exit_app(self):
        """Keluar dari aplikasi dengan pesan yang baik"""
        clear_screen()
        print(f"\n{Colors.OKGREEN}{'='*60}")
        print("TERIMA KASIH TELAH MENGGUNAKAN")
        print("SISTEM DETEKSI URL PHISHING")
        print(f"{'='*60}{Colors.ENDC}\n")
        sys.exit(0)

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    app = PhishingDetectorApp()
    app.run()

if __name__ == "__main__":
    main()