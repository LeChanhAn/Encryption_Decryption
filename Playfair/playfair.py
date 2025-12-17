# playfair.py

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
        if i+1 >= len(prepared_text): break # Safety check
        
        char1 = prepared_text[i]
        char2 = prepared_text[i+1]
        
        pos1 = find_position(matrix, char1)
        pos2 = find_position(matrix, char2)

        # Trường hợp ký tự lạ không có trong bảng (dù đã lọc)
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
        
    return "".join(result)