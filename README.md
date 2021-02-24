Flask-SQLAlchemy-Rest
================

Flask-SQLAlchemy-Rest is an extension for Flask that can easily generate rest api with Flask-SQLAlchemy.

## Installing
```
$ pip install flask_sqlalchemy_rest
```

## Example
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

With the above application you can visit the following APIs:
```
[GET]    http://127.0.0.1:5000/api/user
[POST]   http://127.0.0.1:5000/api/user
[GET]    http://127.0.0.1:5000/api/user/<id>
[PUT]    http://127.0.0.1:5000/api/user/<id>
[DELETE] http://127.0.0.1:5000/api/user/<id>
```

## Documentation 

```
class Rest(object):
    def __init__(self, app=None, db=None, url_prefix='/api', auth_decorator=None):
        ...
    def init_app(self, app, db=None, url_prefix=None, auth_decorator=None)
        ...
    def add_model(self, model, url_name=None, methods=['GET', 'POST', 'PUT', 'DELETE'], ignore_columns=[]):
        ...
```
