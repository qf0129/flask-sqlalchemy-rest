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
    username = db.Column(db.String)
    email = db.Column(db.String)

with app.app_context():
    db.create_all()

rest.add_model(User)
```

With the above application you can visit the following APIs:
```
[GET]    http://127.0.0.1:5000/api/user  # ?page=1&page_size=10&email=xxx&username=xxx&contain_keys=email,username
[POST]   http://127.0.0.1:5000/api/user
[GET]    http://127.0.0.1:5000/api/user/<id>
[PUT]    http://127.0.0.1:5000/api/user/<id>
[DELETE] http://127.0.0.1:5000/api/user/<id>
```

## Documentation 


Class `Rest()`  
&nbsp;&nbsp;def `__init__`(app=None, db=None, url_prefix='/api', auth_decorator=None)    
&nbsp;&nbsp;def `init_app`(app, db=None, url_prefix=None, auth_decorator=None)   
&nbsp;&nbsp;&nbsp;&nbsp;**app:** Flask application instance  
&nbsp;&nbsp;&nbsp;&nbsp;**db:**  Flask-SQLAlchemy instance   
&nbsp;&nbsp;&nbsp;&nbsp;**url_prefix:** Base url path for apis   
&nbsp;&nbsp;&nbsp;&nbsp;**auth_decorator:** Decorator function for authentication

&nbsp;&nbsp;def `add_model`(model, url_name=None, methods=['GET', 'POST', 'PUT', 'DELETE'], ignore_columns=[])   
&nbsp;&nbsp;&nbsp;&nbsp;**model:** `SQLAlchemy.Model` object  
&nbsp;&nbsp;&nbsp;&nbsp;**url_name:** Will be displayed in url    
&nbsp;&nbsp;&nbsp;&nbsp;**methods:** Allowed HTTP methods. Only `GET,POST,PUT,DELETE` are allowed    
&nbsp;&nbsp;&nbsp;&nbsp;**ignore_columns:** Ignored columns in api with `GET` method    

