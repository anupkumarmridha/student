from asyncio import exceptions
import mysql.connector as connector
import json
from flask import Flask, redirect
class Database:
    #Creating constractor
    def __init__(self):
        self.cnx=connector.connect(host='localhost',
                port='3306',
                user='root',
                password='root',
                database='student_attendance')
        self.cnx.autocommit=True
        self.cur=self.cnx.cursor(dictionary=True)
        
        # admin table
        def create_admin():
                admin_table="""create table if not exists admin(
                    admin_id int not NULL primary key, 
                    f_name varchar(255) not NULL,
                    l_name varchar(255) not NULL,
                    admin_email varchar(255) not NULL,
                    admin_pass varchar(255) not NULL,
                    phone varchar(12));
                    """
                self.cur.execute(admin_table)
        
        # Student table
        def create_student():
                student_table="""create table if not exists student(
                    stu_roll int not NULL primary key, 
                    f_name varchar(255) not NULL,
                    l_name varchar(255) not NULL,
                    gender enum('M','F'),
                    dob Date,
                    stu_adrs varchar(500),
                    stu_email varchar(255) not NULL,
                    stu_pass varchar(255) not NULL,
                    phone varchar(12),
                    created_at datetime default now(),
                    updated_at datetime default now()
                    );
                    """
                self.cur.execute(student_table)
        
        # faculty table
        def create_faculty():
            faculty_table="""create table if not exists faculty(
                    faculty_id int not NULL primary key, 
                    f_name varchar(255) not NULL,
                    l_name varchar(255) not NULL,
                    gender enum('M','F'),
                    dob Date,
                    faculty_adrs varchar(500),
                    faculty_email varchar(255) not NULL,
                    faculty_pass varchar(255) not NULL,
                    phone varchar(12),
                    created_at datetime default now(),
                    updated_at datetime default now()
                    );
                    """
            self.cur.execute(faculty_table)
        
        # subject table
        def create_course():
            course_table="""create table if not exists course(
                    course_id int not NULL primary key, 
                    course_name varchar(255) not NULL,
                    course_desc varchar(555),
                    created_at datetime default now(),
                    updated_at datetime default now()
                    );
                    """
            self.cur.execute(course_table) 

        # subject table
        def create_subject():
            subject_table="""create table if not exists subject(
                    sub_id int not NULL primary key, 
                    sub_name varchar(255) not NULL,
                    course_id int not NULL,
                    faculty_id int not NULL,
                    created_at datetime default now(),
                    updated_at datetime default now(),
                    foreign key(course_id) references course(course_id) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(faculty_id) references faculty(faculty_id) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    """
            self.cur.execute(subject_table) 
        
        # present
        def create_present():
            present_table="""create table if not exists present(
                    present_id int not NULL primary key AUTO_INCREMENT, 
                    stu_roll int not NULL, 
                    sub_id int not NULL, 
                    created_at datetime default now(),
                    foreign key(stu_roll) references student(stu_roll) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(sub_id) references subject(sub_id) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    """
            self.cur.execute(present_table) 
# absent
        def create_absent():
            absent_table="""create table if not exists absent(
                    absent_id int not NULL primary key AUTO_INCREMENT, 
                    stu_roll int not NULL, 
                    sub_id int not NULL, 
                    created_at datetime default now(),
                    foreign key(stu_roll) references student(stu_roll) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(sub_id) references subject(sub_id) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    """
            self.cur.execute(absent_table)
# report
        def create_report():
            report_table="""create table if not exists report(
                    report_id int not NULL primary key AUTO_INCREMENT, 
                    stu_roll int not NULL, 
                    faculty_id int not NULL, 
                    sub_id int not NULL, 
                    course_id int not NULL, 
                    created_at datetime default now(),
                    foreign key(stu_roll) references student(stu_roll) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(faculty_id) references faculty(faculty_id) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(sub_id) references subject(sub_id) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(course_id) references course(course_id) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    """

            self.cur.execute(report_table)

        
            
        try:
            create_admin()
            create_student()
            create_faculty()
            create_course()
            create_subject()
            create_present()
            create_absent()
            create_report()
            print("Created")
        except Exception as e:
            print(e)
        

    #Insert-admin
    def insert_admin(self, admin_id, f_name, l_name, admin_email, admin_pass, phone):
       query="""insert into admin(admin_id, f_name, l_name, admin_email, admin_pass, phone)
            values({},'{}','{}','{}','{}','{}')""".format(admin_id, f_name, l_name, admin_email, admin_pass, phone)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-admin
    def update_admin(self, admin_id, new_f_name, new_l_name, new_admin_email, new_admin_pass, new_phone):
        query="update admin set admin_id={}, f_name='{}', l_name='{}', admin_email='{}', admin_pass='{}' phone='{}' where admin_id={}".format(admin_id, new_f_name, new_l_name, new_admin_email, new_admin_pass, new_phone)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)

