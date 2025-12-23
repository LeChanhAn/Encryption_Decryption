from flask import Flask, render_template, request
import des_module as des
import binascii
import re

app = Flask(__name__)

# --- BỎ HÀM normalize_key/iv Ở ĐÂY VÌ MODULE ĐÃ CÓ ---
# Chúng ta chỉ cần kiểm tra format bằng regex để báo lỗi đẹp hơn cho UI thôi

def validate_hex_format(hex_str, name="Giá trị"):
    if not re.fullmatch(r"[0-9A-Fa-f]{16}", hex_str):
        raise ValueError(f"{name} phải gồm đúng 16 ký tự HEX (0-9, A-F)!")
    return hex_str

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    iv_result = ""
    error = None
    
    form_data = {
        'input_text': '',
        'key': '',
        'iv': '',
        'mode': 'CBC',
        'action': 'encrypt'
    }

    if request.method == 'POST':
        try:
            input_text = request.form.get('input_text', '')
            key_hex = request.form.get('key', '').strip()
            iv_hex = request.form.get('iv', '').strip()
            mode = request.form.get('mode')
            action = request.form.get('action')

            form_data.update({
                'input_text': input_text,
                'key': key_hex,
                'iv': iv_hex,
                'mode': mode,
                'action': action
            })

            # 1. KIỂM TRA INPUT (Validate)
            validate_hex_format(key_hex, "Khóa (Key)")
            
            # 2. XỬ LÝ
            if action == 'encrypt':
                plaintext_bytes = input_text.encode('utf-8')

                # SỬA LẠI: Truyền thẳng key_hex (string), KHÔNG convert sang bytes
                ct_hex, new_iv = des.encrypt(plaintext_bytes, key_hex, mode, iv_hex if iv_hex else None)

                result = ct_hex
                if new_iv:
                    iv_result = new_iv 

            elif action == 'decrypt':
                # Kiểm tra ciphertext có phải hex không
                try:
                    binascii.unhexlify(input_text.strip())
                except:
                    raise ValueError("Ciphertext phải là chuỗi Hex hợp lệ!")

                if mode == 'CBC':
                    if not iv_hex:
                        raise ValueError("Giải mã CBC bắt buộc phải nhập IV!")
                    validate_hex_format(iv_hex, "IV") # Validate IV
                    
                    # SỬA LẠI: Truyền thẳng key_hex và iv_hex (string)
                    pt_text = des.decrypt(input_text.strip(), key_hex, mode, iv_hex)
                else:
                    # SỬA LẠI: Truyền thẳng key_hex
                    pt_text = des.decrypt(input_text.strip(), key_hex, mode)

                result = pt_text

        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, iv_result=iv_result, error=error, form=form_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)