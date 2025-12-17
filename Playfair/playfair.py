import os
import math

# --- PHẦN 1: LOGIC TÁCH TỪ (WORD SEGMENTATION) ---
class WordSegmenter:
    def __init__(self, dictionary_file='words.txt'):
        self.words = set()
        self.word_costs = {}
        self.max_word_len = 0
        self.total_words = 0
        
        # Thử load từ điển
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, dictionary_file)
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    self.words.add(word)
                    self.max_word_len = max(self.max_word_len, len(word))
                    self.total_words += 1
            
            # Tính "chi phí" cho mỗi từ (dựa trên định luật Zipf - từ càng phổ biến chi phí càng thấp)
            # Ở đây ta giả lập chi phí đơn giản bằng logarit
            for word in self.words:
                self.word_costs[word] = math.log((self.total_words + 1) * 10) 
        else:
            print(f"⚠️ Cảnh báo: Không tìm thấy file '{dictionary_file}'. Tính năng tách từ sẽ không hoạt động.")

    def segment(self, text):
        """Dùng quy hoạch động (Dynamic Programming) để tìm cách tách từ tối ưu nhất"""
        if not self.words:
            return text # Trả về nguyên gốc nếu không có từ điển

        text = text.lower()
        n = len(text)
        # cost[i] là chi phí thấp nhất để tách đoạn text[:i]
        cost = [0] + [float('inf')] * n
        
        # result[i] lưu vị trí cắt từ cuối cùng để truy vết
        result = [0] * (n + 1)

        for i in range(1, n + 1):
            # Chỉ xét các từ có độ dài hợp lý để tối ưu tốc độ
            for j in range(max(0, i - self.max_word_len), i):
                word = text[j:i]
                if word in self.words:
                    # Chi phí của từ này (giả sử bằng len nếu không có freq, hoặc dùng hàm log)
                    # Ở đây dùng logic đơn giản: ưu tiên từ dài và hợp lệ
                    word_cost = cost[j] + 1 
                    
                    if word_cost < cost[i]:
                        cost[i] = word_cost
                        result[i] = j
        
        # Truy vết để tạo lại câu
        out = []
        i = n
        while i > 0:
            j = result[i]
            if cost[i] == float('inf'): # Trường hợp không tìm thấy từ hợp lệ
                # Cố gắng lùi 1 ký tự (xử lý tên riêng hoặc từ lạ)
                out.append(text[i-1:i]) 
                i -= 1
            else:
                out.append(text[j:i])
                i = j
        
        return " ".join(reversed(out)).upper()

# Khởi tạo instance toàn cục để không phải load file nhiều lần
# Bạn cần tải file 'words.txt' để cùng thư mục
segmenter = WordSegmenter('words.txt')


# --- PHẦN 2: LOGIC PLAYFAIR CŨ (GIỮ NGUYÊN & CẢI TIẾN) ---

def create_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    seen = set()
    
    for char in key:
        if char not in seen and 'A' <= char <= 'Z':
            matrix.append(char)
            seen.add(char)
            
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in seen:
            matrix.append(char)
            seen.add(char)
            
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for r, row in enumerate(matrix):
        if char in row:
            return r, row.index(char)
    return None

def prepare_text(text, encrypt=True):
    text = text.upper().replace("J", "I")
    clean_text = "".join([c for c in text if c.isalpha()])
    
    if not encrypt:
        return clean_text
        
    pairs = []
    i = 0
    while i < len(clean_text):
        a = clean_text[i]
        b = ''
        if (i + 1) < len(clean_text):
            b = clean_text[i + 1]
            
        if a == b:
            pairs.append(a + 'X')
            i += 1
        elif b == '':
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
            
    return "".join(pairs)

def process_playfair(text, key, mode='encrypt'):
    if not text or not key:
        return ""
        
    matrix = create_matrix(key)
    prepared_text = prepare_text(text, encrypt=(mode == 'encrypt'))
    result = []
    
    shift = 1 if mode == 'encrypt' else -1
    
    for i in range(0, len(prepared_text), 2):
        if i+1 >= len(prepared_text): break 
        
        char1 = prepared_text[i]
        char2 = prepared_text[i+1]
        
        pos1 = find_position(matrix, char1)
        pos2 = find_position(matrix, char2)

        if not pos1 or not pos2: 
            continue

        row1, col1 = pos1
        row2, col2 = pos2
        
        if row1 == row2:
            r1_new, c1_new = row1, (col1 + shift) % 5
            r2_new, c2_new = row2, (col2 + shift) % 5
        elif col1 == col2:
            r1_new, c1_new = (row1 + shift) % 5, col1
            r2_new, c2_new = (row2 + shift) % 5, col2
        else:
            r1_new, c1_new = row1, col2
            r2_new, c2_new = row2, col1
            
        result.append(matrix[r1_new][c1_new])
        result.append(matrix[r2_new][c2_new])
        
    raw_result = "".join(result)
    
    # --- CẢI TIẾN: NẾU LÀ GIẢI MÃ, HÃY THỬ KHÔI PHỤC DẤU CÁCH ---
    if mode == 'decrypt':
        # 1. Thử tách từ bằng từ điển
        segmented_result = segmenter.segment(raw_result)
        return segmented_result
        
    return raw_result