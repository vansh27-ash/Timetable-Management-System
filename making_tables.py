from mysql.connector import connect
from tkinter.messagebox import showinfo,showerror,showwarning


def startup(password, db_for_Teacher, db_for_Student, Classes):
    
    try:
        Db1 = connect(host='localhost', user='root', passwd=password, database=db_for_Teacher, charset='utf8')
        Db2 = connect(host='localhost', user='root', passwd=password, database=db_for_Student, charset='utf8')
    except:
        showerror('Error','An unexpected error occured')
    if not Db1.is_connected() and not Db2.is_connected():
        showwarning('Warning','Unable to connect to mysql')
    else:
        cursor1 = Db1.cursor()
        cursor2 = Db2.cursor()

        cursor2.execute('''Create table student
        (
            name varchar(50),
            email_id varchar(50),
            phone_number varchar(15),
            class varchar(5),
            password varchar(65),
            school_id varchar(15)
        )''')

        query = 'create table classes (Class varchar(15),'
        days = ['Mon','Tue','Wed','Thurs','Fri','Sat']
        for i in days:
            for j in range(8):
                query+=f"{i}{j+1} varchar(40),"
        query = query.strip(',')+')'
        cursor2.execute(query)
        for i in range(1,Classes+1):
            for j in ('A','B'):
                query='insert into classes values('
                query+=f"'class{i}{j}',"
                query+='null,'*47+'null)'
                cursor2.execute(query)
                Db2.commit()

        cursor1.execute('''Create table teacher
        (
            name varchar(50),
            email_id varchar(50),
            phone_number varchar(15),
            password varchar(65),
            school_id varchar(15),
            subject varchar(100)
        )''')

        query = 'create table timetable (Tablename varchar(40),'
        days = ['Mon','Tue','Wed','Thurs','Fri','Sat']
        for i in days:
            for j in range(8):
                query+=f"{i}{j+1} char(3),"
        query = query.strip(',')+')'
        cursor1.execute(query)
        
        Db1.close(),Db2.close()
