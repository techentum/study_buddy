from . import app
from .models import *

@app.route('/')
def home():
    return 'hello world'