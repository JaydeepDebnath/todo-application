from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    todos = db.relationship('Todo', backref='author', lazy=True)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.File(200))
    completed = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,)


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)

    