# faculty module
    def insert_faculty(self, faculty_id, f_name, l_name, gender, dob, faculty_adrs, faculty_email, faculty_pass, phone):
       query="""insert into faculty(faculty_id, f_name, l_name, gender, dob, faculty_adrs, faculty_email, faculty_pass, phone)
            values({},'{}','{}','{}','{}','{}','{}','{}','{}')""".format(faculty_id, f_name, l_name, gender, dob, faculty_adrs ,faculty_email, faculty_pass, phone)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-faculty
    def update_faculty(self, faculty_id, f_name, l_name, gender, dob, faculty_adrs, faculty_email, faculty_pass, phone):
        query="update faculty set faculty_id={}, f_name='{}', l_name='{}', gender='{}', dob='{}', faculty_adrs='{}', faculty_email='{}', faculty_pass='{}', phone='{}' where faculty_id={}".format(faculty_id, f_name, l_name, gender, dob, faculty_adrs, faculty_email, faculty_pass, phone,faculty_id)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)


        # Delete faculty
    def delete_faculty(self, faculty_id):
        
        query="delete from faculty where faculty_id={}".format(faculty_id)
        print(query)
        cur=self.cnx.cursor()
        
        cur.execute(query)


    #fetch all
    def fetch_all_faculty(self):
        query="select * from faculty"
        self.cur.execute(query)
        print(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

    #fetch one
    def fetch_one_faculty(self, faculty_id):
        query="select * from faculty where faculty_id={}".format(faculty_id)
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

        # print("Deleted")


# insert student
    def insert_student(self, stu_roll, f_name, l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone):
       query="""insert into student(stu_roll, f_name, l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone)
            values({},'{}','{}','{}','{}','{}','{}','{}','{}')""".format(stu_roll, f_name, l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-student
    def update_student(self, stu_roll, f_name, l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone):
        query="update student set stu_roll={}, f_name='{}', l_name='{}', gender='{}', dob='{}', stu_adrs='{}', stu_email='{}', stu_pass='{}', phone='{}' where stu_roll={}".format(stu_roll, f_name, l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone, stu_roll)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)
    


        # Delete student
    def delete_student(self, stu_roll):
        
        query="delete from student where stu_roll={}".format(stu_roll)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)    

    #fetch all
    def fetch_all_student(self):
        query="select * from student"
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

    #fetch one
    def fetch_one_student(self, stu_roll):
        query="select * from student where stu_roll={}".format(stu_roll)
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

# insert course
    def insert_course(self, course_id, course_name, course_desc):
       query="""insert into course(course_id, course_name, course_desc)
            values({},'{}','{}')""".format(course_id, course_name, course_desc)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-course
    def update_course(self, course_id, course_name,course_desc):
        query="update course set course_id={}, course_name='{}', course_desc='{}' where course_id={}".format(course_id, course_name, course_desc, course_id)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)



    #fetch all course
    def fetch_all_course(self):
        query="select * from course"
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

    #fetch one course
    def fetch_one_course(self, course_id):
        query="select * from course where course_id={}".format(course_id)
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

        # Delete cousre
    def delete_course(self, course_id):
        
        query="delete from course where course_id={}".format(course_id)
        print(query)
        cur=self.cnx.cursor()
        
        cur.execute(query)
        # print("Deleted")



# insert subject
    def insert_subject(self, sub_id, sub_name,course_id, faculty_id):
       query="""insert into subject(sub_id, sub_name, course_id, faculty_id)
            values({},'{}',{},{})""".format(sub_id, sub_name,course_id, faculty_id)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-student
    def update_subject(self, sub_id, sub_name,course_id, faculty_id):
        query="update subject set sub_id={}, sub_name='{}', course_id={}, faculty_id={} where sub_id={}".format(sub_id, sub_name, course_id, faculty_id, sub_id)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)

    #fetch all
    def fetch_all_subject(self):
        query="select * from subject s inner join course c on c.course_id=s.course_id inner join faculty f where s.faculty_id=f.faculty_id;"
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

    #fetch one
    def fetch_one_subject(self, sub_id):
        query="select * from subject where sub_id={}".format(sub_id)
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

        # Delete student
    def delete_subject(self, sub_id):
        
        query="delete from subject where sub_id={}".format(sub_id)
        print(query)
        cur=self.cnx.cursor()
        
        cur.execute(query)
        # print("Deleted")


# insert present
    def insert_present(self, present_id, sub_id, stu_roll):
       query="""insert into present(present_id, sub_id, stu_roll)
            values({},{},{})""".format(present_id, sub_id, stu_roll)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-student
    def update_present(self, present_id, sub_id, stu_roll):
        query="update present set present_id={}, sub_id={}, stu_roll={} where present_id={}".format(present_id, sub_id, stu_roll)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)



    #fetch all
    def fetch_all_present(self):
        query="select * from present"
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

    #fetch one
    def fetch_one_present(self, present_id):
        query="select * from present where present_id={}".format(present_id)
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

        # Delete student
    def delete_present(self, present_id):
        
        query="delete from present where present_id={}".format(present_id)
        print(query)
        cur=self.cnx.cursor()
        
        cur.execute(query)
        # print("Deleted")



# insert absent
    def insert_absent(self, absent_id, stu_roll, sub_id):
       query="""insert into absent(absent_id, stu_roll, sub_id)
            values({},{},{})""".format(absent_id, stu_roll, sub_id)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-student
    def update_absent(self, absent_id, stu_roll, sub_id):
        query="update absent set absent_id={}, stu_roll={}, sub_id={} where absent_id={}".format(absent_id, stu_roll, sub_id)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)
        

    #fetch all
    def fetch_all_absent(self):
        query="select * from absent"
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

    #fetch one
    def fetch_one_absent(self, absent_id):
        query="select * from student where absent_id={}".format(absent_id)
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

        # Delete student
    def delete_absent(self, absent_id):
        
        query="delete from absent where absent_id={}".format(absent_id)
        print(query)
        cur=self.cnx.cursor()
        
        cur.execute(query)
        # print("Deleted")

