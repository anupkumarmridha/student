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

@app.route("/update-admin", methods=['GET', 'POST'])
def updateAdmin(admin_id):
    if request.method=='POST':
        admin_id=request.form['admin_id']
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        admin_email=request.form['admin_email']
        admin_pass=request.form['admin_pass']
        phone=request.form['phone']
        db.update_admin(admin_id, f_name, l_name, admin_email, admin_pass, phone)
        return redirect('/')
    return render_template('update_admin.html')

# Faculty Module
@app.route("/add-faculty", methods=['GET', 'POST'])
def addFaculty():
    if request.method=='POST':
        faculty_id=request.form['faculty_id']
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        gender=request.form.get('gender')
        dob=request.form['dob']
        faculty_adrs=request.form['faculty_adrs']
        faculty_email=request.form['faculty_email']
        faculty_pass=request.form['faculty_pass']
        faculty_pass2=request.form['faculty_pass2']
        phone=request.form['phone']
        if(faculty_pass==faculty_pass2):
            db.insert_faculty(faculty_id, f_name, l_name, gender, dob, faculty_adrs, faculty_email, faculty_pass, phone)
            return redirect('/all-faculty')
        else:
            return "Invalid Password"
    # print(allTodo)
    allFaculty=db.fetch_all_faculty()
    return render_template('add_faculty.html',allFaculty=allFaculty)

# update faculty
@app.route("/update-faculty/<int:faculty_id>", methods=['GET', 'POST'])
def updateFaculty(faculty_id):
    if request.method=='POST':
        print("hi")
        # faculty_id=request.form['faculty_id']
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        gender=request.form.get('gender')
        dob=request.form['dob']
        faculty_adrs=request.form['faculty_adrs']
        faculty_email=request.form['faculty_email']
        faculty_pass=request.form['faculty_pass']
        phone=request.form['phone']
        db.update_faculty(faculty_id, f_name, l_name, gender, dob, faculty_adrs, faculty_email, faculty_pass, phone)
        return redirect('/all-faculty')
    faculty_details=db.fetch_one_faculty(faculty_id)
    return render_template('update_faculty.html',faculty_details=faculty_details)

@app.route("/delete-faculty/<int:faculty_id>", methods=['GET', 'POST'])
def deleteFaculty(faculty_id):
    # print(allTodo)
    db.delete_faculty(faculty_id)
    return redirect('/all-faculty')

@app.route("/all-faculty", methods=['GET', 'POST'])
def allFacultyDeatils():
    # print(allTodo)
    allFaculty=db.fetch_all_faculty()
    return render_template('all_faculty_details.html',allFaculty=allFaculty)



@app.route("/faculty-details/<int:faculty_id>", methods=['GET', 'POST'])
def facultyDeatils(faculty_id):
    # print(allTodo)
    facultyBio=db.fetch_one_faculty(faculty_id)
    return render_template('faculty_details.html',facultyBio=facultyBio)

#student module 
@app.route("/add-student", methods=['GET', 'POST'])
def addStudent():
    if request.method=='POST':
        stu_roll=request.form['stu_roll']
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        gender=request.form.get('gender')
        dob=request.form['dob']
        stu_adrs=request.form['stu_adrs']
        stu_email=request.form['stu_email']
        stu_pass=request.form['stu_pass']
        stu_pass2=request.form['stu_pass2']
        phone=request.form['phone']
        if stu_pass==stu_pass2:
            db.insert_student(stu_roll, f_name, l_name, gender, dob, stu_adrs, stu_email, stu_pass, phone)
            return redirect('/all-student')
        else:
            return "invalid password"
            
    # print(allTodo)
    allStudent=db.fetch_all_student()
    return render_template('add_student.html',allStudent=allStudent)


