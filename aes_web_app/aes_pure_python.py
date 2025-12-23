
from typing import List, Tuple
import secrets
import sys

Byte = int
Block = List[Byte]  # length 16

# AES S-box
sbox = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

# inverse S-box
inv_sbox = [
  0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb,
  0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb,
  0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e,
  0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25,
  0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92,
  0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84,
  0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06,
  0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b,
  0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73,
  0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e,
  0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b,
  0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4,
  0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f,
  0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef,
  0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61,
  0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d
]

# Rcon
Rcon = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

# GF(2^8) multiply helpers
def xtime(x: Byte) -> Byte:
    x &= 0xFF
    return ((x << 1) ^ 0x1B) & 0xFF if (x & 0x80) else (x << 1) & 0xFF

def mul(a: Byte, b: Byte) -> Byte:
    res = 0
    a &= 0xFF
    b &= 0xFF
    while b:
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res & 0xFF

# Key expansion for AES-128: 16-byte key -> 176 bytes
def key_expansion(key: bytes) -> List[Byte]:
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes for AES-128")
    w = list(key)[:]
    bytes_produced = 16
    rcon_iter = 1
    while bytes_produced < 176:
        temp = w[bytes_produced-4:bytes_produced]
        if bytes_produced % 16 == 0:
            # rotate
            temp = temp[1:] + temp[:1]
            # sub
            temp = [sbox[t] for t in temp]
            # Rcon
            temp[0] ^= Rcon[rcon_iter]
            rcon_iter += 1
        for t in temp:
            w.append(w[bytes_produced - 16] ^ t)
            bytes_produced += 1
    return w 

# AddRoundKey (state is 4x4 list)
def add_round_key(state: List[List[Byte]], round_key: List[Byte], round_idx: int):
    rk_offset = round_idx * 16
    for c in range(4):
        for r in range(4):
            state[r][c] ^= round_key[rk_offset + c*4 + r]

# SubBytes / InvSubBytes
def sub_bytes(state: List[List[Byte]]):
    for r in range(4):
        for c in range(4):
            state[r][c] = sbox[state[r][c]]

def inv_sub_bytes(state: List[List[Byte]]):
    for r in range(4):
        for c in range(4):
            state[r][c] = inv_sbox[state[r][c]]

# ShiftRows / InvShiftRows
def shift_rows(state: List[List[Byte]]):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]

def inv_shift_rows(state: List[List[Byte]]):
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]

# MixColumns/InvMixColumns
def mix_columns(state: List[List[Byte]]):
    for c in range(4):
        a0 = state[0][c]; a1 = state[1][c]; a2 = state[2][c]; a3 = state[3][c]
        state[0][c] = (mul(0x02, a0) ^ mul(0x03, a1) ^ a2 ^ a3) & 0xFF
        state[1][c] = (a0 ^ mul(0x02, a1) ^ mul(0x03, a2) ^ a3) & 0xFF
        state[2][c] = (a0 ^ a1 ^ mul(0x02, a2) ^ mul(0x03, a3)) & 0xFF
        state[3][c] = (mul(0x03, a0) ^ a1 ^ a2 ^ mul(0x02, a3)) & 0xFF

def inv_mix_columns(state: List[List[Byte]]):
    for c in range(4):
        a0 = state[0][c]; a1 = state[1][c]; a2 = state[2][c]; a3 = state[3][c]
        state[0][c] = (mul(0x0e, a0) ^ mul(0x0b, a1) ^ mul(0x0d, a2) ^ mul(0x09, a3)) & 0xFF
        state[1][c] = (mul(0x09, a0) ^ mul(0x0e, a1) ^ mul(0x0b, a2) ^ mul(0x0d, a3)) & 0xFF
        state[2][c] = (mul(0x0d, a0) ^ mul(0x09, a1) ^ mul(0x0e, a2) ^ mul(0x0b, a3)) & 0xFF
        state[3][c] = (mul(0x0b, a0) ^ mul(0x0d, a1) ^ mul(0x09, a2) ^ mul(0x0e, a3)) & 0xFF

# Encrypt single 16-byte block
def aes_encrypt_block(inp: bytes, expanded_key: List[Byte]) -> bytes:
    if len(inp) != 16:
        raise ValueError("Block must be 16 bytes")
    # state column-major: state[r][c] = inp[c*4 + r]
    state = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            state[r][c] = inp[c*4 + r]
    add_round_key(state, expanded_key, 0)
    for rnd in range(1, 10):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, expanded_key, rnd)
    # final round
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, expanded_key, 10)
    out = bytearray(16)
    for r in range(4):
        for c in range(4):
            out[c*4 + r] = state[r][c]
    return bytes(out)

# Decrypt single 16-byte block
def aes_decrypt_block(inp: bytes, expanded_key: List[Byte]) -> bytes:
    if len(inp) != 16:
        raise ValueError("Block must be 16 bytes")
    state = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            state[r][c] = inp[c*4 + r]
    add_round_key(state, expanded_key, 10)
    for rnd in range(9, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, expanded_key, rnd)
        inv_mix_columns(state)
    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, expanded_key, 0)
    out = bytearray(16)
    for r in range(4):
        for c in range(4):
            out[c*4 + r] = state[r][c]
    return bytes(out)

