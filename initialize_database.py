from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import tempfile
import os

from app import app, db

load_dotenv()

def initialize_database(db_filename=os.getenv("SQLALCHEMY_DATABASE_FILENAME")):
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+db_filename
    # db.init(app)
    if(not os.path.isfile(db_filename)):
        with app.app_context():
            db.create_all()
            #db.session.commit()
            print("\narbron-reports-redux: File '{}' not found! Creating new database in '{}'.".format(db_filename, db_filename))
    else:
        print("\narbron-reports-redux: '{}' exists already! Terminating creation of database.".format(db_filename))

# Creates a temporary .db file, used for testing purposes
#def initialize_temp_database():
#    app = Flask(__name__)
#    temp_db = tempfile.NamedTemporaryFile(suffix=".db")
#    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+temp_db.name
#    db = SQLAlchemy(app)
#    from app import model
#    db.create_all()
#    db.session.commit()
#    return temp_db

if __name__ == "__main__":
    initialize_database()
