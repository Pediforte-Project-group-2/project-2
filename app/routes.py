from flask import render_template, request, flash,session, redirect, url_for
from app import app,db,models
from app.models import User
import hashlib
from app.my_func import check_login
import datetime
date= datetime.datetime.now()
day = date.strftime("%a")
day1 = date.strftime('%d')
year = date.year
month =  date.strftime("%b")
H = date.strftime('%H')
Min = date.strftime('%M')
Sec = date.strftime('%S')
Today= "{} {} {} {}, {}:{}:{}".format(day,month,day1,year,H,Min,Sec)


@app.route('/')
def index():
    return render_template('index.html',date= Today)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=="GET":
        return render_template('login.html') 
    else:
        name = request.form['name']
        password = request.form['password']
        if name=='' or password =='':
            flash("Fill in empty input fields")
            return render_template('login.html')
        else:
            password_h = hashlib.sha256(password.encode()).hexdigest()
            session['name']= name
            session['password']= password_h
            user = check_login()
            if user is None:
                flash('Invalid username or  password')
                return render_template('login.html')
            else:
                session['name']= user.name
                session['password']= user.password_hash
                resp = redirect(url_for('dashboard'))
                resp.set_cookie('name',user.name)
                resp.set_cookie('password',user.password_hash)
                return resp

            
          


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        matric = request.form['matric_num']
        gender = request.form['gender']
        role = request.form['role']
        password = request.form['password']
        c_password = request.form['c-password']
        # Verification
        if role == 'Admin':
           if name =='' or password =='' or c_password =='':
                flash("Fill in input fields !")
                return render_template('signup.html')
           if c_password != password:
                flash("passord does not match!")
                return render_template('signup.html')
        else:
            if name =='' or phone =='' or matric =='' or password =='' or c_password =='':
                flash("Fill in empty input fields!")
                return render_template('signup.html')
            if c-password != password:
                flash("password does not match!")
                return render_template('signup.html')
        # Signup success
        hashed = hashlib.sha256(password.encode()).hexdigest()
        user= User(name=name,email=email,password_hash=hashed,role=role,phone=phone,matric=matric,gender=gender)
        db.session.add(user)
        db.session.commit()
        flash('Registration sucessful')
        return render_template('student.html')


       
       


@app.route('/dashboard')
def dashboard():
    logged_in = True
    if 'name' in session:
       name = session['name']
       password = session['password']
    else:
        name = request.cookies.get('name')
        password = request.cookies.get('password')
        if name is None or email is None:
            logged_in = False
    #check if a student or Admin is logged in
    user = User.query.filter((User.name==name)&(User.password_hash == password)).first()
    return render_template('dashboard.html',name=user.name,role=user.role)

@app.route('/logout')
def logout():
    session.pop('name',None)
    session.pop('password',None)
    resp = redirect(url_for('index'))
    resp.set_cookie('name','')
    resp.set_cookie('password','',expires=0)
    return resp

@app.route('/admin/view-profiles')
def admin():
    return render_template("admin.html")
 
@app.route('/extra')
def extra():
    return render_template('extra.html')
