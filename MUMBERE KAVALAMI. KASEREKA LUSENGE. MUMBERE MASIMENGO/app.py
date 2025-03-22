from flask import Flask, render_template, request

import numpy as np

app = Flask(__name__)

def cesar_cipher(text, key, action):
    shift = int(key) % 26
    if action == "decrypt":
        shift = -shift
    result = "".join(
        chr((ord(c) - 65 + shift) % 26 + 65) if c.isalpha() else c
        for c in text.upper()
    )
    return result

def affine_cipher(text, key, action):
    a, b = map(int, key.split(","))
    
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None
    
    if action == "decrypt":
        a_inv = mod_inverse(a, 26)
        if a_inv is None:
            return "Erreur : a n'a pas d'inverse modulaire."
    
    result = ""
    for c in text.upper():
        if c.isalpha():
            x = ord(c) - 65
            if action == "encrypt":
                result += chr((a * x + b) % 26 + 65)
            else:
                result += chr((a_inv * (x - b)) % 26 + 65)
        else:
            result += c
    return result

def vigenere_cipher(text, key, action):
    key = key.upper()
    key_indices = [ord(k) - 65 for k in key]
    text = text.upper()
    
    result = []
    key_index = 0

    for c in text:
        if c.isalpha():
            shift = key_indices[key_index % len(key)]
            shift = shift if action == "encrypt" else -shift
            new_char = chr((ord(c) - 65 + shift) % 26 + 65)
            result.append(new_char)
            key_index += 1
        else:
            result.append(c)

    return "".join(result)

def hill_cipher(text, key, action):
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    text = text.replace(" ", "").upper()
    n = int(len(key) ** 0.5)

    if len(text) % n != 0:
        text += 'X' * (n - len(text) % n)

    key_matrix = np.array(key).reshape((n, n))

    result = ""

    for i in range(0, len(text), n):
        block = [ord(c) - 65 for c in text[i:i + n]]
        block_matrix = np.array(block).reshape((n, 1))

        if action == 'encrypt':
            result_block = np.dot(key_matrix, block_matrix) % 26
        elif action == 'decrypt':
            det = int(round(np.linalg.det(key_matrix))) % 26
            det_inv = mod_inverse(det, 26)

            if det_inv is None:
                return "Erreur : La matrice de chiffrement n'est pas inversible modulo 26."

            adjugate = np.round(np.linalg.inv(key_matrix) * det).astype(int) % 26
            inv_key_matrix = (det_inv * adjugate) % 26
            result_block = np.dot(inv_key_matrix, block_matrix) % 26

        result += ''.join(chr(int(x) + 65) for x in result_block.flatten())

    return result

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        algorithm = request.form["algorithm"]
        action = request.form["action"]
        text = request.form["text"]
        key = request.form["key"]

        try:
            if algorithm == "cesar":
                result = cesar_cipher(text, key, action)
            elif algorithm == "affine":
                result = affine_cipher(text, key, action)
            elif algorithm == "vigenere":
                result = vigenere_cipher(text, key, action)
            elif algorithm == "hill":
                key_list = list(map(int, key.split(",")))
                result = hill_cipher(text, key_list, action)
            else:
                error = "Algorithme non reconnu."
        except Exception as e:
            error = f"Erreur : {str(e)}"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
