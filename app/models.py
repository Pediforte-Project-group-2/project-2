from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),index=True,unique=True)
    email = db.Column(db.String(120),unique=True)
    phone = db.Column(db.String(50))
    matric = db.Column(db.String(20),unique=True)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(10))
    password_hash = db.Column(db.String(200),index=True,unique=True)
    reqistered = db.Column(db.DateTime(), default= datetime.utcnow())
    
    def __repr__(self):
        return '<User {}>'.format(self.name)

