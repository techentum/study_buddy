from dotenv import load_dotenv
import os
load_dotenv()

from flask import Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.environ.get('FLASK_SECRET')

from .models import db
with app.app_context():
    db.create_all()
    
from .routes import *