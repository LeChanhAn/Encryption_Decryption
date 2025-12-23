import random
import math
import os
from collections import Counter

class MonoalphabeticCipherBreaker:
    # hàm này là khởi tạo, load bảng tần suất quadgram từ file
    def __init__(self, quadgram_file):
        self.english_freq = {
            'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02, 'h': 5.92, 'd': 4.32,
            'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49, 
            'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.10, 'z': 0.07,
        }
        self.quadgram_logs = {}
        self.floor = -20.0 
        self._load_quadgram_stats(quadgram_file)

    def _load_quadgram_stats(self, filename):
        quad_counts = {}
        total_count = 0
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File not found at: {filename}")

            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) == 2:
                        quad = parts[0].lower()
                        count = int(parts[1])
                        quad_counts[quad] = count
                        total_count += count

            for quad, count in quad_counts.items():
                self.quadgram_logs[quad] = math.log10(float(count) / total_count)
            
            if quad_counts:
                min_prob = math.log10(0.01 / total_count)
                self.floor = min_prob
                        
        except Exception as e:
            print(f"ERROR: Unable to read quadgrams file. {e}")
            self.quadgram_logs = {'tion': -2.0, 'ther': -2.1, 'that': -2.2}
            self.floor = -10.0

    def analyze_text(self, text):
        text = text.lower()
        letters = [c for c in text if c.isalpha()]
        char_freq = Counter(letters)
        total = sum(char_freq.values())
        return {k: (v/total)*100 for k, v in char_freq.items()}
    
    def create_initial_key(self, ciphertext):
        char_freq = self.analyze_text(ciphertext)
        sorted_cipher = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)
        sorted_english = sorted(self.english_freq.items(), key=lambda x: x[1], reverse=True)
        
        key = {}
        for i, (cipher_char, _) in enumerate(sorted_cipher):
            if i < len(sorted_english):
                key[cipher_char] = sorted_english[i][0]
        
        all_letters = set('abcdefghijklmnopqrstuvwxyz')
        used = set(key.values())
        unused = list(all_letters - used)
        
        for char in all_letters:
            if char not in key:
                key[char] = unused.pop(0) if unused else char
        return key
    
    def decrypt_with_key(self, ciphertext, key):
        result = []
        for char in ciphertext:
            if char.isalpha():
                decrypted = key.get(char.lower(), char.lower())
                result.append(decrypted.upper() if char.isupper() else decrypted)
            else:
                result.append(char)
        return ''.join(result)
    
    def calculate_fitness(self, text):
        text_lower = "".join([c for c in text.lower() if c.isalpha()])
        score = 0
        
        if len(text_lower) < 4:
            return -1000.0
            
        for i in range(len(text_lower) - 3):
            quad = text_lower[i:i+4]
            score += self.quadgram_logs.get(quad, self.floor)
            
        return score
    
    def swap_keys(self, key):
        new_key = key.copy()
        keys_list = list(key.keys())
        if len(keys_list) >= 2:
            k1, k2 = random.sample(keys_list, 2)
            new_key[k1], new_key[k2] = new_key[k2], new_key[k1]
        return new_key
    
    def hill_climbing(self, ciphertext, iterations=10000):
        current_key = self.create_initial_key(ciphertext)
        current_text = self.decrypt_with_key(ciphertext, current_key)
        current_score = self.calculate_fitness(current_text)
        
        no_improvement_count = 0
        
        for i in range(iterations):
            new_key = self.swap_keys(current_key)
            new_text = self.decrypt_with_key(ciphertext, new_key)
            new_score = self.calculate_fitness(new_text)
            
            if new_score > current_score:
                current_score = new_score
                current_key = new_key
                current_text = new_text
                no_improvement_count = 0
            else:
                no_improvement_count += 1
            
            if no_improvement_count > 1500: 
                break 

        return current_key, current_text, current_score

def solve_cipher_web(ciphertext):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    quad_path = os.path.join(base_dir, 'source', 'english_quadgrams.txt')
    output_path = os.path.join(base_dir, 'plaintext.txt') # <-- Đường dẫn file output
    
    breaker = MonoalphabeticCipherBreaker(quad_path)
    best_key, plaintext, score = breaker.hill_climbing(ciphertext)
    
    sorted_key = dict(sorted(best_key.items()))
    
    # TẠO VÀ GHI VÀO FILE plaintext.txt
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            # Ghi thông tin khóa
            f.write("--- KEY (BẢNG THAY THẾ) ---\n")
            key_str = " | ".join([f"{k.upper()}->{v.upper()}" for k, v in sorted_key.items()])
            f.write(key_str + "\n\n")
            
            # Ghi điểm số
            f.write(f"Fitness Score: {score:.2f}\n")
            f.write("-" * 50 + "\n\n")
            
            # Ghi Plaintext
            f.write("--- PLAINTEXT ---\n")
            f.write(plaintext)
            
        print(f"✅ Đã lưu kết quả vào: {output_path}")
        
    except Exception as e:
        print(f"Lỗi khi ghi file: {e}")

    return {
        "key": sorted_key,
        "plaintext": plaintext,
        "score": score
    }