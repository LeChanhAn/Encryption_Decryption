from flask import Flask, render_template, request
import mono_decrypt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    ciphertext = ""
    error = None

    if request.method == 'POST':
        ciphertext = request.form.get('ciphertext', '')
        
        if ciphertext:
            try:
                result = mono_decrypt.solve_cipher_web(ciphertext)
            except Exception as e:
                error = str(e)
        else:
            error = "Vui lòng nhập đoạn mã!"

    return render_template('index.html', result=result, ciphertext=ciphertext, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)