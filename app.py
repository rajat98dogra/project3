import json

from flask import Flask, session, redirect, render_template, request, jsonify, flash
# from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from werkzeug.security import check_password_hash, generate_password_hash


import requests
app = Flask(__name__)
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='root',url='localhost',db='user')
app.config["SESSION_PERMANENT"] = False
app.config["S   ESSION_TYPE"] = "filesystem"
app.secret_key="00as"
# Session(app)

engine = create_engine(DB_URL)
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login' ,methods=["GET","POST"])
def login():
    session.clear()
    if request.method=="POST":
        username = request.form.get('name')
        password = request.form.get('password')
        # print(username,password)


        rows = db.execute("SELECT username,password FROM users WHERE username = :username",
                            {"username": username})
        row=rows.fetchone()
        # print(row,'#####################################')
        if row:
            if row[0]==username and row[1]==password:
                session['user'] = row[0]
                d = db.execute("SELECT * FROM books").fetchall()
                res = {"res":d,"username":username}
                return render_template('book.html', res=res)
        else:
            mes="INVALID DETAILS"
            return render_template('login.html',mes=mes)


    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/signin' ,methods=["GET","POST"])
def signin():
    if request.method=="POST":
        userCheck = db.execute("SELECT * FROM users WHERE username = :username",
                           {"username": request.form.get("name")}).fetchone()

        if userCheck :
            mes="USER ALready Exist"
            return render_template('signin.html', mes=mes)
        else:

            password=request.form.get("password")
            cpassword=request.form.get("confirmpassword")

            if password != cpassword:
                mes = "Password Not matched"
                return render_template('signin.html', mes=mes)
            username = request.form.get("name")
            email = request.form.get("email")
            db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
                       {"username": username,
                        "email": email,
                        "password": password,
                        })
            db.commit()

            return render_template('login.html')

    return render_template('signin.html')

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        value = request.form.get("search")
        option = request.form.get("option")
        print(value,option,"####################3")

        rows = db.execute("SELECT * FROM books WHERE {0} = '{1}'".format(option, value))
        return render_template('book.html', res={"res":rows})
    else:
        return redirect('/search')

@app.route('/book/review<string:isbn>/<string:title>')
def review(isbn,title):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "I3Ux7Tpx9uwPDdNuuZ3Q", "isbns": isbn})
    res=(res.json())
    res=res['books'][0]

    return render_template('review.html',res={"res":res,"title":title})

if __name__ == '__main__':
    app.run(debug=True)