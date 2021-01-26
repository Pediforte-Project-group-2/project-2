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

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DOB = db.Column(db.String(20))
    nationality = db.Column(db.String(120))
    POB = db.Column(db.String(120))
    POO = db.Column(db.String(120))
    state = db.Column(db.String(120))
    M_S = db.Column(db.String(120))
    religion = db.Column(db.String(120))
    address = db.Column(db.String(200))
    kin = db.Column(db.String(120))
    kin_address = db.Column(db.String(200))
    previous_uni = db.Column(db.String(120))
    program = db.Column(db.String(120))
    mode = db.Column(db.String(120))
    qualification = db.Column(db.String(120))
    award = db.Column(db.String(120))
    study = db.Column(db.String(120))
    faculty = db.Column(db.String(120))
    department = db.Column(db.String(120))
    duration = db.Column(db.String(120))
    health = db.Column(db.String(120))
    kin_relationship = db.Column(db.String(120))
    kin_no = db.Column(db.String(120))
    user_id = db.Column(db.Integer,index=True,unique=True)



