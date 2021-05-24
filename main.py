from flask import Flask
from api_router import api_blueprint
from models import db
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.getenv("SQLALCHEMY_DATABASE_FILENAME")
db.init_app(app)
app.register_blueprint(api_blueprint)
