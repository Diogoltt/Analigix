from app import app 

if __name__ == '__main__':
    print("Servidor da API iniciado em http://127.0.0.1:5000")
    app.run(debug=True, port=5000)