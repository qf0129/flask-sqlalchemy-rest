Flask-SQLAlchemy-Rest
================

Flask-SQLAlchemy-Rest is an extension for Flask that can easily generate rest api with Flask-SQLAlchemy.

#### Installing
`pip install Flask-SQLAlchemy-Rest`

#### Example
-------
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_rest import Rest

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
rest = Rest(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

with app.app_context():
    db.create_all()

rest.add_model(User)
```