# PKCS#7 padding/unpadding
def pkcs7_pad(data: bytes) -> bytes:
    block = 16
    pad = block - (len(data) % block)
    if pad == 0:
        pad = block
    return data + bytes([pad])*pad

def pkcs7_unpad(data: bytes) -> bytes:
    if not data or (len(data) % 16) != 0:
        raise ValueError("Invalid padded data")
    last = data[-1]
    pad = last
    if pad == 0 or pad > 16:
        raise ValueError("Invalid padding length")
    if data[-pad:] != bytes([last])*pad:
        raise ValueError("Invalid padding bytes")
    return data[:-pad]

# Generate secure random IV (16 bytes)
def gen_iv() -> bytes:
    return secrets.token_bytes(16)

# AES-CBC encrypt
def aes_cbc_encrypt(plaintext: bytes, key: bytes, iv_out: bytearray=None) -> bytes:
    expanded = key_expansion(key)
    data = pkcs7_pad(plaintext)
    if iv_out is None:
        iv = gen_iv()
    else:
        if len(iv_out) == 0:
            iv = gen_iv()
            iv_out.extend(iv)
        else:
            if len(iv_out) != 16:
                raise ValueError("IV must be 16 bytes")
            iv = bytes(iv_out)
    prev = bytearray(iv)
    out = bytearray()
    for i in range(0, len(data), 16):
        block = bytes([data[i+j] ^ prev[j] for j in range(16)])
        enc = aes_encrypt_block(block, expanded)
        out.extend(enc)
        prev = bytearray(enc)
    return bytes(out)

# AES-CBC decrypt
def aes_cbc_decrypt(ciphertext: bytes, key: bytes, iv_in: bytes) -> bytes:
    if len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext not multiple of block size")
    if len(iv_in) != 16:
        raise ValueError("IV (16 bytes) required for CBC decrypt")
    expanded = key_expansion(key)
    prev = bytearray(iv_in)
    out = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        dec = aes_decrypt_block(block, expanded)
        plain = bytes([dec[j] ^ prev[j] for j in range(16)])
        out.extend(plain)
        prev = bytearray(block)
    return pkcs7_unpad(bytes(out))

# AES-CFB-128 encrypt (full-block CFB)
def aes_cfb_encrypt(plaintext: bytes, key: bytes, iv_out: bytearray=None) -> bytes:
    expanded = key_expansion(key)
    if iv_out is None:
        iv = gen_iv()
    else:
        if len(iv_out) == 0:
            iv = gen_iv()
            iv_out.extend(iv)
        else:
            if len(iv_out) != 16:
                raise ValueError("IV must be 16 bytes")
            iv = bytes(iv_out)
    shiftreg = bytearray(iv)
    out = bytearray()
    stream = bytearray(16)
    si = 16 
    for i in range(len(plaintext)):
        if si == 16:
            stream = bytearray(aes_encrypt_block(bytes(shiftreg), expanded))
            si = 0
        c = plaintext[i] ^ stream[si]
        out.append(c)
        shiftreg = shiftreg[1:] + bytes([c])
        si += 1
    return bytes(out)

# AES-CFB-128 decrypt
def aes_cfb_decrypt(ciphertext: bytes, key: bytes, iv_in: bytes) -> bytes:
    if len(iv_in) != 16:
        raise ValueError("IV (16 bytes) required for CFB decrypt")
    expanded = key_expansion(key)
    shiftreg = bytearray(iv_in)
    out = bytearray()
    stream = bytearray(16)
    si = 16
    for i in range(len(ciphertext)):
        if si == 16:
            stream = bytearray(aes_encrypt_block(bytes(shiftreg), expanded))
            si = 0
        p = ciphertext[i] ^ stream[si]
        out.append(p)
        shiftreg = shiftreg[1:] + bytes([ciphertext[i]])
        si += 1
    return bytes(out)

# Helpers: hex encode/decode
def to_hex(b: bytes) -> str:
    return b.hex()

def from_hex(s: str) -> bytes:
    if len(s) % 2 != 0:
        raise ValueError("Invalid hex length")
    return bytes.fromhex(s)

# main
def main():
    try:
        plain = b"Hello AES in pure Python! This is a test message for CBC and CFB modes."
        key = b"thisisa128bitkey"  # 16 bytes
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes")

        print("=== AES-128-CBC demo ===")
        iv_holder = bytearray()
        ct = aes_cbc_encrypt(plain, key, iv_holder)
        print("IV (hex):", to_hex(bytes(iv_holder)))
        print("Ciphertext (hex):", to_hex(ct))
        pt = aes_cbc_decrypt(ct, key, bytes(iv_holder))
        print("Decrypted:", pt.decode('utf-8'))

        print("\n=== AES-128-CFB demo ===")
        iv_holder2 = bytearray()
        ct2 = aes_cfb_encrypt(plain, key, iv_holder2)
        print("IV (hex):", to_hex(bytes(iv_holder2)))
        print("Ciphertext (hex):", to_hex(ct2))
        pt2 = aes_cfb_decrypt(ct2, key, bytes(iv_holder2))
        print("Decrypted:", pt2.decode('utf-8'))

    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
