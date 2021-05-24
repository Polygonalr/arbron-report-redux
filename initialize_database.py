from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import tempfile
import os

def initialize_database(db_filename=os.getenv("SQLALCHEMY_DATABASE_FILENAME")):
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+db_filename
    db = SQLAlchemy(app)
    if(not os.path.isfile(db_filename)):
        db.create_all()
        print("\narbron-reports-redux: File '{}' not found! Creating new database in '{}'.".format(db_filename, db_filename))
    else:
        print("\narbron-reports-redux: '{}' exists already! Terminating creation of database.".format(db_filename))

# Creates a temporary .db file, used for testing purposes
def initialize_temp_database():
    load_dotenv()
    app = Flask(__name__)
    temp_db = tempfile.NamedTemporaryFile(suffix=".db")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+temp_db.name
    db = SQLAlchemy(app)
    db.create_all()
    return temp_db

if __name__ == "__main__":
    initialize_database()