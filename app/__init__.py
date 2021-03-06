from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initial imports and checks
load_dotenv()
db_file = os.getenv("SQLALCHEMY_DATABASE_FILENAME")

# Initializing global objects
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_file
db = SQLAlchemy(app)
cors = CORS(app)

from app import models
from app.api_router import api_blueprint
from app.frontend_router import frontend_blueprint

# Registration of blueprints which stores routes from the other files
app.register_blueprint(api_blueprint)
app.register_blueprint(frontend_blueprint)

#if not os.path.isfile(db_file):
    #print("\nDatabase file {} not found! Terminating program.\n".format(db_file))
    #exit()
