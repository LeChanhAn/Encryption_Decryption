import string
import os

# Tần suất chữ cái tiếng Anh chuẩn (A-Z)
english_freq = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]

def ic(text):
    text = text.upper()
    freq = [0] * 26
    N = 0
    for c in text:
        if 'A' <= c <= 'Z':
            freq[ord(c) - ord('A')] += 1
            N += 1
    if N < 2:
        return 0
    sum_val = sum(f * (f - 1) for f in freq)
    return sum_val / (N * (N - 1))

def chi_square(freq, expected):
    chi = 0
    for i in range(26):
        if expected[i] > 0:
            chi += (freq[i] - expected[i]) ** 2 / expected[i]
    return chi

def find_key_length(letters, max_m=20): 
    best_m = 1
    best_ic = 0
    for m in range(1, max_m + 1):
        subsets = ['' for _ in range(m)]
        for i, c in enumerate(letters):
            subsets[i % m] += c
        avg_ic = sum(ic(s) for s in subsets) / m
        
        if avg_ic > best_ic:
            best_ic = avg_ic
            best_m = m
    return best_m

def find_key_from_subsets(subsets):
    key = ''
    for s in subsets:
        freq = [0] * 26
        for c in s:
            freq[ord(c) - ord('A')] += 1
        total = len(s)
        expected = [total * english_freq[i] for i in range(26)]
        
        best_shift = 0
        best_chi = float('inf')
        
        for shift in range(26):
            new_freq = [0] * 26
            for j in range(26):
                new_freq[(j - shift) % 26] += freq[j]
            chi = chi_square(new_freq, expected)
            if chi < best_chi:
                best_chi = chi
                best_shift = shift
        key += chr(best_shift + ord('A'))
    return key

def decrypt_vigenere(ciphertext, key):
    plaintext = []
    key_len = len(key)
    key_index = 0
    for c in ciphertext:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            k_char = key[key_index % key_len].upper()
            shift = ord(k_char) - ord('A')
            decrypted = chr((ord(c) - base - shift) % 26 + base)
            plaintext.append(decrypted)
            key_index += 1
        else:
            plaintext.append(c)
    return "".join(plaintext)


def solve_cipher_web(ciphertext):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, 'plaintext.txt')

    if not ciphertext:
        return {"key": "", "plaintext": "", "error": "No input text"}

    letters = ''.join(c for c in ciphertext if c.isalpha()).upper()
    if not letters:
        return {"key": "", "plaintext": ciphertext, "error": "No letters found"}

    m = find_key_length(letters)
    subsets = ['' for _ in range(m)]
    for i, c in enumerate(letters):
        subsets[i % m] += c
    found_key = find_key_from_subsets(subsets)
    plaintext = decrypt_vigenere(ciphertext, found_key)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("--- VIGENERE CRACK RESULT ---\n")
            f.write(f"FOUND KEY: {found_key}\n")
            f.write("-" * 30 + "\n\n")
            f.write("--- PLAINTEXT ---\n")
            f.write(plaintext)
        
        print(f"✅ Đã lưu kết quả vào: {output_path}")

    except Exception as e:
        print(f"❌ Lỗi khi ghi file: {e}")

    return {
        "key": found_key,
        "plaintext": plaintext
    }

if __name__ == "__main__":
    input_filename = "ciphertext.txt"
    
    if not os.path.exists(input_filename):
        with open(input_filename, "w", encoding="utf-8") as f:
            f.write("RIJVS") 
        print(f"⚠️ Đã tạo file mẫu '{input_filename}'. Hãy thay đổi nội dung nếu muốn.")

    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"[-] Đang đọc file '{input_filename}'...")
        
        result = solve_cipher_web(content)
        
        print(f"\n[KẾT QUẢ TRẢ VỀ TỪ HÀM]:")
        print(f"Key: {result['key']}")
        print(f"Plaintext (preview): {result['plaintext'][:50]}...")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {input_filename}")