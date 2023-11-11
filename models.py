import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False)
    
    last_name = db.Column(db.String(50),
                           nullable=False)
    
    image_url = db.Column(db.String(500),
                           nullable=True)
    
    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    __tablename__ = "posts";

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(200),
                      nullable=False)
    
    content = db.Column(db.String(1000),
                        nullable=False)
    
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    user = db.relationship('User', backref="posts")