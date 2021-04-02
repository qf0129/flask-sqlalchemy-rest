from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_rest import Rest
import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
rest = Rest(app, db, max_page_size=300)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    key1 = db.Column(db.Float)
    key2 = db.Column(db.Boolean, default=False)
    key3 = db.Column(db.Text)
    ctime1 = db.Column(db.DateTime, default=datetime.datetime.now)
    ctime2 = db.Column(db.Date, default=datetime.datetime.now().date)
    ctime3 = db.Column(db.Time, default=datetime.datetime.now().time)


class UserAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    address = db.Column(db.Text)


with app.app_context():
    db.create_all()

user_join_models = {
    'user_address': {
        'model': UserAddress,
        'column_a': User.id,
        'column_b': UserAddress.user_id,
        'inner_join': False,
    }
}

rest.add_model(User, ignore_columns=['key1'], json_columns=['key3'], search_columns=['name', 'key3'], join_models=user_join_models)
rest.add_model(UserAddress)
