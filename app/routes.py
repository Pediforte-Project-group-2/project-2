from flask import render_template, request, flash,session, redirect, url_for
from app import app,db,models
from app.models import User,Info
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
            if c_password != password:
                flash("password does not match!")
                return render_template('signup.html')
        # Signup success
        hashed = hashlib.sha256(password.encode()).hexdigest()
        user= User(name=name,email=email,password_hash=hashed,role=role,phone=phone,matric=matric,gender=gender)
        db.session.add(user)
        db.session.commit()
        flash('Registration sucessful')
        return redirect(url_for('login'))


       
       


@app.route('/dashboard')
def dashboard():
    #check if a student or Admin is logged in
    logged_in = True
    if 'name' in session:
        name = session['name']
        password = session['password']
    else:
        name = request.cookies.get('name')
        password = request.cookies.get('password')
        if name is None or password is None:
            logged_in = False
            return redirect(url_for('login'))
    # Admin template
    student_obj= User.query.filter(User.role =="Student").all()
    students=[]
    for item in student_obj:
        item_dict = {
        'name': item.name,
        'matric':item.matric,
        'gender':item.gender,
        'registered': item.reqistered,
        'id':item.id
        }
        students.append(item_dict)
    #Student template
    user = User.query.filter((User.name==name)&(User.password_hash == password)).first()
    info= Info.query.filter(Info.user_id==user.id).first()
    return render_template('dashboard.html',user=user,students=students,info=info)


@app.route('/logout')
def logout():
    session.pop('name',None)
    session.pop('password',None)
    resp = redirect(url_for('index'))
    resp.set_cookie('name','')
    resp.set_cookie('password','',expires=0)
    return resp

   
 
@app.route('/extra')
def extra():
    return render_template('extra.html')




@app.route('/student/register/<id>' ,methods=['POST','GET'])
def student(id):
    user = User.query.filter(User.id==id).first()
    if  request.method=='GET':
        if user is not None:
            return render_template('student.html',user=user)
    else:
        user = User.query.filter(User.id==id).first()
        info_1 = user.id
        info_2 = request.form['dob']
        info_3 = request.form['nation']
        info_4 = request.form['place']
        info_5 = request.form['origin']
        info_6= request.form['state']
        info_7 = request.form['status']
        info_8 = request.form['religion']
        info_9 = request.form['address']
        info_10 = request.form['kin']
        info_11 = request.form['kin address']
        info_12 = request.form['kin no']
        info_13 = request.form['ex uni']
        info_14 = request.form['program']
        info_15 = request.form['mode']
        info_16 = request.form['qualification']
        info_17 = request.form['award']
        info_18 = request.form['study']
        info_19 = request.form['faculty']
        info_20 = request.form['department']
        info_21 = request.form['duration']
        info_22 = request.form['health']
        info_23 = request.form['kin relationship']
        info = Info(user_id=info_1,DOB=info_2,nationality=info_3,POB=info_4,POO=info_5,state=info_6,M_S=info_7,religion=info_8,address=info_9,kin=info_10,kin_address=info_11,previous_uni=info_13,program=info_14,mode=info_15,qualification=info_16,award=info_17,study=info_18,faculty=info_19,department=info_20,duration=info_21,health=info_22,kin_relationship=info_23,kin_no=info_12)
        db.session.add(info)
        db.session.commit()
        flash("Update Successful")
        return redirect(url_for('dashboard'))


@app.route('/student-profile/delete/<id>')
def delete(id):
    user = User.query.filter(User.id==id).first()
    info = User.query.filter(info.user_id==id).first()
    if user is not None:
        db.session.delete(user)
        db.session.delete(info)
        db.session.commit()
        flash('{}\'s account was deleted'.format(user.name))
        return redirect(url_for('dashboard'))
