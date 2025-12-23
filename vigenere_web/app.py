from flask import Flask, render_template, request
import vigenere
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    key = None
    plaintext = ""
    ciphertext = ""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(base_dir, 'ciphertext.txt')

    if request.method == 'GET':
        if os.path.exists(input_file_path):
            try:
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    ciphertext = f.read().strip()
            except:
                pass

    if request.method == 'POST':
        ciphertext = request.form.get('ciphertext', '')
        
        if ciphertext:
            result = vigenere.solve_cipher_web(ciphertext)
            
            key = result.get('key')
            plaintext = result.get('plaintext')
            
            try:
                with open(input_file_path, 'w', encoding='utf-8') as f:
                    f.write(ciphertext)
            except:
                pass

    return render_template('index.html', key=key, plaintext=plaintext, ciphertext=ciphertext)

if __name__ == '__main__':
    app.run(debug=True, port=5000)