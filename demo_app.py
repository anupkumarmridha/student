from logging import exception
from plistlib import InvalidFileException
from flask import Flask, redirect, render_template, request
from datetime import datetime
from db import Database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db=Database()

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')

# admin module
@app.route("/add-admin", methods=['GET', 'POST'])
def addAdmin():
    if request.method=='POST':
        admin_id=request.form['admin_id']
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        admin_email=request.form['admin_email']
        admin_pass=request.form['admin_pass']
        phone=request.form['phone']
        db.insert_admin(admin_id, f_name, l_name, admin_email, admin_pass, phone)
    # print(allTodo)
    allStudent=db.fetch_all()
    return render_template('add_admin.html',allStudent=allStudent)

@app.route("/student-details/<int:stu_roll>", methods=['GET', 'POST'])
def studentDeatils(stu_roll):
    # print(allTodo)
    stuBio=db.fetch_one_student(stu_roll)
    return render_template('student_details.html',stuBio=stuBio)

@app.route("/all-student", methods=['GET', 'POST'])
def allStudentDeatils():
    # print(allTodo)
    allStudent=db.fetch_all_student()
    return render_template('all_student_details.html',allStudent=allStudent)