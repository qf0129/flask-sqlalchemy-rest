from setuptools import setup 
import re

with open("flask_sqlalchemy_rest/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name = "Flask-SQLAlchemy-Rest",
    version = version,
    url = "https://github.com/qf0129/flask-sqlalchemy-rest",
    license='MIT',
    author='Qifei',
    author_email='qf0129@qq.com',
    description = "Easily generate rest api with Flask-SQLAlchemy",
    long_description = "Flask-SQLAlchemy-Rest is an extension for Flask that can easily generate rest api with Flask-SQLAlchemy.",
    packages = ['flask_sqlalchemy_rest'],
    include_package_data = True,
    platforms = "any",
    install_requires=["Flask-SQLAlchemy>=2.4.0"],
)