@app.route("/update-student/<int:stu_roll>", methods=['GET', 'POST'])
def updateStudent(stu_roll):
    if request.method=='POST':
        stu_roll=request.form['stu_roll']
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        gender=request.form.get('gender')
        dob=request.form['dob']
        stu_adrs=request.form['stu_adrs']
        stu_email=request.form['stu_email']
        stu_pass=request.form['stu_pass']
        phone=request.form['phone']
        db.update_student(stu_roll, f_name, l_name, gender, dob, stu_adrs, stu_email, stu_pass, phone)
        return redirect('/all-student')
    return render_template('update_student.html')

@app.route("/delete-student/<int:stu_roll>", methods=['GET', 'POST'])
def deleteStudent(stu_roll):
    # print(allTodo)
    db.delete_student(stu_roll)
    return redirect('/all-student')

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


#course module 
@app.route("/add-course", methods=['GET', 'POST'])
def addCourse():
    if request.method=='POST':
        course_id=request.form['course_id']
        course_name=request.form['course_name']
        course_desc=request.form['course_desc']
        db.insert_course(course_id, course_name, course_desc)
        return redirect('/add-course')
    # print(allTodo)
    allCourse=db.fetch_all_course()
    return render_template('add_course.html',allCourse=allCourse)


@app.route("/update-course/<int:course_id>", methods=['GET', 'POST'])
def updateCourse(course_id):
    if request.method=='POST':
        course_id=request.form['course_id']
        course_name=request.form['course_name']
        db.update_course(course_id, course_name)
        return redirect('/add-course')

    return render_template('update_course.html')

@app.route("/delete-course/<int:course_id>", methods=['GET', 'POST'])
def deleteCourse(course_id):
    # print(allTodo)
    db.delete_course(course_id)
    return redirect('/add-course')

@app.route("/course-details/<int:course_id>", methods=['GET', 'POST'])
def courseDeatils(course_id):
    # print(allTodo)
    courseBio=db.fetch_one_course(course_id)
    return render_template('course_details.html',courseBio=courseBio)

@app.route("/all-course", methods=['GET', 'POST'])
def allCourseDeatils():
    # print(allTodo)
    allCourse=db.fetch_all_course()
    return render_template('all_course_details.html',allCourse=allCourse)



#course module 
@app.route("/add-subject", methods=['GET', 'POST'])
def addSubject():
    if request.method=='POST':
        sub_id=request.form['sub_id']
        sub_name=request.form['sub_name']
        course_id=request.form.get('course_id')
        faculty_id=request.form.get('faculty_id')
        db.insert_subject(sub_id, sub_name,course_id,faculty_id)
        return redirect('/add-subject')
    # print(allTodo)
    allSubject=db.fetch_all_subject()
    allCourse=db.fetch_all_course()
    allFaculty=db.fetch_all_faculty()
    
    return render_template('add_subject.html',allSubject=allSubject, allCourse=allCourse, allFaculty=allFaculty)


@app.route("/update-subject/<int:sub_id>", methods=['GET', 'POST'])
def updateSubject(sub_id):
    if request.method=='POST':
        sub_id=request.form['subject_id']
        sub_name=request.form['subject_name']
        course_id=request.form['course_id']
        stu_roll=request.form['stu_roll']
        faculty_id=request.form['faculty_id']
        db.update_subject(sub_id, sub_name,course_id, stu_roll, faculty_id)
        return redirect('/all-subject')
    return render_template('update_subject.html')

@app.route("/delete-subject/<int:sub_id>", methods=['GET', 'POST'])
def deleteSubject(sub_id):
    # print(allTodo)
    db.delete_subject(sub_id)
    return redirect('/all-subject')

@app.route("/subject-details/<int:sub_id>", methods=['GET', 'POST'])
def subjectDeatils(sub_id):
    # print(allTodo)
    subBio=db.fetch_one_subject(sub_id)
    return render_template('subject_details.html',subBio=subBio)


@app.route("/all-subject", methods=['GET', 'POST'])
def allSubjectDeatils():
    # print(allTodo)
    allSub=db.fetch_all_subject()
    return render_template('all_subject_details.html', allSub=allSub)









if __name__=='__main__':
    app.run(debug=True, port=8000)
    