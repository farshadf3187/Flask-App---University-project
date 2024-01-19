from flask_sqlalchemy import SQLAlchemy
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    lastEditDate = db.Column(db.String(255))
    lastEditTime = db.Column(db.String(255))
