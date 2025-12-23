from flask import Flask, render_template, request
import playfair

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = ""
    input_text = ""
    key_text = ""
    mode = ""

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        input_text = request.form.get('input_text', '').strip()
        key_text = request.form.get('key_text', '').strip()
        action = request.form.get('action') # 'encrypt' hoặc 'decrypt'

        if input_text and key_text:
            if action == 'encrypt':
                mode = "MÃ HÓA (ENCRYPTION)"
                # Gọi hàm mã hóa
                result_text = playfair.process_playfair(input_text, key_text, mode='encrypt')
            elif action == 'decrypt':
                mode = "GIẢI MÃ (DECRYPTION)"
                # Gọi hàm giải mã
                result_text = playfair.process_playfair(input_text, key_text, mode='decrypt')

    return render_template('index.html', 
                           input_text=input_text, 
                           key_text=key_text, 
                           result_text=result_text,
                           mode=mode)

if __name__ == '__main__':
    app.run(debug=True, port=5000)