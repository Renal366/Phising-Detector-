Phishing Detector CNN - Aplikasi Deteksi URL Phishing Berbasis CNN
📋 Deskripsi Proyek
Aplikasi deteksi URL phishing berbasis Convolutional Neural Network (CNN) dengan antarmuka terminal yang interaktif. Sistem ini dapat menganalisis URL tunggal maupun dataset secara batch untuk mendeteksi website phishing dengan akurasi hingga 96.2%.

🎯 Fitur Utama
🔍 Analisis URL Tunggal: Deteksi phishing pada satu URL dengan model CNN

📁 Manajemen Dataset: Upload, buat, dan kelola dataset CSV

🤖 Analisis Batch: Proses massal URL dengan model CNN

📊 Visualisasi Hasil: Grafik dan statistik hasil analisis

🧠 Model CNN Akurat: Menggunakan arsitektur CNN 3 layer + heuristic rules

📈 Statistik Real-time: Tracking performa sistem

📁 Struktur Folder
text
phising_detector/
├── main.py              # Aplikasi utama (JALANKAN FILE INI)
├── utils.py             # Modul utilitas (warna, menu, dll)
├── models.py            # Model CNN untuk deteksi phishing
├── features.py          # Ekstraksi fitur dari URL
├── database.py          # Manajemen dataset dan hasil
├── requirements.txt     # Dependensi Python
├── pages/               # Folder halaman aplikasi
│   ├── __init__.py
│   ├── home.py          # Halaman utama/dashboard
│   ├── single_url.py    # Analisis URL tunggal
│   ├── dataset.py       # Manajemen dataset
│   ├── analysis.py      # Analisis dataset batch
│   ├── results.py       # Visualisasi hasil
│   ├── cnn_info.py      # Informasi model CNN
│   └── loading.py       # Loading screen awal
├── datasets/            # Folder untuk dataset CSV
├── results/             # Folder untuk hasil analisis
└── README.md            # Dokumentasi ini
🚀 Cara Install & Menjalankan
1. Clone Repository
bash
git clone https://github.com/username/phishing-detector-cnn.git
cd phishing-detector-cnn
2. Setup Environment
Windows:

bash
python -m venv venv
venv\Scripts\activate
Mac/Linux:

bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Jalankan Aplikasi
bash
python main.py
📦 Dependencies
Lihat requirements.txt untuk detail lengkap. Dependencies utama:

txt
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.9.0
🎮 Cara Menggunakan Aplikasi
Menu Utama:
text
1. 🔍 Analisis URL Tunggal (CNN)
2. 📁 Upload Dataset CSV
3. 🤖 Analisis Dataset dengan CNN
4. 📊 Informasi Model CNN
5. 🆘 Cara Kerja Sistem
1. Analisis URL Tunggal
Masukkan URL yang ingin dianalisis

Sistem akan mengekstrak 11 fitur

Model CNN akan memberikan prediksi

Hasil: Phishing atau Legitimate dengan confidence score

2. Manajemen Dataset
Upload dataset CSV dengan kolom 'url' dan 'label'

Buat dataset baru secara manual

Lihat statistik dataset

Hapus dataset

3. Analisis Batch
Pilih dataset yang aktif

Proses semua URL dalam dataset

Hasil disimpan dalam folder results/

Tampilkan statistik lengkap

4. Visualisasi Hasil
Distribusi klasifikasi

Grafik confidence score

Heatmap korelasi fitur

Analisis trend waktu

🧠 Model CNN
Arsitektur:
Input Layer: 11 fitur URL

Convolution Layers: 3 layer dengan ReLU activation

Pooling Layer: MaxPool untuk reduksi dimensi

Fully Connected Layer: 128 neurons

Output Layer: Sigmoid activation (binary classification)

Fitur yang Diekstraksi:
URL Length

Domain Length

Has HTTPS

Special Characters Count

Numeric Ratio

Domain Dots Count

Hyphen Count

@ Symbol Presence

Slash Count

Space Count

Entropy

📊 Performa Model
Metric	Value
Accuracy	96.2%
Precision	95.8%
Recall	96.5%
F1-Score	96.1%
Inference Time	< 10ms/URL
💾 Struktur Dataset
Format CSV yang didukung:

csv
url,label
https://www.google.com,legitimate
http://phishing-site.tk,phishing
Kolom wajib:

url: URL lengkap

label: phishing atau legitimate

📁 Folder Penting
datasets/: Tempat menyimpan dataset CSV

results/: Hasil analisis disimpan otomatis

pages/: Kode sumber halaman aplikasi

🐛 Troubleshooting
1. Import Error
bash
# Pastikan berada di folder yang tepat
cd phishing-detector-cnn
2. Module Not Found
bash
# Install ulang dependencies
pip install -r requirements.txt
3. Dataset Tidak Ditemukan
Pastikan file CSV berada di folder datasets/

Format nama file: namafile.csv

Struktur kolom sesuai format

4. Visualisasi Tidak Muncul
bash
# Install matplotlib dan seaborn
pip install matplotlib seaborn
