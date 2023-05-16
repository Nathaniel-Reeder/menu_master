from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import db, connect_to_db
from werkzeug.security import check_password_hash

app = Flask(__name__)





if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)