from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['DATABASE_PATH'] = os.path.join(basedir, 'database', 'despesas_brasil.db')
app.config['TABLE_NAME'] = 'despesas' 

from app import routes