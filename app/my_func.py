from flask import session, request
from app.models import User

def check_login():
    name = None
    password = None
    if 'name' in session:
        name = session['name']
        password = session['password']
    elif request.cookies.get('name') and request.cookies.get('password'):
        name = request.cookies.get('name')
        password = request.cookies.get('password')
    if name is None or password is None:
        return False

    # verify User
    user = User.query.filter((User.name==name)&(User.password_hash == password)).first()
    if user is None:
        session.pop('name',None)
        session.pop('password',None)
        return None
    else:
        return user
    