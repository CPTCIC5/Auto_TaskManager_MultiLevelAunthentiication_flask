from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open("config.json","r") as c:
    params = json.load(c)["params"]

app=Flask(__name__)

app.config['SECRET_KEY'] = "secret_string"
app.config['SECRET_KEY'] = "secret_str"
app.config['SECRET_KEY'] = "secret_str"


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pass']
)
mail = Mail(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brain.db'
db=SQLAlchemy(app)

class Posts(db.Model):
    sno=db.Column(db.Integer,primary_key=True,nullable=True)
    title = db.Column(db.String(200), nullable=False)
    content= db.Column(db.String(5000), nullable=False)
    phone= db.Column(db.Integer,nullable=True)
    img_file = db.Column(db.String(80), nullable=True)
    time=db.Column(db.String(12), nullable=True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login",methods=["GET","POST"])
def login():
    if 'uname' in session and session['uname'] == params['admin-user1']:
        return redirect("/taskcreator")
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        session['uname']=username
        if username == params['admin-user1'] and password == params['admin-pass1']:
            return redirect("/taskcreator")
        else:
            return render_template('login.html',params=params)
    return render_template('login.html')
            


@app.route("/taskcreator",methods=["GET","POST"])
def taskcreator():
        if 'uname' in session and session['uname'] == params['admin-user1']:
            if (request.method=="POST"):
                title=request.form.get('title')
                content=request.form.get('content')
                phone=request.form.get('phone')
                img_file=request.form.get('img_file')
                entry=Posts(title=title,content=content,phone=phone,img_file=img_file,time=datetime.now())
                db.session.add(entry)
                db.session.commit()
                mail.send_message('NEW QUERY RAISED',
                sender=phone,
                recipients=[params['gmail-user']],
                body=title+ "\n" + content +"\n" +phone +"\n"
                )
        return render_template('taskcreator.html')


@app.route("/login1",methods=["GET","POST"])
def login1():
    if 'uname1' in session and session['uname1'] == params['admin-user2']:
        return redirect("/taskhandler")
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        session['uname1']=username
        if username == params['admin-user2'] and password == params['admin-pass2']:
            return redirect("/taskhandler")
        else:
            return render_template('login1.html',params=params)
    return render_template('login1.html')



@app.route("/taskhandler")
def taskhandler():
    report=Posts.query.all()
    return render_template('taskhandler.html',report=report)

@app.route("/logout")
def logout():
        if 'uname' in session and session['uname'] == params['admin-user1']:
            session.pop('uname')
            return redirect("/login")

@app.route("/logout1")
def logout1():
        if 'uname' in session and session['uname1'] == params['admin-user2']:
            session.pop('uname1')
            return redirect("/login1")
            
@app.route("/delete/<int:sno>")
def delete(sno):
    report2=Posts.query.filter_by(sno=sno).first()
    db.session.delete(report2)
    db.session.commit()
    return redirect("/taskhandler")

@app.route("/edit/<int:sno>")
def edit(sno):
    if request.method=="POST":
        title=request.form('title')
        content=request.form('content')
        phone=request.form('phone')
        report3=Posts.query.filter_by(sno=sno).first()
        report3.title=request.form.get('title')
        report3.content=request.form.get('content')
        report3.phone=request.form.get('phone')
        db.session.add(report3)
        db.session.commit()
    return redirect("/taskhandler")

@app.route("/login2",methods=["GET","POST"])
def login2():
    if 'uname2' in session and session['uname2'] == params['admin-user3']:
        return redirect("/taskexecutor")
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        session['uname2']=username
        if username == params['admin-user3'] and password == params['admin-pass3']:
            return redirect("/taskexecutor")
        else:
            return render_template('login2.html',params=params)
    return render_template('login2.html')


@app.route("/taskexecutor")
def taskexecutor():
    return render_template('taskexecutor.html')


@app.route("/logout2")
def logout2():
        if 'uname2' in session and session['uname2'] == params['admin-user3']:
            session.pop('uname2')
            return redirect("/taskexector")


if __name__=="__main__":
    app.run(debug=True)