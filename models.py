
from flask_sqlalchemy import SQLAlchemy

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