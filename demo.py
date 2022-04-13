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
        query="update student set stu_roll={}, f_name='{}', l_name='{}', gender='{}', dob='{}', stu_adrs='{}', stu_email='{}', stu_pass='{}' phone='{}' where stu_roll={}".format(stu_roll, f_name, l_name, gender, dob, stu_adrs ,stu_email, stu_pass, phone)
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