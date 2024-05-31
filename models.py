from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User (db.Model):
    """User Table"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement= True)
    first_name = db.Column(db.String(50),
                           nullable = False)
    last_name = db.Column(db.String(50),
                          nullable =False)
    image_URL = db.Column(db.Text,
                          nullable = False,
                          default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    
class Post (db.Model):
    """Post Table"""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    title = db.Column(db.Text,
                      nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)
    
    created_at = db.Column(db.DateTime, 
                           default=datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='posts')

    