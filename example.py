from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_rest import Rest
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
rest = Rest(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    key_float = db.Column(db.Float)
    enabled = db.Column(db.Boolean)
    ctime1 = db.Column(db.DateTime, default=datetime.datetime.now)
    ctime2 = db.Column(db.Date, default=datetime.datetime.now().date)
    ctime3 = db.Column(db.Time, default=datetime.datetime.now().time)

with app.app_context():
    db.create_all()

rest.add_model(User)