import mysql.connector as connector

class DBHelper:
    #Creating constractor
    def __init__(self):
        self.cnx=connector.connect(host='localhost',
                port='3306',
                user='root',
                password='root',
                database='pythonTest')
        query="""create table if not exists user(
                userId int primary key, 
                userName varchar(255), 
                phone varchar(12))"""
        cur=self.cnx.cursor()
        cur.execute(query)
        print("Created")