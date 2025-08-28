import os
import sqlite3
from flask import Flask
from dotenv import load_dotenv
from staffing.routes import pages


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLITE3_DB"] = os.environ.get("SQLITE3_DB")
    app.db = sqlite3.connect(app.config["SQLITE3_DB"], check_same_thread=False)

    app.register_blueprint(pages)
    return app