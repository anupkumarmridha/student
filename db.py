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
                    s_f_name varchar(255) not NULL,
                    s_l_name varchar(255) not NULL,
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

        def create_enroll():
            course_table="""create table if not exists enroll(
                    enroll_id int not NULL AUTO_INCREMENT primary key, 
                    stu_roll int not NULL,
                    course_id int not NULL,
                    created_at datetime default now(),
                    updated_at datetime default now(),
                    foreign key(stu_roll) references student(stu_roll) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(course_id) references course(course_id) ON UPDATE CASCADE ON DELETE CASCADE
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
        
        # attendance
        def create_attendance():
            attendance_table="""create table if not exists attendance(
                    id int not NULL primary key AUTO_INCREMENT, 
                    status char(1) not NULL, 
                    stu_roll int not NULL, 
                    sub_id int not NULL, 
                    on_date datetime default now(),
                    foreign key(stu_roll) references student(stu_roll) ON UPDATE CASCADE ON DELETE CASCADE,
                    foreign key(sub_id) references subject(sub_id) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    """
            self.cur.execute(attendance_table) 
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
            # create_admin()
            create_student()
            create_faculty()
            create_course()
            create_enroll()
            create_subject()
            create_attendance()
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
    def insert_student(self, stu_roll, s_f_name, s_l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone):
       query="""insert into student(stu_roll, s_f_name, s_l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone)
            values({},'{}','{}','{}','{}','{}','{}','{}','{}')""".format(stu_roll, s_f_name, s_l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-student
    def update_student(self, stu_roll, s_f_name, s_l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone):
        query="update student set stu_roll={}, s_f_name='{}', s_l_name='{}', gender='{}', dob='{}', stu_adrs='{}', stu_email='{}', stu_pass='{}', phone='{}' where stu_roll={}".format(stu_roll, s_f_name, s_l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone, stu_roll)
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

# insert enroll
    def insert_enroll(self,stu_roll, course_id):
       query="""insert into enroll(stu_roll,course_id)
            values({},{})""".format(stu_roll,course_id)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    def fetch_course_enroll(self, course_id):
        query="""select * from enroll e inner join student s on e.stu_roll=s.stu_roll
         where course_id={}""".format(course_id)
        print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
        self.cur.execute(query)
        
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return 0

    def fetch_one_enroll(self, enroll_id):
        query="select * from enroll where enroll_id={}".format(enroll_id)
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}
    
    def check_course_enroll(self,course_id):
        query="select * from enroll where course_id={}".format(course_id)
        self.cur.execute(query)
        result=self.cur.fetchall()
        print(query)
        if len(result)>0:
            # return json.dumps(result)
            return 1
        else:
            return 0
    
    def fetch_not_enrolled_students(self):
        query="""select * from enroll e right join student s on e.stu_roll=s.stu_roll
         where e.course_id is NULL ;"""
        self.cur.execute(query)
        result=self.cur.fetchall()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}


    def delete_enroll(self, enroll_id):
        query="delete from enroll where enroll_id={}".format(enroll_id)
        print(query)
        cur=self.cnx.cursor()
        
        cur.execute(query)


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

    def fetch_course_single_subject(self, sub_id):
        query="""
                select * from course c inner join subject s on c.course_id=s.course_id
                where s.sub_id={}""".format(sub_id)
        print(query)
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return {"message":"No data Found"}

    def fetch_subject_students(self, sub_id):
        query="""
            select * from enroll e inner join student s on e.stu_roll=s.stu_roll 
            inner join course c on e.course_id=c.course_id 
            inner join subject sub where sub.course_id= e.course_id and sub_id={}; 
            """.format(sub_id)
        print(query)
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return []
        
# insert present
    def insert_attendance(self, status, sub_id, stu_roll):
       query="""insert into attendance(status, stu_roll, sub_id)
            values('{}',{},{})""".format(status, stu_roll, sub_id)
       print(query)
    #    cur=self.cnx.cursor()    #curser method is come from connection
       self.cur.execute(query)
    #    self.cnx.commit()    #commit method come from connection

    # update-student
    def update_attendance(self, status, sub_id, stu_roll):
        query="update present set status='{}' where sub_id={}, stu_roll={}".format(status, sub_id, stu_roll)
        print(query)
        cur=self.cnx.cursor()
        cur.execute(query)

    def fetch_subject_attendance(self,sub_id):
        query="""select * from attendance a inner join student s
                inner join subject sub inner join course c 
                inner join faculty f where a.stu_roll=s.stu_roll and 
                sub.sub_id=a.sub_id and a.sub_id={} and c.course_id=sub.course_id 
                and sub.faculty_id=f.faculty_id""".format(sub_id)
        
        print(query)
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return 0
            
    def fetch_subject_total_student(self,sub_id):
        query="select count(distinct(stu_roll)) as totalStudent from attendance where sub_id={}".format(sub_id)
        print(query)
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return 0

    def fetch_subject_total_present(self,sub_id):
        query="select count(status) as present from attendance where sub_id={} and status='P'".format(sub_id)
        print(query)
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return 0
    
    def fetch_subject_total_absent(self,sub_id):
        query="select count(status) as absent from attendance where sub_id={} and status='A'".format(sub_id)
        print(query)
        self.cur.execute(query)
        result=self.cur.fetchall()
        # cur=self.cnx.cursor()
        if len(result)>0:
            # return json.dumps(result)
            return result
        else:
            return 0
