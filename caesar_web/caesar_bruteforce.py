from flask import Flask, render_template, request
import string

app = Flask(__name__)

# hàm giải mã  với c là ky tự cần dịch, k là khoá dịch
def shift_char(c, k):
    if 'A' <= c <= 'Z':
        return chr((ord(c) - ord('A') - k) % 26 + ord('A'))
    elif 'a' <= c <= 'z':
        return chr((ord(c) - ord('a') - k) % 26 + ord('a'))
    else:
        return c

# dùng để thử tất cả các khoá dịch từ 0 đến 25 (26 chữ cái)
def caesar_bruteforce(ciphertext):
    if not ciphertext: return None, ""
    
    best_k = None
    best_plain = ""
    english_keywords = ["the", "and", "that", "is", "was", "for", "with", "this", "you", "have", "are"]
    max_score = -1

    for k in range(26):
        plaintext = "".join(shift_char(c, k) for c in ciphertext)
        # tính score
        score = sum(plaintext.lower().count(word) for word in english_keywords)

        if score > max_score:
            max_score = score
            best_k = k
            best_plain = plaintext

    return best_k, best_plain


@app.route('/', methods=['GET', 'POST'])
def index():
    k = None
    plaintext = ""
    input_cipher = ""

    if request.method == 'POST':
        input_cipher = request.form.get('ciphertext') # Lấy dữ liệu từ ô nhập liệu
        k, plaintext = caesar_bruteforce(input_cipher) # Gọi hàm logic của bạn để xử lý

    return render_template('index.html', k=k, plaintext=plaintext, input_cipher=input_cipher)

if __name__ == '__main__':
    app.run(debug=True)