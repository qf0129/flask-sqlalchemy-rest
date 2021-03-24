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
[GET]    http://127.0.0.1:5000/api/user
[POST]   http://127.0.0.1:5000/api/user
[GET]    http://127.0.0.1:5000/api/user/<id>
[PUT]    http://127.0.0.1:5000/api/user/<id>
[DELETE] http://127.0.0.1:5000/api/user/<id>
``` 
And you can add params in GET url:

```
[GET] http://127.0.0.1:5000/api/user?_page=1&_page_size=10&_sort=id&_desc=1&email:eq=xxx&username:contains=xxx 
```
`_page` page index, default 1   
`_page_size` number of pages, default 10   
`_sort` column name to sort  
`_desc` if `_desc=1`, will sort the data in descending order   
`_serach` query columns with `search_columns` option      
`email:eq` filter email with operator [`eq`](#Operator)    
`username:contains` filter username with operator [`contains`](#Operator)   


# Documentation 

### Operator
`eq` equal  
`ne` not equal  
`gt` greter than  
`ge` greter equal  
`lt` less than  
`le` less equal  
`in` in a list, like `http://127.0.0.1:5000/api/user?name:in=Name1,Name2,Name3 `  
`notin` not in a list  
`contains` contains some strings  

### Class `Rest`
&nbsp;&nbsp;```def __init__(app=None, db=None, url_prefix='/api', auth_decorator=None, max_page_size=100)```    
&nbsp;&nbsp;&nbsp;&nbsp;**app:** Flask application instance  
&nbsp;&nbsp;&nbsp;&nbsp;**db:**  Flask-SQLAlchemy instance   
&nbsp;&nbsp;&nbsp;&nbsp;**url_prefix:** Base url path for apis   
&nbsp;&nbsp;&nbsp;&nbsp;**auth_decorator:** Decorator function for authentication
&nbsp;&nbsp;&nbsp;&nbsp;**max_page_size:** max page size in GET api

&nbsp;&nbsp;```def add_model(model, url_name=None, methods=['GET', 'POST', 'PUT', 'DELETE'], ignore_columns=[], json_columns=[], search_columns=[])```   
&nbsp;&nbsp;&nbsp;&nbsp;**model:** `SQLAlchemy.Model` object  
&nbsp;&nbsp;&nbsp;&nbsp;**url_name:** Will be displayed in url    
&nbsp;&nbsp;&nbsp;&nbsp;**methods:** Allowed HTTP methods. Only `GET,POST,PUT,DELETE` are allowed    
&nbsp;&nbsp;&nbsp;&nbsp;**ignore_columns:** Ignored columns in `GET` api     
&nbsp;&nbsp;&nbsp;&nbsp;**json_columns:** Columns to be parsed into JSON format   
&nbsp;&nbsp;&nbsp;&nbsp;**search_columns:** Columns can query with `_serach` param in `GET` api    

