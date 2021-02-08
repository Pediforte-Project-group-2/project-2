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
    logged_in = True
    if 'name' in session:
        name = session['name']
        password = session['password']
        return redirect(url_for('dashboard'))
    else:
        name = request.cookies.get('name')
        password = request.cookies.get('password')
        if name is None or password is None:
            logged_in = False
            return render_template('index.html',date= Today)
        return redirect(url_for('dashboard'))


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=="GET":
       return render_template('login.html') 
    else:
        name = request.form['name']
        password = request.form['password']
        if name=='' or password =='':
            flash("Please enter your username and password!")
            return render_template('login.html')
        else:
            password_h = hashlib.sha256(password.encode()).hexdigest()
            session['name']= name
            session['password']= password_h
            session['logged_in']= True
            user = check_login()
            if user is None:
                flash('Invalid username or  password')
                return render_template('login.html')
            else:
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
    length= len(students)
    user = User.query.filter((User.name==name)&(User.password_hash == password)).first()
    info= Info.query.filter(Info.user_id==user.id).first()
    return render_template('dashboard.html',user=user,students=students,info=info,len=length)


@app.route('/logout')
def logout():
    session.pop('name',None)
    session.pop('password',None)
    session.pop('logged_in',None)
    resp = redirect(url_for('index'))
    resp.set_cookie('name','')
    resp.set_cookie('password','',expires=0)
    return resp

   
 
@app.route('/extra')
def extra():
    return render_template('extra.html')




@app.route('/student/register/<id>' ,methods=['POST','GET'])
def student(id):
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
    user = User.query.filter(User.id==id).first()
    info = Info.query.filter(Info.user_id==id).first()
    if info is None:
        info="nil"
    if  request.method=='GET':
        if user is not None:
            return render_template('student.html',user=user,info=info)
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
        if info =="nil":
            info = Info(user_id=info_1,DOB=info_2,nationality=info_3,POB=info_4,POO=info_5,state=info_6,M_S=info_7,religion=info_8,address=info_9,kin=info_10,kin_address=info_11,previous_uni=info_13,program=info_14,mode=info_15,qualification=info_16,award=info_17,study=info_18,faculty=info_19,department=info_20,duration=info_21,health=info_22,kin_relationship=info_23,kin_no=info_12)
            db.session.add(info)
        else:
             info.DOB=info_2
             info.nationality=info_3
             info.POB=info_4
             info.POO=info_5
             info.state=info_6
             info.M_S=info_7
             info.religion=info_8
             info.address=info_9
             info.kin=info_10
             info.kin_address=info_11
             info.previous_uni=info_13
             info.program=info_14
             info.mode=info_15
             info.qualification=info_16
             info.award=info_17
             info.study=info_18
             info.faculty=info_19
             info.department=info_20
             info.duration=info_21
             info.health=info_22
             info.kin_relationship=info_23
             info.kin_no=info_12
        db.session.commit()
        flash("Biodata updated Successful")
        return redirect(url_for('dashboard'))


@app.route('/student-profile/delete/<id>')
def delete(id):
    logged_in = True
    if 'name' in session:
        name = session['name']
        password = session['password']
        if name!= 'Admin':
            return redirect(url_for('logout'))
    else:
        name = request.cookies.get('name')
        password = request.cookies.get('password')
        if name is None or password is None:
            logged_in = False
            return redirect(url_for('login'))
        elif name!= 'Admin':
            return redirect(url_for('logout'))
    user = User.query.filter(User.id==id).first()
    info = Info.query.filter(Info.user_id==id).first()
    if user is not None:
        db.session.delete(user)
        if info is not None:
            db.session.delete(info)
        db.session.commit()
        flash('{}\'s account was deleted'.format(user.name))
        return redirect(url_for('dashboard'))
    else:
        flash("Account not Found!!")
        return redirect(url_for('dashboard'))



@app.route('/admin/view/<id>')
def view(id):
    logged_in = True
    if 'name' in session:
        name = session['name']
        password = session['password']
        if name!= 'Admin':
            return redirect(url_for('logout'))
    else:
        name = request.cookies.get('name')
        password = request.cookies.get('password')
        if name is None or password is None:
            logged_in = False
            return redirect(url_for('login'))
        elif name!= 'Admin':
            return redirect(url_for('logout'))
    user = User.query.filter(User.id==id).first()
    info = Info.query.filter(Info.user_id==id).first()
    if user is not None and info is not None:
        return render_template('admin.html',user=user,info=info)
    else:
        flash("Student not found!!")
        return redirect(url_for('dashboard'))

@app.route('/student-profile/edit/<id>',methods=['GET','POST'])
def edit(id):
    logged_in = True
    if 'name' in session:
        name = session['name']
        password = session['password']
        if name!= 'Admin':
            return redirect(url_for('logout'))
    else:
        name = request.cookies.get('name')
        password = request.cookies.get('password')
        if name is None or password is None:
            logged_in = False
            return redirect(url_for('login'))
        elif name!= 'Admin':
            return redirect(url_for('logout'))
    user = User.query.filter(User.id==id).first()
    if request.method=='GET' and  user is not None:
        return render_template('edit.html', user=user)
    elif  request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        matric = request.form['matric_num']
        gender = request.form['gender']
        user.name=name
        user.email=email
        user.phone=phone
        user.matric=matric
        user.gender=gender
        db.session.commit()
        flash("{}'s profile was updated sucessful".format(user.name))
        return redirect(url_for('dashboard'))
    else:
        flash("Account not Found!!")
        return redirect(url_for('dashboard'))

@app.route('/admission')
def admission():
    return render_template('admission.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
    


