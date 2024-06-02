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
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"
    
    posts = db.relationship('Post', backref='users')
    
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
    
    user = db.relationship('User')
    tags = db.relationship('Tag', secondary ='post_tags', backref ='posts_tags')

class Tag (db.Model):
    """Tag Table"""
    __tablename__ = 'tags'
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    name = db.Column(db.Text,
                     nullable = False,
                     unique = True)
    
    posts = db.relationship('Post', secondary='post_tags', backref='tags_posts')
    

class PostTag (db.Model):
    """Post Tag Table"""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True,
                        nullable = False)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True,
                       nullable = False)
    