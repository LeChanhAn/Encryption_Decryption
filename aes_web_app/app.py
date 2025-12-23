from flask import Flask, render_template, request
import aes_pure_python as aes
import re # Thêm thư viện regex

app = Flask(__name__)
app.secret_key = 'aes_secret_key_demo'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    iv_result = ""
    error = None
    
    form_data = {
        'input_text': '',
        'key': '',
        'iv': '',
        'mode': 'cbc',
        'action': 'encrypt'
    }

    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            input_text = request.form.get('input_text', '')
            key_str = request.form.get('key', '').strip()
            iv_hex = request.form.get('iv', '').strip()
            mode = request.form.get('mode')
            action = request.form.get('action')

            # Cập nhật form data
            form_data.update({
                'input_text': input_text,
                'key': key_str,
                'iv': iv_hex,
                'mode': mode,
                'action': action
            })

            # --- SỬA LOGIC XỬ LÝ KEY (Hỗ trợ 32 Hex hoặc 16 Text) ---
            key_bytes = None
            
            # Trường hợp 1: Key là 32 ký tự Hex
            if len(key_str) == 32 and re.fullmatch(r'[0-9A-Fa-f]+', key_str):
                try:
                    key_bytes = bytes.fromhex(key_str)
                except:
                    pass
            
            # Trường hợp 2: Key là 16 ký tự văn bản thường (Fallback)
            if key_bytes is None:
                if len(key_str) == 16:
                     key_bytes = key_str.encode('utf-8')
                else:
                    raise ValueError("Key phải là 32 ký tự HEX hoặc 16 ký tự văn bản!")

            # --------------------------------------------------------

            # 2. Xử lý logic Mã hóa / Giải mã
            if action == 'encrypt':
                plain_bytes = input_text.encode('utf-8')
                iv_holder = bytearray() 
                
                if mode == 'cbc':
                    cipher_bytes = aes.aes_cbc_encrypt(plain_bytes, key_bytes, iv_holder)
                else: # cfb
                    cipher_bytes = aes.aes_cfb_encrypt(plain_bytes, key_bytes, iv_holder)
                
                result = aes.to_hex(cipher_bytes)
                iv_result = aes.to_hex(bytes(iv_holder))

            elif action == 'decrypt':
                try:
                    cipher_bytes = aes.from_hex(input_text.strip())
                    iv_bytes = aes.from_hex(iv_hex.strip())
                except:
                    raise ValueError("Ciphertext hoặc IV phải là chuỗi Hex hợp lệ!")

                if len(iv_bytes) != 16:
                    raise ValueError("IV phải đúng 16 bytes (32 ký tự Hex)!")

                if mode == 'cbc':
                    plain_bytes = aes.aes_cbc_decrypt(cipher_bytes, key_bytes, iv_bytes)
                else: # cfb
                    plain_bytes = aes.aes_cfb_decrypt(cipher_bytes, key_bytes, iv_bytes)
                
                result = plain_bytes.decode('utf-8')

        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, iv_result=iv_result, error=error, form=form_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)