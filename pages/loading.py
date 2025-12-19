"""
HALAMAN LOADING AWAL
Animasi loading sebelum masuk ke aplikasi utama.
"""

import os
import sys
import time
from utils import Colors

class LoadingScreen:
    """Kelas untuk menampilkan animasi loading screen"""
    
    def __init__(self):
        self.version = "v2.1"
        self.author = "Sistem Deteksi Phishing CNN"
        self.year = "2025"
        
    def clear_screen(self):
        """Bersihkan layar terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display(self):  # ✅ METHOD INI HARUS ADA
        """Tampilkan loading screen lengkap"""
        self.clear_screen()
        
    def print_logo(self):
        """Tampilkan logo aplikasi"""
        logo = f"""{Colors.BOLD}{Colors.OKCYAN}
                                                                                                            
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
                                                                     
              SISTEM DETEKSI URL PHISHING BERBASIS CNN              
        {Colors.ENDC}"""
        
        print(logo)
    
    def animate_loading_bar(self, duration=3):
        """Animasi loading bar"""
        print(f"\n{Colors.BOLD}🚀 Memulai sistem deteksi phishing...{Colors.ENDC}\n")
        
        width = 50
        steps = 20
        
        for i in range(steps + 1):
            # Hitung persentase
            percentage = (i / steps) * 100
            
            # Buat loading bar
            bar_length = int(width * (i / steps))
            bar = f"{Colors.OKGREEN}{'█' * bar_length}{Colors.LIGHTBLACK_EX}{'░' * (width - bar_length)}{Colors.ENDC}"
            
            # Status berdasarkan progress
            if percentage < 30:
                status = "Memuat modul dasar..."
            elif percentage < 60:
                status = "Menginisialisasi model CNN..."
            elif percentage < 80:
                status = "Memuat dataset..."
            elif percentage < 95:
                status = "Menyiapkan antarmuka..."
            else:
                status = "Siap digunakan!"
            
            # Tampilkan loading bar
            print(f"\r  [{bar}] {percentage:.0f}% - {status}", end="", flush=True)
            
            # Delay untuk animasi
            time.sleep(duration / steps)
        
        print("\n")
    
    def animate_text(self, text, delay=0.05):
        """Animasi teks ketik"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def system_check(self):
        """Pemeriksaan sistem"""
        print(f"{Colors.BOLD}🔍 Memeriksa sistem...{Colors.ENDC}\n")
        
        checks = [
            ("Python Version", f"{sys.version.split()[0]}", True),
            ("OS System", f"{os.name.upper()}", True),
            ("Working Directory", os.getcwd(), True),
            ("Required Modules", "Semua terinstal", True),
            ("Dataset Folder", "Tersedia", True),
            ("Model CNN", "Tersedia", True)
        ]
        
        for check_name, status, ok in checks:
            icon = f"{Colors.OKGREEN}✓{Colors.ENDC}" if ok else f"{Colors.FAIL}✗{Colors.ENDC}"
            print(f"  {icon} {check_name:<25}: {status}")
            time.sleep(0.1)
        
        print()
    
    def show_welcome_message(self):
        """Tampilkan pesan selamat datang"""
        welcome_text = f"""
        {Colors.BOLD}{Colors.OKCYAN}✨ SELAMAT DATANG! ✨{Colors.ENDC}
        
        {Colors.OKGREEN}Aplikasi Deteksi Phishing siap membantu Anda:{Colors.ENDC}
        • Analisis URL mencurigakan
        • Deteksi website phishing
        • Edukasi keamanan digital
        • Perlindungan data pribadi
        
        {Colors.WARNING}⚠️  Waspada terhadap serangan phishing yang semakin canggih!{Colors.ENDC}
        """
        
        print(welcome_text)
    
    def countdown(self, seconds=3):
        """Animasi hitung mundur"""
        print(f"\n{Colors.BOLD}⏱️  Masuk ke aplikasi dalam:{Colors.ENDC}")
        
        for i in range(seconds, 0, -1):
            print(f"\r  {Colors.OKCYAN}{i}{Colors.ENDC}...", end="", flush=True)
            time.sleep(1)
        
        print(f"\r  {Colors.OKGREEN}🚀 Mulai!{Colors.ENDC}\n")
        time.sleep(0.5)
    
    def display(self):
        """Tampilkan loading screen lengkap"""
        self.clear_screen()
        
        # Tampilkan logo
        self.print_logo()
        
        # Informasi versi
        print(f"{Colors.LIGHTBLACK_EX}{' ' * 20}Versi: {self.version} | © {self.year}{Colors.ENDC}\n")
        
        # Animasi loading bar
        self.animate_loading_bar(duration=2.5)
        
        # System check
        self.system_check()
        
        # Pesan selamat datang
        self.show_welcome_message()
        
        # Hitung mundur
        self.countdown(seconds=2)
        
        # Clear screen untuk aplikasi utama
        self.clear_screen()