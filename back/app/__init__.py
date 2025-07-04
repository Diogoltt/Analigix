from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['DATABASE_PATH'] = os.path.join(basedir, 'database', 'despesas_brasil.db')
app.config['TABLE_NAME'] = 'despesas' 

from app import routes

# Configurar Swagger
try:
    from app.swagger_config import init_swagger
    api = init_swagger(app)
    print("📚 Swagger configurado com sucesso! Acesse: http://localhost:5000/docs/")
except ImportError as e:
    print(f"⚠️ Swagger não configurado: {e}")
except Exception as e:
    print(f"❌ Erro ao configurar Swagger: {e}")