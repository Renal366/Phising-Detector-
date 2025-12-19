"""
VISUALISASI HASIL
Halaman untuk menampilkan dan memvisualisasikan hasil analisis.
"""
import sys
import os

# FIX: Tambahkan parent directory ke sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Sekarang import akan bekerja
from utils import Colors, print_menu, get_user_choice, print_success, print_error, print_warning
import matplotlib.pyplot as plt
import pandas as pd
class ResultsPage:
    """
    Halaman untuk visualisasi hasil analisis.
    Menyediakan berbagai chart dan grafik untuk analisis data.
    """
    
    def __init__(self, app):
        """
        Inisialisasi halaman visualisasi hasil.
        
        Args:
            app: Instance aplikasi utama
        """
        self.app = app
    
    def display(self):
        
        # Tampilkan menu
        print_menu("JENIS VISUALISASI", [
            "Distribusi Hasil Klasifikasi",
            "Grafik Confidence Score",
            "Analisis Fitur Penting",
            "Perbandingan Label Aktual vs Prediksi",
            "Trend Analisis Waktu",
            "Heatmap Korelasi Fitur",
            "Kembali ke Menu Utama"
        ], "results")
    
    def get_input(self):
        """Dapatkan input dari pengguna"""
        choice = get_user_choice(1, 7)
        
        if choice == 99:
            return "exit"
        
        if choice == 1:
            self._show_classification_distribution()
        elif choice == 2:
            self._show_confidence_chart()
        elif choice == 3:
            self._show_feature_importance()
        elif choice == 4:
            self._show_comparison_chart()
        elif choice == 5:
            self._show_time_analysis()
        elif choice == 6:
            self._show_correlation_heatmap()
        elif choice == 7:
            return "home"
        
        return "results"
    
    def _show_classification_distribution(self):
        """Tampilkan distribusi hasil klasifikasi"""
        try:
            import matplotlib.pyplot as plt
            
            # Dapatkan data dari hasil analisis terakhir
            analysis_page = self.app.pages["analysis"]
            results = analysis_page.current_results
            
            if not results or 'results' not in results:
                print_error("Tidak ada data hasil analisis!")
                print_warning("Silakan jalankan analisis dataset terlebih dahulu.")
                return
            
            data = results['results']
            
            # Hitung distribusi
            phishing_count = sum(1 for r in data if r['predicted_label'] == 'phishing')
            legitimate_count = len(data) - phishing_count
            
            # Buat pie chart
            labels = ['Phishing', 'Legitimate']
            sizes = [phishing_count, legitimate_count]
            colors = ['#ff6b6b', '#51cf66']
            explode = (0.1, 0)  # Explode phishing slice
            
            plt.figure(figsize=(10, 8))
            
            plt.subplot(2, 2, 1)
            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
            plt.title('Distribusi Hasil Klasifikasi', fontsize=14, fontweight='bold')
            plt.axis('equal')
            
            # Buat bar chart
            plt.subplot(2, 2, 2)
            bars = plt.bar(labels, sizes, color=colors, edgecolor='black', linewidth=2)
            plt.title('Jumlah URL per Kategori', fontsize=14, fontweight='bold')
            plt.ylabel('Jumlah URL')
            
            # Tambahkan nilai di atas bar
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            # Tampilkan statistik
            plt.subplot(2, 2, 3)
            plt.axis('off')
            
            stats_text = f"""
            STATISTIK KLASIFIKASI
            {'='*30}
            Total URL: {len(data)}
            Phishing: {phishing_count} ({phishing_count/len(data)*100:.1f}%)
            Legitimate: {legitimate_count} ({legitimate_count/len(data)*100:.1f}%)
            
            CONFIDENCE RATA-RATA:
            Phishing: {sum(r['confidence'] for r in data if r['predicted_label'] == 'phishing')/phishing_count*100 if phishing_count > 0 else 0:.1f}%
            Legitimate: {sum(r['confidence'] for r in data if r['predicted_label'] == 'legitimate')/legitimate_count*100 if legitimate_count > 0 else 0:.1f}%
            """
            
            plt.text(0.1, 0.5, stats_text, fontsize=12, family='monospace', verticalalignment='center')
            
            # Histogram probability
            plt.subplot(2, 2, 4)
            phishing_probs = [r['probability'] for r in data if r['predicted_label'] == 'phishing']
            legitimate_probs = [r['probability'] for r in data if r['predicted_label'] == 'legitimate']
            
            plt.hist(phishing_probs, alpha=0.5, label='Phishing', color='red', bins=20)
            plt.hist(legitimate_probs, alpha=0.5, label='Legitimate', color='green', bins=20)
            plt.title('Distribusi Probabilitas', fontsize=14, fontweight='bold')
            plt.xlabel('Probabilitas')
            plt.ylabel('Frekuensi')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.suptitle('Visualisasi Hasil Klasifikasi URL Phishing', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.show()
            
            print_success("Visualisasi distribusi klasifikasi ditampilkan!")
            
        except ImportError:
            print_error("Modul matplotlib tidak tersedia!")
            print_warning("Instal dengan: pip install matplotlib")
        except Exception as e:
            print_error(f"Error menampilkan visualisasi: {str(e)}")
    
    def _show_confidence_chart(self):
        """Tampilkan grafik confidence score"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Dapatkan data
            analysis_page = self.app.pages["analysis"]
            results = analysis_page.current_results
            
            if not results or 'results' not in results:
                print_error("Tidak ada data hasil analisis!")
                return
            
            data = results['results']
            
            # Siapkan data untuk plotting
            phishing_confidences = [r['confidence'] * 100 for r in data if r['predicted_label'] == 'phishing']
            legitimate_confidences = [r['confidence'] * 100 for r in data if r['predicted_label'] == 'legitimate']
            
            plt.figure(figsize=(12, 8))
            
            # Box plot
            plt.subplot(2, 2, 1)
            box_data = [phishing_confidences, legitimate_confidences]
            box_labels = ['Phishing', 'Legitimate']
            
            box = plt.boxplot(box_data, labels=box_labels, patch_artist=True)
            
            # Warna box
            colors = ['lightcoral', 'lightgreen']
            for patch, color in zip(box['boxes'], colors):
                patch.set_facecolor(color)
            
            plt.title('Distribusi Confidence Score', fontsize=14, fontweight='bold')
            plt.ylabel('Confidence (%)')
            plt.grid(True, alpha=0.3)
            
            # Scatter plot
            plt.subplot(2, 2, 2)
            
            # Ambil sample untuk scatter plot (maks 100)
            sample_size = min(100, len(data))
            sample_indices = np.random.choice(len(data), sample_size, replace=False)
            
            phishing_x, phishing_y = [], []
            legitimate_x, legitimate_y = [], []
            
            for idx in sample_indices:
                result = data[idx]
                if result['predicted_label'] == 'phishing':
                    phishing_x.append(result['probability'])
                    phishing_y.append(result['confidence'] * 100)
                else:
                    legitimate_x.append(result['probability'])
                    legitimate_y.append(result['confidence'] * 100)
            
            plt.scatter(phishing_x, phishing_y, color='red', alpha=0.6, label='Phishing', s=50)
            plt.scatter(legitimate_x, legitimate_y, color='green', alpha=0.6, label='Legitimate', s=50)
            
            plt.title('Hubungan Probability vs Confidence', fontsize=14, fontweight='bold')
            plt.xlabel('Probability')
            plt.ylabel('Confidence (%)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Density plot
            plt.subplot(2, 2, 3)
            
            from scipy import stats
            
            if phishing_confidences:
                kde_phishing = stats.gaussian_kde(phishing_confidences)
                x_range = np.linspace(min(phishing_confidences + legitimate_confidences), 
                                     max(phishing_confidences + legitimate_confidences), 100)
                plt.plot(x_range, kde_phishing(x_range), color='red', label='Phishing', linewidth=2)
            
            if legitimate_confidences:
                kde_legitimate = stats.gaussian_kde(legitimate_confidences)
                plt.plot(x_range, kde_legitimate(x_range), color='green', label='Legitimate', linewidth=2)
            
            plt.title('Density Plot Confidence Score', fontsize=14, fontweight='bold')
            plt.xlabel('Confidence (%)')
            plt.ylabel('Density')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Cumulative distribution
            plt.subplot(2, 2, 4)
            
            if phishing_confidences:
                sorted_phishing = np.sort(phishing_confidences)
                y_vals = np.arange(len(sorted_phishing)) / float(len(sorted_phishing) - 1)
                plt.plot(sorted_phishing, y_vals, color='red', label='Phishing', linewidth=2)
            
            if legitimate_confidences:
                sorted_legitimate = np.sort(legitimate_confidences)
                y_vals = np.arange(len(sorted_legitimate)) / float(len(sorted_legitimate) - 1)
                plt.plot(sorted_legitimate, y_vals, color='green', label='Legitimate', linewidth=2)
            
            plt.title('Cumulative Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Confidence (%)')
            plt.ylabel('Cumulative Probability')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.suptitle('Analisis Confidence Score Model CNN', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.show()
            
            # Tampilkan statistik
            print(f"\n{Colors.BOLD}📊 STATISTIK CONFIDENCE SCORE:{Colors.ENDC}")
            
            if phishing_confidences:
                print(f"\n{Colors.FAIL}Phishing:{Colors.ENDC}")
                print(f"  Rata-rata: {np.mean(phishing_confidences):.1f}%")
                print(f"  Median: {np.median(phishing_confidences):.1f}%")
                print(f"  Standar Deviasi: {np.std(phishing_confidences):.1f}%")
                print(f"  Minimum: {np.min(phishing_confidences):.1f}%")
                print(f"  Maximum: {np.max(phishing_confidences):.1f}%")
            
            if legitimate_confidences:
                print(f"\n{Colors.OKGREEN}Legitimate:{Colors.ENDC}")
                print(f"  Rata-rata: {np.mean(legitimate_confidences):.1f}%")
                print(f"  Median: {np.median(legitimate_confidences):.1f}%")
                print(f"  Standar Deviasi: {np.std(legitimate_confidences):.1f}%")
                print(f"  Minimum: {np.min(legitimate_confidences):.1f}%")
                print(f"  Maximum: {np.max(legitimate_confidences):.1f}%")
            
        except ImportError as e:
            print_error(f"Modul tidak tersedia: {str(e)}")
            print_warning("Instal modul yang diperlukan: pip install matplotlib scipy numpy")
        except Exception as e:
            print_error(f"Error menampilkan chart: {str(e)}")
    
    def _show_feature_importance(self):
        """Tampilkan analisis feature importance"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Dapatkan data
            analysis_page = self.app.pages["analysis"]
            results = analysis_page.current_results
            
            if not results or 'results' not in results:
                print_error("Tidak ada data hasil analisis!")
                return
            
            data = results['results']
            
            # Kumpulkan feature importance
            feature_importance = {}
            
            for result in data[:100]:  # Batasi untuk performa
                if 'prediction_details' in result and 'feature_importance' in result['prediction_details']:
                    for feature, importance in result['prediction_details']['feature_importance'].items():
                        feature_importance[feature] = feature_importance.get(feature, 0) + importance
            
            # Normalisasi
            if not feature_importance:
                print_error("Tidak ada data feature importance!")
                return
            
            total_importance = sum(feature_importance.values())
            feature_importance = {k: v/total_importance for k, v in feature_importance.items()}
            
            # Urutkan berdasarkan importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            features, importances = zip(*sorted_features[:15])  # Ambil 15 teratas
            
            # Buat horizontal bar chart
            plt.figure(figsize=(12, 8))
            
            y_pos = np.arange(len(features))
            
            # Buat gradient warna
            colors = plt.cm.RdYlGn(importances / max(importances))
            
            plt.barh(y_pos, importances, color=colors, edgecolor='black')
            plt.yticks(y_pos, features)
            plt.xlabel('Importance (Normalized)')
            plt.title('Feature Importance untuk Deteksi Phishing', fontsize=16, fontweight='bold')
            plt.gca().invert_yaxis()  # Fitur terpenting di atas
            
            # Tambahkan nilai di bar
            for i, v in enumerate(importances):
                plt.text(v + 0.01, i, f'{v:.3f}', va='center', fontweight='bold')
            
            plt.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            plt.show()
            
            # Tampilkan deskripsi fitur
            print(f"\n{Colors.BOLD}📋 DESKRIPSI FITUR PENTING:{Colors.ENDC}")
            
            feature_descriptions = {
                'url_length': 'Panjang total URL',
                'special_chars': 'Jumlah karakter khusus',
                'entropy': 'Tingkat kompleksitas/randomness',
                'numeric_ratio': 'Rasio angka dalam URL',
                'domain_dots': 'Jumlah titik dalam domain',
                'has_https': 'Keamanan protokol HTTPS',
                'phishing_keywords': 'Kata kunci phishing umum',
                'hyphen_count': 'Jumlah tanda hubung',
                'at_symbol': 'Kehadiran simbol @',
                'subdomain_count': 'Jumlah subdomain'
            }
            
            for i, (feature, importance) in enumerate(sorted_features[:10], 1):
                description = feature_descriptions.get(feature, 'Tidak ada deskripsi')
                print(f"\n{i}. {Colors.BOLD}{feature}{Colors.ENDC}")
                print(f"   Importance: {importance:.3f}")
                print(f"   Deskripsi: {description}")
            
        except Exception as e:
            print_error(f"Error menampilkan feature importance: {str(e)}")
    
    def _show_comparison_chart(self):
        """Tampilkan perbandingan label aktual vs prediksi"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Dapatkan data
            analysis_page = self.app.pages["analysis"]
            results = analysis_page.current_results
            
            if not results or 'results' not in results:
                print_error("Tidak ada data hasil analisis!")
                return
            
            data = results['results']
            
            # Filter data dengan label aktual
            labeled_data = [r for r in data if r['actual_label'] != 'unknown']
            
            if not labeled_data:
                print_error("Tidak ada data dengan label aktual!")
                return
            
            # Buat confusion matrix
            from collections import Counter
            
            categories = ['phishing', 'legitimate']
            confusion = {actual: {pred: 0 for pred in categories} for actual in categories}
            
            for result in labeled_data:
                actual = result['actual_label'].lower()
                predicted = result['predicted_label'].lower()
                
                if actual in categories and predicted in categories:
                    confusion[actual][predicted] += 1
            
            # Siapkan data untuk heatmap
            matrix = [[confusion['phishing']['phishing'], confusion['phishing']['legitimate']],
                     [confusion['legitimate']['phishing'], confusion['legitimate']['legitimate']]]
            
            # Buat heatmap
            plt.figure(figsize=(10, 8))
            
            sns.heatmap(matrix, annot=True, fmt='d', cmap='RdYlGn',
                       xticklabels=['Pred: Phishing', 'Pred: Legitimate'],
                       yticklabels=['Aktual: Phishing', 'Aktual: Legitimate'],
                       cbar_kws={'label': 'Jumlah URL'})
            
            plt.title('Confusion Matrix: Perbandingan Aktual vs Prediksi', fontsize=16, fontweight='bold')
            plt.xlabel('Prediksi Model')
            plt.ylabel('Label Aktual')
            
            plt.tight_layout()
            plt.show()
            
            # Hitung metrik
            tp = matrix[0][0]
            fp = matrix[1][0]
            tn = matrix[1][1]
            fn = matrix[0][1]
            
            accuracy = (tp + tn) / (tp + tn + fp + fn) * 100
            precision = tp / (tp + fp) * 100 if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) * 100 if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            # Tampilkan metrik
            print(f"\n{Colors.BOLD}📈 METRIK PERFORMA:{Colors.ENDC}")
            print(f"\n{Colors.OKCYAN}Berdasarkan {len(labeled_data)} URL dengan label aktual{Colors.ENDC}\n")
            
            print(f"{Colors.BOLD}Confusion Matrix:{Colors.ENDC}")
            print(f"                    Prediksi")
            print(f"                  Phishing  Legitimate")
            print(f"Aktual  Phishing     {tp:<4}       {fn:<4}")
            print(f"        Legitimate   {fp:<4}       {tn:<4}")
            
            print(f"\n{Colors.BOLD}Metrik:{Colors.ENDC}")
            print(f"  Akurasi:   {accuracy:.2f}%")
            print(f"  Precision: {precision:.2f}%")
            print(f"  Recall:    {recall:.2f}%")
            print(f"  F1-Score:  {f1:.2f}%")
            
            # Buat bar chart metrik
            plt.figure(figsize=(10, 6))
            
            metrics = ['Akurasi', 'Precision', 'Recall', 'F1-Score']
            values = [accuracy, precision, recall, f1]
            colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
            
            bars = plt.bar(metrics, values, color=colors, edgecolor='black', linewidth=2)
            
            plt.title('Metrik Performa Model', fontsize=16, fontweight='bold')
            plt.ylabel('Persentase (%)')
            plt.ylim(0, 100)
            
            # Tambahkan nilai di atas bar
            for bar, value in zip(bars, values):
                plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                        f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print_error("Modul seaborn tidak tersedia!")
            print_warning("Instal dengan: pip install seaborn")
        except Exception as e:
            print_error(f"Error menampilkan perbandingan: {str(e)}")
    
    def _show_time_analysis(self):
        """Tampilkan analisis trend waktu"""
        try:
            import matplotlib.pyplot as plt
            from datetime import datetime
            
            print_warning("Fitur ini memerlukan data timestamp pada dataset.")
            print("Untuk demo, menggunakan simulasi data waktu.")
            
            # Simulasi data waktu
            dates = []
            phishing_counts = []
            legitimate_counts = []
            
            # Generate data 30 hari terakhir
            import random
            from datetime import timedelta
            
            end_date = datetime.now()
            
            for i in range(30):
                date = end_date - timedelta(days=30-i)
                dates.append(date)
                
                # Simulasi random counts
                phishing_counts.append(random.randint(5, 20))
                legitimate_counts.append(random.randint(80, 120))
            
            # Buat line chart
            plt.figure(figsize=(14, 8))
            
            plt.subplot(2, 1, 1)
            plt.plot(dates, phishing_counts, 'r-', label='Phishing', linewidth=2, marker='o')
            plt.plot(dates, legitimate_counts, 'g-', label='Legitimate', linewidth=2, marker='s')
            
            plt.title('Trend Deteksi Harian (30 Hari Terakhir)', fontsize=14, fontweight='bold')
            plt.xlabel('Tanggal')
            plt.ylabel('Jumlah URL')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            
            # Buat stacked area chart
            plt.subplot(2, 1, 2)
            
            plt.stackplot(dates, phishing_counts, legitimate_counts,
                         labels=['Phishing', 'Legitimate'],
                         colors=['#ff6b6b', '#51cf66'], alpha=0.7)
            
            plt.title('Distribusi Kumulatif', fontsize=14, fontweight='bold')
            plt.xlabel('Tanggal')
            plt.ylabel('Jumlah URL (Kumulatif)')
            plt.legend(loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            
            plt.suptitle('Analisis Trend Waktu Deteksi Phishing', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.show()
            
            # Hitung statistik trend
            print(f"\n{Colors.BOLD}📊 STATISTIK TREND WAKTU:{Colors.ENDC}")
            
            # Moving average
            window_size = 7
            
            if len(phishing_counts) >= window_size:
                moving_avg = []
                for i in range(len(phishing_counts) - window_size + 1):
                    moving_avg.append(sum(phishing_counts[i:i+window_size]) / window_size)
                
                print(f"\n{Colors.FAIL}Rata-rata bergerak Phishing (7 hari):{Colors.ENDC}")
                print(f"  Terbaru: {moving_avg[-1]:.1f}")
                print(f"  Perubahan: {((moving_avg[-1] - moving_avg[0])/moving_avg[0]*100 if moving_avg[0] > 0 else 0):.1f}%")
            
            # Prediksi sederhana
            if len(phishing_counts) > 1:
                last_week_avg = sum(phishing_counts[-7:]) / min(7, len(phishing_counts))
                prev_week_avg = sum(phishing_counts[-14:-7]) / min(7, len(phishing_counts[-14:-7]))
                
                print(f"\n{Colors.BOLD}📈 ANALISIS PERBANDINGAN MINGGUAN:{Colors.ENDC}")
                print(f"  Minggu ini: {last_week_avg:.1f} phishing/hari")
                print(f"  Minggu lalu: {prev_week_avg:.1f} phishing/hari")
                
                if prev_week_avg > 0:
                    change = ((last_week_avg - prev_week_avg) / prev_week_avg) * 100
                    print(f"  Perubahan: {change:+.1f}%")
                    
                    if change > 10:
                        print(f"  {Colors.FAIL}⚠ Peringatan: Peningkatan signifikan dalam phishing!{Colors.ENDC}")
                    elif change < -10:
                        print(f"  {Colors.OKGREEN}✓ Penurunan signifikan dalam phishing{Colors.ENDC}")
            
        except Exception as e:
            print_error(f"Error menampilkan analisis waktu: {str(e)}")
    
    def _show_correlation_heatmap(self):
        """Tampilkan heatmap korelasi antar fitur"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            import pandas as pd
            import numpy as np
            
            # Dapatkan data
            analysis_page = self.app.pages["analysis"]
            results = analysis_page.current_results
            
            if not results or 'results' not in results:
                print_error("Tidak ada data hasil analisis!")
                return
            
            data = results['results']
            
            # Ambil sample untuk performa
            sample_size = min(100, len(data))
            sample_data = data[:sample_size]
            
            # Ekstrak fitur-fitur numerik
            features_list = []
            
            for result in sample_data:
                if 'features' in result:
                    features = result['features']
                    
                    # Pilih fitur numerik tertentu
                    selected_features = {
                        'url_length': features.get('url_length', 0),
                        'special_chars': features.get('special_chars', 0),
                        'numeric_ratio': features.get('numeric_ratio', 0) * 100,  # Konversi ke persen
                        'domain_dots': features.get('domain_dots', 0),
                        'hyphen_count': features.get('hyphen_count', 0),
                        'entropy': features.get('entropy', 0),
                        'has_https': features.get('has_https', 0),
                        'phishing_keywords': features.get('phishing_keywords', 0),
                        'is_phishing': 1 if result['predicted_label'] == 'phishing' else 0
                    }
                    
                    features_list.append(selected_features)
            
            if not features_list:
                print_error("Tidak dapat mengekstrak fitur numerik!")
                return
            
            # Buat DataFrame
            df = pd.DataFrame(features_list)
            
            # Hitung matriks korelasi
            correlation_matrix = df.corr()
            
            # Buat heatmap
            plt.figure(figsize=(12, 10))
            
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            
            sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                       center=0, square=True, linewidths=1, cbar_kws={"shrink": .8})
            
            plt.title('Heatmap Korelasi Antar Fitur', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.show()
            
            # Tampilkan korelasi tinggi
            print(f"\n{Colors.BOLD}📊 KORELASI TERTINGGI DENGAN 'is_phishing':{Colors.ENDC}")
            
            phishing_correlations = correlation_matrix['is_phishing'].sort_values(ascending=False)
            
            for feature, corr in phishing_correlations.items():
                if feature != 'is_phishing':
                    corr_abs = abs(corr)
                    
                    if corr_abs > 0.3:
                        color = Colors.FAIL if corr_abs > 0.5 else Colors.WARNING
                        direction = "positif" if corr > 0 else "negatif"
                        
                        print(f"\n{color}{feature}: {corr:.3f} ({direction}){Colors.ENDC}")
                        
                        # Interpretasi
                        if feature == 'special_chars' and corr > 0:
                            print(f"  Interpretasi: Semakin banyak karakter khusus, semakin mungkin phishing")
                        elif feature == 'has_https' and corr < 0:
                            print(f"  Interpretasi: HTTPS mengurangi kemungkinan phishing")
                        elif feature == 'phishing_keywords' and corr > 0:
                            print(f"  Interpretasi: Kata kunci phishing meningkatkan probabilitas")
                        elif feature == 'entropy' and corr > 0:
                            print(f"  Interpretasi: Entropy tinggi terkait dengan URL phishing")
            
            # Analisis multivariate
            print(f"\n{Colors.BOLD}🔍 ANALISIS MULTIVARIATE:{Colors.ENDC}")
            
            # Cari fitur dengan korelasi tinggi antar mereka sendiri
            high_corr_pairs = []
            
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr = abs(correlation_matrix.iloc[i, j])
                    if corr > 0.7:  # Threshold untuk korelasi tinggi
                        feat1 = correlation_matrix.columns[i]
                        feat2 = correlation_matrix.columns[j]
                        high_corr_pairs.append((feat1, feat2, corr))
            
            if high_corr_pairs:
                print(f"\n{Colors.WARNING}⚠ Fitur dengan korelasi tinggi (multikolinearitas):{Colors.ENDC}")
                for feat1, feat2, corr in high_corr_pairs:
                    print(f"  {feat1} ↔ {feat2}: {corr:.3f}")
                
                print(f"\n{Colors.OKCYAN}Saran: Pertimbangkan untuk menghapus salah satu fitur yang berkorelasi tinggi{Colors.ENDC}")
            
        except ImportError:
            print_error("Modul seaborn atau pandas tidak tersedia!")
            print_warning("Instal dengan: pip install seaborn pandas")
        except Exception as e:
            print_error(f"Error menampilkan heatmap: {str(e)}")