"""
UTILITAS - FUNGSI BANTUAN
Kumpulan fungsi utilitas untuk aplikasi deteksi phishing.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

class Colors:
    """
    Kode warna ANSI untuk terminal.
    Digunakan untuk memberikan warna pada output terminal.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARK_GRAY = '\033[30m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

def clear_screen():
    """
    Bersihkan layar terminal.
    Mendeteksi sistem operasi untuk perintah yang tepat.
    """
    os.system('clear' if os.name != 'nt' else 'cls')
    
def print_banner(page_name: str = ""):
    """
    Tampilkan banner khusus berdasarkan halaman.
    
    Args:
        page_name: Nama halaman untuk banner khusus
    """
    clear_screen()
    
    banners = {
        "home": """
            ░█▀▀░▀█▀░█▀▀░▀█▀░█▀▀░█▄█░░░█▀▄░█▀▀░▀█▀░█▀▀░█░█░█▀▀░▀█▀░░░█▀█░█░█░▀█▀░█▀▀░▀█▀░█▀█░█▀▀
            ░▀▀█░░█░░▀▀█░░█░░█▀▀░█░█░░░█░█░█▀▀░░█░░█▀▀░█▀▄░▀▀█░░█░░░░█▀▀░█▀█░░█░░▀▀█░░█░░█░█░█░█
            ░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀░▀░░░▀▀░░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀
                        
                        Pencegahan Serangan Siber melalui Deteksi URL Phishing
                Menggunakan Model CNN Berbasis Deep Learning dengan Tingkat Akurasi Optimal
        """,
        
        "single_url": """
                                       
                            ⢠⣾⣿⣿⣗⣢⠀⠀⠀⠀⠀⠀   ⢤⣒⣿⣿⣷⣆⠀⠀
⠀                           ⠋⠉⠉⠙⠻⣿⣷⡄⠀⠀⠀⡄⣾⣿⠛⠉⠉⠉⠃⠀
⠀⠀                          ⢀⡠⢤⣠⣀⡹⡄⠀⠀⠀⡘⣁⣤⣠⠤⡀⠀⠀⠀
⠀                           ⡤⢾⣿⣿⣿⣿⡿⠀⠀⠀⠀⠸⣿⣿⣿⣿⣾⠦⣄⠀ 
⠀⠀⠀⠀                            ⠉⠈⠀⠀⣠⠀⠀⠀⣀⠀⠈⠈⠁⠀⠀⠀⠀   
⠀⠀⠀⠀⠀⠀                            ⣀⡔⢻⠀⠀⠀⠙⠢⡀⠀⠀⠀⠀⠀⠀
                           ⢘⡦⣤⠤⠒⠋⠘⢤⡀⣀⣀⣀⡨⠚⠉⠓⠠⣤⢤⡞⠀  
⠀⠀                           ⠹⡮⡛⠛⠛⢻⡿⠥⠤⡽⡿⠛⠛⠛⣣⡾⠁⠀⠀
⠀⠀⠀                           ⠙⢄⠁⠀⠀⠈⣇⣀⡼⠃⠀⠀ ⢁⠞⠀⠀⠀⠀
⠀⠀⠀⠀⠀                            ⠉⢆⡀⠀⢸⣿⡇⠀⢀⠠⠂⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀                            ⠈⠁⠸⢿⡿⠃⠋⠀⠀⠀⠀⠀⠀
          
                        ANALISIS URL TUNGGAL - CNN MODEL
                      Deteksi Phishing dengan Deep Learning
        """,
        
        "dataset": """

⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠻⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀MANAJEMEN DATASET - CNN TRAINING 
⠀⠠⠀⠐⠒⠒⠀⠀⠈⠉⠉⠉⠉⢉⣉⣉⣉⣙⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Upload & Kelola Data untuk Pelatihan CNN   ⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡀⠤⠒⠒⠉⠁⠀⠀⠀⠀⠳⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠛⠛⠉⠛⠛⠶⢦⣤⡐⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⢳⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⡤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠳⠶⢶⣦⠤⣄⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠉⠑⢄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠀⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄                                                                

        """,
        
        "analysis": """
                                    
            )        (    (   (   (   (                     )    )   (   (       )           (   (   (       )         
   (     ( /(  (     )\ ) )\ ))\ ))\ ))\ )           (   ( /( ( /(   )\ ))\ ) ( /(   (       )\ ))\ ))\ ) ( /( (       
   )\    )\()) )\   (()/((()/(()/(()/(()/(           )\  )\()))\()) (()/(()/( )\())  )\  (  (()/(()/(()/( )\()))\ )    
((((_)( ((_)((((_)(  /(_))/(_))(_))(_))(_))  ___   (((_)((_)\((_)\   /(_))(_)|(_)\ (((_) )\  /(_))(_))(_)|(_)\(()/(    
 )\ _ )\ _((_)\ _ )\(_)) (_))(_))(_))(_))   |___|  )\___ _((_)_((_) (_))(_))   ((_))\___((_)(_))(_))(_))  _((_)/(_))_  
 (_)_\(_) \| (_)_\(_) |  |_ _/ __|_ _/ __|        ((/ __| \| | \| | | _ \ _ \ / _ ((/ __| __/ __/ __|_ _|| \| (_)) __| 
  / _ \ | .` |/ _ \ | |__ | |\__ \| |\__ \         | (__| .` | .` | |  _/   /| (_) | (__| _|\__ \__ \| | | .` | | (_ | 
 /_/ \_\|_|\_/_/ \_\|____|___|___/___|___/          \___|_|\_|_|\_| |_| |_|_\ \___/ \___|___|___/___/___||_|\_|  \___|           
                                        
        ANALISIS BATCH - CNN PROCESSING            Proses Massal URL dengan Model Deep Learning  
        """,
        
        "cnn_info": """
                
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@  @@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@ @@@@@@@   @@@@@@@   @@@@@@@ @@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@ @@@@@@@     @@@@@     @@@@@@@ @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@ @@@n@@@@               @@@@ @@@ @@@@@@@@@@@@@@  ARSITEKTUR CNN - DEEP LEARNING 
@@@@@@@@@@@@@ @@@ @@@@                 @@@@ @@@ @@@@@@@@@@@@@  Model Neural Network untuk Deteksi Phishing 
@@@@@@@@@@@@@@@@ @@@@                   @@@@ @@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@ @@@@      @       @      @@@@ @@@@@@@@@@@@@@@ 
@@@@@@@@@@@@@@@ @@@@      @@     @@      @@@@ @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@ @@@@@                 @@@@@ @@@@@@@@@@@@@@@@
@@@@@@@@@@@@@n@@@ @@@@@@@           @@@@@@@ @@@n@@@@@@@@@@@@@
@@@@@@@@@@@@@@ @@@ @@@@@@@@       @@@@@@@@ @@@ @@@@@@@@@@@@@@
@@@@@@@@@@@@@@@ @@@@@@@@@@@       @@@@@@@@@@@ @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@ @@@@@@@@@@@     @@@@@@@@@@@ @@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        """
    }
    
    # Tampilkan banner sesuai halaman
    banner = banners.get(page_name, banners["home"])
    print(f"{Colors.HEADER}{Colors.BOLD}{banner}{Colors.ENDC}")

    print(f"{Colors.BOLD}Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)
    print(f"{Colors.ENDC}")

def print_menu(title: str, options: list[str], current_page: str = ""):
    """
    Cetak menu dengan format yang konsisten.
    
    Args:
        title: Judul menu
        options: List opsi menu
        current_page: Halaman saat ini (opsional)
    """
    print(f"\n{Colors.BOLD}┌─ {title.upper()} {'─' * (50 - len(title))}┐{Colors.ENDC}")
    
    # Tampilkan opsi menu (dimulai dari 1)
    for i, option in enumerate(options, 1):
        print(f"{Colors.OKBLUE}│ {i}. {option}{Colors.ENDC}")
    
    # Jika ada current_page, tambahkan "Kembali" dengan angka yang BENAR
    if current_page and current_page != "home" and current_page != "":
        # Angka untuk "Kembali" adalah angka SETELAH opsi terakhir
        back_number = len(options) + 1
        print(f"{Colors.WARNING}│ {back_number}. Kembali ke Menu Utama{Colors.ENDC}")  # BUKAN 0
    
    print(f"{Colors.WARNING}│ 99. Keluar Aplikasi{Colors.ENDC}")
    print(f"{Colors.BOLD}└{'─' * 56}┘{Colors.ENDC}")

def get_user_choice(min_val: int = 0, max_val: int = 99) -> int:
    """
    Dapatkan pilihan pengguna dengan validasi.
    
    Args:
        min_val: Nilai minimum yang valid
        max_val: Nilai maksimum yang valid
        
    Returns:
        Pilihan pengguna sebagai integer
    """
    while True:
        try:
            choice = input(f"\n{Colors.OKBLUE}Pilih opsi ({min_val}-{max_val}): {Colors.ENDC}").strip()
            
            if choice == "":
                print(f"{Colors.FAIL}Pilihan tidak boleh kosong!{Colors.ENDC}")
                continue
            
            choice_int = int(choice)
            
            if choice_int == 99:
                return 99
            
            if min_val <= choice_int <= max_val:
                return choice_int
            else:
                print(f"{Colors.FAIL}Pilihan harus antara {min_val} dan {max_val}!{Colors.ENDC}")
                
        except ValueError:
            print(f"{Colors.FAIL}Masukkan angka yang valid!{Colors.ENDC}")

def print_table(headers: List[str], rows: List[List[str]], title: str = ""):
    """
    Cetak tabel dengan format yang rapi.
    
    Args:
        headers: List header kolom
        rows: List baris data
        title: Judul tabel (opsional)
    """
    if title:
        print(f"\n{Colors.BOLD}{title}{Colors.ENDC}")
    
    # Hitung lebar kolom
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Tambahkan padding
    col_widths = [w + 2 for w in col_widths]
    
    # Cetak header
    header_line = "┌"
    for w in col_widths:
        header_line += "─" * w + "┬"
    header_line = header_line[:-1] + "┐"
    print(header_line)
    
    header_cells = []
    for i, header in enumerate(headers):
        header_cells.append(f"{header:<{col_widths[i]}}")
    print(f"│{Colors.BOLD}{Colors.OKBLUE}" + "│".join(header_cells) + f"{Colors.ENDC}│")
    
    # Cetak separator
    sep_line = "├"
    for w in col_widths:
        sep_line += "─" * w + "┼"
    sep_line = sep_line[:-1] + "┤"
    print(sep_line)
    
    # Cetak rows
    for row in rows:
        row_cells = []
        for i, cell in enumerate(row):
            if i < len(col_widths):
                row_cells.append(f"{str(cell):<{col_widths[i]}}")
        print("│" + "│".join(row_cells) + "│")
    
    # Cetak footer
    footer_line = "└"
    for w in col_widths:
        footer_line += "─" * w + "┴"
    footer_line = footer_line[:-1] + "┘"
    print(footer_line)

def progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', length: int = 50):
    """
    Tampilkan progress bar di terminal.
    
    Args:
        iteration: Iterasi saat ini
        total: Total iterasi
        prefix: Teks sebelum progress bar
        suffix: Teks setelah progress bar
        length: Panjang progress bar
    """
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = f"{Colors.OKGREEN}█{Colors.ENDC}" * filled_length + f"{Colors.WARNING}░{Colors.ENDC}" * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    
    if iteration == total:
        print()

def validate_url(url: str) -> bool:
    """
    Validasi format URL.
    
    Args:
        url: URL string untuk divalidasi
        
    Returns:
        True jika URL valid, False jika tidak
    """
    import re
    
    # Pattern untuk validasi URL sederhana
    pattern = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'(([A-Z0-9]([A-Z0-9-]*[A-Z0-9])?\.)+[A-Z]{2,}|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP address
        r'(:\d+)?'  # port
        r'(/.*)?$', re.IGNORECASE)
    
    return bool(pattern.match(url))

def format_bytes(size: int) -> str:
    """
    Format ukuran bytes menjadi human-readable string.
    
    Args:
        size: Ukuran dalam bytes
        
    Returns:
        String yang diformat
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def get_timestamp() -> str:
    """
    Dapatkan timestamp saat ini dalam format string.
    
    Returns:
        Timestamp string
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def print_success(message: str):
    """
    Cetak pesan sukses dengan format yang konsisten.
    
    Args:
        message: Pesan sukses
    """
    print(f"\n{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message: str):
    """
    Cetak pesan error dengan format yang konsisten.
    
    Args:
        message: Pesan error
    """
    print(f"\n{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_warning(message: str):
    """
    Cetak pesan peringatan dengan format yang konsisten.
    
    Args:
        message: Pesan peringatan
    """
    print(f"\n{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_info(message: str):
    """
    Cetak pesan informasi dengan format yang konsisten.
    
    Args:
        message: Pesan informasi
    """
    print(f"\n{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")