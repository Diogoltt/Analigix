# backend/app.py
from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = r'C:\Users\feliperibeiro\Documents\Analigix\Analigix\back\csvs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    estado = request.form.get('estado')
    ano = request.form.get('ano')
    arquivo = request.files.get('file')

    if not estado or not ano:
        return 'Estado e ano são obrigatórios.', 400

    if not arquivo:
        return 'Nenhum arquivo enviado.', 400

    caminho_arquivo = os.path.join(UPLOAD_FOLDER, f"{estado}_{ano}_{arquivo.filename}")
    arquivo.save(caminho_arquivo)

    return 'Arquivo recebido com sucesso!', 200

if __name__ == '__main__':
    app.run(debug=True)
