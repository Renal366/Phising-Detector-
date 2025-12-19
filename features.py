"""
EKSTRAKSI FITUR - PREPROCESSING URL
Modul untuk mengekstrak fitur-fitur penting dari URL.
"""

from urllib.parse import urlparse
import math
import re
from typing import Dict, Optional, Tuple

class FeatureExtractor:
    """
    Ekstraktor fitur untuk analisis URL.
    Mengekstrak berbagai fitur struktural dan statistik dari URL.
    """
    
    def __init__(self):
        """Inisialisasi ekstraktor fitur"""
        self.common_phishing_keywords = [
            'login', 'verify', 'secure', 'account', 'banking',
            'confirm', 'update', 'payment', 'signin', 'authenticate',
            'password', 'credential', 'validation', 'suspend', 'locked'
        ]
        
        self.legitimate_domains = [
            'google.com', 'facebook.com', 'amazon.com', 'github.com',
            'microsoft.com', 'apple.com', 'paypal.com', 'netflix.com'
        ]
    
    def extract_all_features(self, url: str) -> Optional[Dict]:
        """
        Ekstrak semua fitur dari sebuah URL.
        
        Args:
            url: URL string untuk dianalisis
            
        Returns:
            Dictionary berisi semua fitur yang diekstrak
        """
        try:
            if not url or not isinstance(url, str):
                return None
            
            # Parse URL
            parsed = urlparse(url)
            domain = parsed.netloc
            path = parsed.path
            
            # Ekstrak fitur-fitur
            features = {}
            
            # 1. Fitur panjang
            features.update(self._extract_length_features(url, domain, path))
            
            # 2. Fitur karakter
            features.update(self._extract_character_features(url, domain))
            
            # 3. Fitur struktural
            features.update(self._extract_structural_features(parsed, domain))
            
            # 4. Fitur statistik
            features.update(self._extract_statistical_features(url, domain))
            
            # 5. Fitur semantik
            features.update(self._extract_semantic_features(url, domain))
            
            # 6. Fitur entropy
            features.update(self._extract_entropy_features(url))
            
            return features
            
        except Exception as e:
            print(f"Error dalam ekstraksi fitur: {str(e)}")
            return None
    
    def _extract_length_features(self, url: str, domain: str, path: str) -> Dict:
        """
        Ekstrak fitur-fitur terkait panjang URL.
        
        Args:
            url: Full URL
            domain: Domain string
            path: Path string
            
        Returns:
            Dictionary fitur panjang
        """
        return {
            'url_length': len(url),
            'domain_length': len(domain),
            'path_length': len(path),
            'avg_segment_length': self._calculate_avg_segment_length(domain),
            'max_segment_length': self._calculate_max_segment_length(domain)
        }
    
    def _extract_character_features(self, url: str, domain: str) -> Dict:
        """
        Ekstrak fitur-fitur terkait karakter dalam URL.
        
        Args:
            url: Full URL
            domain: Domain string
            
        Returns:
            Dictionary fitur karakter
        """
        return {
            'special_chars': len(re.findall(r'[!@#$%^&*()_+\-=\[\]{};\'":|,.<>?\\]', url)),
            'numeric_chars': len(re.findall(r'\d', url)),
            'numeric_ratio': len(re.findall(r'\d', url)) / len(url) if url else 0,
            'vowel_ratio': len(re.findall(r'[aeiouAEIOU]', domain)) / len(domain) if domain else 0,
            'consonant_ratio': len(re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]', domain)) / len(domain) if domain else 0,
            'hyphen_count': url.count('-'),
            'underscore_count': url.count('_'),
            'at_symbol': url.count('@'),
            'slash_count': url.count('/'),
            'space_count': url.count(' ')
        }
    
    def _extract_structural_features(self, parsed, domain: str) -> Dict:
        """
        Ekstrak fitur-fitur struktural URL.
        
        Args:
            parsed: Parsed URL object
            domain: Domain string
            
        Returns:
            Dictionary fitur struktural
        """
        return {
            'has_https': 1 if parsed.scheme == 'https' else 0,
            'has_http': 1 if parsed.scheme == 'http' else 0,
            'domain_dots': domain.count('.'),
            'has_port': 1 if parsed.port else 0,
            'has_query': 1 if parsed.query else 0,
            'has_fragment': 1 if parsed.fragment else 0,
            'has_subdomain': 1 if len(domain.split('.')) > 2 else 0,
            'subdomain_count': len(domain.split('.')) - 2 if len(domain.split('.')) > 2 else 0,
            'is_ip_address': 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain) else 0
        }
    
    def _extract_statistical_features(self, url: str, domain: str) -> Dict:
        """
        Ekstrak fitur-fitur statistik URL.
        
        Args:
            url: Full URL
            domain: Domain string
            
        Returns:
            Dictionary fitur statistik
        """
        char_freq = {}
        for char in url:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        return {
            'char_variance': self._calculate_variance(list(char_freq.values())),
            'digit_sequence': self._count_digit_sequences(url),
            'letter_sequence': self._count_letter_sequences(url),
            'special_sequence': self._count_special_sequences(url)
        }
    
    def _extract_semantic_features(self, url: str, domain: str) -> Dict:
        """
        Ekstrak fitur-fitur semantik URL.
        
        Args:
            url: Full URL
            domain: Domain string
            
        Returns:
            Dictionary fitur semantik
        """
        keyword_count = 0
        for keyword in self.common_phishing_keywords:
            if keyword.lower() in url.lower():
                keyword_count += 1
        
        is_legitimate_domain = 0
        for legit_domain in self.legitimate_domains:
            if legit_domain in domain.lower():
                is_legitimate_domain = 1
                break
        
        return {
            'phishing_keywords': keyword_count,
            'is_legitimate_domain': is_legitimate_domain,
            'has_brand_name': self._check_brand_name(url),
            'suspicious_tld': self._check_suspicious_tld(domain)
        }
    
    def _extract_entropy_features(self, url: str) -> Dict:
        """
        Ekstrak fitur-fitur entropy URL.
        
        Args:
            url: Full URL
            
        Returns:
            Dictionary fitur entropy
        """
        return {
            'entropy': self._calculate_entropy(url),
            'domain_entropy': self._calculate_entropy(urlparse(url).netloc),
            'path_entropy': self._calculate_entropy(urlparse(url).path)
        }
    
    # ===== HELPER METHODS =====
    
    def _calculate_avg_segment_length(self, domain: str) -> float:
        """Hitung rata-rata panjang segment domain"""
        segments = domain.split('.')
        if not segments:
            return 0
        return sum(len(seg) for seg in segments) / len(segments)
    
    def _calculate_max_segment_length(self, domain: str) -> int:
        """Hitung panjang maksimum segment domain"""
        segments = domain.split('.')
        return max(len(seg) for seg in segments) if segments else 0
    
    def _calculate_variance(self, values: list) -> float:
        """Hitung variance dari list nilai"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _count_digit_sequences(self, text: str) -> int:
        """Hitung jumlah sequence digit berurutan"""
        return len(re.findall(r'\d{3,}', text))
    
    def _count_letter_sequences(self, text: str) -> int:
        """Hitung jumlah sequence huruf berurutan"""
        return len(re.findall(r'[a-zA-Z]{10,}', text))
    
    def _count_special_sequences(self, text: str) -> int:
        """Hitung jumlah sequence karakter khusus berurutan"""
        return len(re.findall(r'[!@#$%^&*()_+\-=\[\]{};\'":|,.<>?\\]{2,}', text))
    
    def _check_brand_name(self, url: str) -> int:
        """Cek apakah URL mengandung nama brand populer"""
        brands = ['google', 'facebook', 'amazon', 'microsoft', 'apple', 'paypal']
        url_lower = url.lower()
        for brand in brands:
            if brand in url_lower:
                return 1
        return 0
    
    def _check_suspicious_tld(self, domain: str) -> int:
        """Cek apakah domain menggunakan TLD yang mencurigakan"""
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.club']
        for tld in suspicious_tlds:
            if domain.endswith(tld):
                return 1
        return 0
    
    def _calculate_entropy(self, text: str) -> float:
        """Hitung entropy Shannon dari sebuah string"""
        if not text:
            return 0
        
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        
        entropy = 0
        text_len = len(text)
        for count in freq.values():
            p = count / text_len
            entropy -= p * math.log2(p)
        
        return entropy