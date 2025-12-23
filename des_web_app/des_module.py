import os

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25
]

E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

P = [
    16, 7, 20, 21, 29,12, 28,17,
     1,15, 23,26, 5,18, 31,10,
     2, 8, 24,14,32,27,  3, 9,
    19,13,30, 6,22,11,  4,25
]

PC1 = [
    57,49,41,33,25,17, 9,
     1,58,50,42,34,26,18,
    10, 2,59,51,43,35,27,
    19,11, 3,60,52,44,36,
    63,55,47,39,31,23,15,
     7,62,54,46,38,30,22,
    14, 6,61,53,45,37,29,
    21,13, 5,28,20,12, 4
]

PC2 = [
    14,17,11,24, 1, 5,
     3,28,15, 6,21,10,
    23,19,12, 4,26, 8,
    16, 7,27,20,13, 2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

S_BOX = [
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    ],
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
    ],
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
    ],
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
    ],
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
    ],
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
    ],
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
    ],
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
    ]
]

def permute(block, table):
    return [block[x - 1] for x in table]

def string_to_bitlist(s):
    return [int(b) for byte in s for b in f"{byte:08b}"]

def bitlist_to_bytes(b):
    return bytes(int("".join(str(x) for x in b[i:i+8]), 2) for i in range(0, len(b), 8))

def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]

def feistel(right, subkey):
    expanded = permute(right, E)
    tmp = xor(expanded, subkey)
    out = []
    for i in range(8):
        block = tmp[i*6:(i+1)*6]
        row = (block[0] << 1) | block[5]
        col = int("".join(str(b) for b in block[1:5]), 2)
        out += [int(b) for b in f"{S_BOX[i][row][col]:04b}"]
    return permute(out, P)

def generate_keys(key):
    key_bits = string_to_bitlist(key)
    key_pc1 = permute(key_bits, PC1)
    left, right = key_pc1[:28], key_pc1[28:]

    shifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    keys = []

    for shift in shifts:
        left = left[shift:] + left[:shift]
        right = right[shift:] + right[:shift]
        keys.append(permute(left + right, PC2))

    return keys

def des_block(block, keys, encrypt=True):
    bits = string_to_bitlist(block)
    bits = permute(bits, IP)
    left, right = bits[:32], bits[32:]

    for i in range(16):
        k = keys[i] if encrypt else keys[15 - i]
        new_right = xor(left, feistel(right, k))
        left, right = right, new_right

    final = permute(right + left, FP)
    return bitlist_to_bytes(final)

def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    return data[:-data[-1]]

def des_ecb_encrypt(data, key):
    keys = generate_keys(key)
    data = pad(data)
    ct = b''
    for i in range(0, len(data), 8):
        ct += des_block(data[i:i+8], keys, True)
    return ct

def des_ecb_decrypt(data, key):
    keys = generate_keys(key)
    pt = b''
    for i in range(0, len(data), 8):
        pt += des_block(data[i:i+8], keys, False)
    return unpad(pt)

def des_cbc_encrypt(data, key, iv=None):
    keys = generate_keys(key)
    data = pad(data)

    if iv is None:
        iv = os.urandom(8)

    ct = b''
    prev = iv

    for i in range(0, len(data), 8):
        block = xor(string_to_bitlist(data[i:i+8]), string_to_bitlist(prev))
        block = bitlist_to_bytes(block)
        encrypted = des_block(block, keys, True)
        ct += encrypted
        prev = encrypted

    return ct, iv

def des_cbc_decrypt(ct, key, iv):
    keys = generate_keys(key)
    pt = b''
    prev = iv

    for i in range(0, len(ct), 8):
        block = des_block(ct[i:i+8], keys, False)
        block = xor(string_to_bitlist(block), string_to_bitlist(prev))
        pt += bitlist_to_bytes(block)
        prev = ct[i:i+8]

    return unpad(pt)

# Nhận key & IV 16 ký tự HEX

def normalize_key(key_str):
    if len(key_str) != 16:
        raise ValueError("Key phải có đúng 16 ký tự HEX.")
    return bytes.fromhex(key_str)

def normalize_iv(iv_str):
    if len(iv_str) != 16:
        raise ValueError("IV phải có đúng 16 ký tự HEX.")
    return bytes.fromhex(iv_str)


# API encrypt / decrypt

def encrypt(plaintext, key_hex, mode, iv_hex=None):
    key = normalize_key(key_hex)

    if mode == "ECB":
        return des_ecb_encrypt(plaintext, key).hex(), None

    elif mode == "CBC":
        iv = normalize_iv(iv_hex) if iv_hex else None
        ct, iv = des_cbc_encrypt(plaintext, key, iv)
        return ct.hex(), iv.hex()

    else:
        raise ValueError("Mode phải là ECB hoặc CBC.")

def decrypt(ciphertext_hex, key_hex, mode, iv_hex=None):
    key = normalize_key(key_hex)
    ct = bytes.fromhex(ciphertext_hex)

    if mode == "ECB":
        return des_ecb_decrypt(ct, key).decode()

    elif mode == "CBC":
        if iv_hex is None:
            raise ValueError("Giải mã CBC cần IV!")
        iv = normalize_iv(iv_hex)
        return des_cbc_decrypt(ct, key, iv).decode()

    else:
        raise ValueError("Mode phải là ECB hoặc CBC.")

# ============================
# TEST DEMO
# ============================

if __name__ == "__main__":
    key = "0123456789ABCDEF"      # 16 hex chars
    iv  = "A1B2C3D4E5F60708"      # 16 hex chars
    plaintext = b"Hello DES pure Python!"

    print("=== DES-ECB ===")
    ct, _ = encrypt(plaintext, key, "ECB")
    print("Ciphertext:", ct)
    print("Decrypted:", decrypt(ct, key, "ECB"))

    print("\n=== DES-CBC ===")
    ct, new_iv = encrypt(plaintext, key, "CBC", iv)
    print("IV:", new_iv)
    print("Ciphertext:", ct)
    print("Decrypted:", decrypt(ct, key, "CBC", new_iv))
