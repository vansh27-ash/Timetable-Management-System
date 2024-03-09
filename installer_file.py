import tkinter as tk
from tkinter import ttk
import hashlib
import mysql.connector as mysql
import string
from random import choice
import making_tables as make
from tkinter.messagebox import showwarning, showinfo
from threading import Thread

def install():
    Start_win_ = tk.Tk()	
    Start_win_.title('TIMETABLE MANAGEMENT SYSTEM')
    icon = tk.PhotoImage(file = 'icon.png')
    Start_win_.iconphoto(1,icon)
    Start_win_.geometry(f'{Start_win_.winfo_screenwidth()}x{Start_win_.winfo_screenheight()}+0+0')
    img = tk.PhotoImage(file='back.png')
    img=img.zoom(2)
    Start_win = tk.Label(Start_win_,image=img,bg='#895ee3')
    Start_win.pack(fill='both',expand=1)
    frame = tk.LabelFrame(Start_win, bg='#895ee3', bd=0, padx=100, pady=10)
    frame.grid(row=0, column=0, padx=250, pady=40, columnspan=5)

    l1 = tk.Label(frame, text='TIMETABLE MANAGEMENT', font=('helvetica', 30), bd=0, bg='#895ee3')
    l2 = tk.Label(frame, text='SYSTEM', font=('helvetica', 30), bd=0, bg='#895ee3')

    l1.grid(row=0, column=0, padx=10)
    l2.grid(row=1, column=0, padx=10)


    def agreed(win):
        '''connect to mysql server and creates db if not present in mysql server 
        also creates table to store admin data'''
        if 1<= Classes.get() <=12:
            
            global  db, cursor

            db_for_admin = database_info.get()
            db_for_Teacher = database_info_T.get()
            db_for_Student = database_info_S.get()
            password = pass_info.get()

            win.destroy()
            if password == '':
                db = mysql.connect(host='localhost', user='root', passwd='', charset='utf8')
            else:
                db = mysql.connect(host='localhost', user='root', passwd=password, charset='utf8')

            cursor = db.cursor()
            cursor.execute('show databases')
            info = cursor.fetchall()
            
            if (db_for_admin.lower(),) in info:
                cursor.execute(f'use {db_for_admin}')
            else:
                cursor.execute(f'create database {db_for_admin}')
                cursor.execute(f'create database {db_for_Teacher}')
                cursor.execute(f'create database {db_for_Student}')

                cursor.execute(f'use {db_for_admin}')
                
            cursor.execute('show tables')

            tables  = cursor.fetchall()
            if ('admins',) not in tables:
                cursor.execute('''Create table Admins
                    (
                        name varchar(50),
                        email_id varchar(50),
                        phone_number varchar(15),
                        password varchar(65),
                        school_id varchar(15),
                        Admin_Id varchar(100)
                    )''')
            
            Admin()
        else:
            showwarning('Warning','classes should be in the range 1-12 where 1 & 12 are included')  


    def Terms(win):
        '''to inform the user/admin about the program services and also fetch the db name and mysql password(if any)
        if db is not created then it will create it''' 
        l1.destroy()
        l2.destroy()
        b.destroy()

        global database_info, pass_info, database_info_T, database_info_S, Classes, School_name

        TandC='''1.This software requires access to your mysql\nso please give the details about the password and
the database to be used(database with that name\nshould not be existing for best experience)
2.If not using password just don't write anything
3.Please ensure that you have installed
mysql.connector ; if not install using pip'''
        
        tk.Label(win,text=TandC,font=('Rockwell',15),width=50, justify='left', bg='#895ee3').grid(row=0,column=0, pady=5,columnspan=3)
        
        database_info = tk.StringVar()
        database_info_T = tk.StringVar()
        database_info_S = tk.StringVar()
        Classes = tk.IntVar()
        School_name = tk.StringVar()

        pass_info = tk.StringVar()
        
        tk.Label(win,text='Enter the database name to be used for admin',font=('Rockwell',15), bg='#895ee3', anchor=tk.W).grid(row=1,column=0,pady=5, sticky=tk.W+tk.E)
        tk.Entry(win,font=('Rockwell',15),textvariable=database_info).grid(row=1,column=1,pady=5)
        
        
        tk.Label(win,text='Enter the database name to be used for Teachers',font=('Rockwell',15), bg='#895ee3').grid(row=2,column=0,pady=5)
        tk.Entry(win,font=('Rockwell',15),textvariable=database_info_T).grid(row=2,column=1,pady=5)

        tk.Label(win,text='Enter the database name to be used for Students',font=('Rockwell',15), bg='#895ee3').grid(row=3,column=0,pady=5)
        tk.Entry(win,font=('Rockwell',15),textvariable=database_info_S).grid(row=3,column=1,pady=5)

        tk.Label(win,text='How many classes are there in your institution',font=('Rockwell',15), bg='#895ee3', anchor=tk.W).grid(row=4,column=0,pady=5, sticky=tk.W+tk.E)
        tk.Entry(win,font=('Rockwell',15),textvariable=Classes).grid(row=4,column=1,pady=5)

        tk.Label(win,text='Enter your Institution Name',font=('Rockwell',15), bg='#895ee3', anchor=tk.W).grid(row=5,column=0,pady=5, sticky=tk.W+tk.E)
        tk.Entry(win,font=('Rockwell',15),textvariable=School_name).grid(row=5,column=1,pady=5)


        tk.Label(win,text='Enter the password',font=('Rockwell',15), bg='#895ee3').grid(row=6,column=0,pady=5)
        tk.Entry(win,font=('Rockwell',15),show='*',textvariable=pass_info).grid(row=6,column=1,pady=5)
        
        tk.Button(win,text='I Agree',font=('Rockwell',20,'underline'),fg='white',bg='black',command=lambda:agreed(win)).grid(row=7,columnspan=3,pady=10)




    '''Admin'''
    def Admin():
        global frame
        '''register  admin to the db and create db in which all the record wil be saved'''
        
        frame = tk.LabelFrame(Start_win, bg='blue', bd=5, padx=10, pady=10)
        frame.grid(row=0, column=0, padx=280, pady=(110,10), columnspan=5)


        Name = tk.StringVar()
        Phone_number = tk.StringVar()
        Email_ID = tk.StringVar()
        Admin_ID = tk.StringVar()

        Password1 = tk.StringVar()
        Password2 = tk.StringVar()

        state1 = tk.StringVar()
        
        state1.set('tk.NORMAL')

        L1 = tk.Label(frame, text='Name', font=('Helvetica', 20), anchor=tk.W, relief=tk.RAISED)
        L2 = tk.Label(frame, text='Email Id', font=('Helvetica', 20), anchor=tk.W, relief=tk.RAISED)
        L3 = tk.Label(frame, text='Password', font=('Helvetica', 20), anchor=tk.W, relief=tk.RAISED)
        L4 = tk.Label(frame, text='Confirm Password', font=('Helvetica', 20), anchor=tk.W, relief=tk.RAISED)
        L5 = tk.Label(frame, text='Admin ID', font=('Helvetica', 20), anchor=tk.W, relief=tk.RAISED)
        L6 = tk.Label(frame, text='Phone Number', font=('Helvetica', 20), anchor=tk.W, relief=tk.RAISED)

        L1.grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)
        L2.grid(row=2, column=0, sticky=tk.W+tk.E, pady=10)
        L3.grid(row=3, column=0, sticky=tk.W+tk.E, pady=10)
        L4.grid(row=4, column=0, sticky=tk.W+tk.E, pady=10)
        L5.grid(row=5, column=0, sticky=tk.W+tk.E, pady=10)
        L6.grid(row=6, column=0, sticky=tk.W+tk.E, pady=10)

        e1 = tk.Entry(frame, textvariable=Name, borderwidth=3, fg='grey', width=50, font=('helvetica, 15'), relief=tk.SUNKEN)
        e2 = tk.Entry(frame, textvariable=Email_ID, borderwidth=3, fg='grey', font=('helvetica, 15'), relief=tk.SUNKEN)
        e3 = tk.Entry(frame, textvariable=Password1, show='*', borderwidth=3, fg='grey', font=('helvetica, 15'), relief=tk.SUNKEN)
        e4 = tk.Entry(frame, textvariable=Password2, show='*', borderwidth=3, fg='grey', font=('helvetica, 15'), relief=tk.SUNKEN)
        e5 = tk.Entry(frame, textvariable=Admin_ID, borderwidth=3, fg='grey', font=('helvetica, 15'), relief=tk.SUNKEN)
        e6 = tk.Entry(frame, textvariable=Phone_number, borderwidth=3, fg='grey', font=('helvetica, 15'), relief=tk.SUNKEN)

        e1.grid(row=1, column=1, sticky=tk.W+tk.E, pady=10, padx=10)
        e2.grid(row=2, column=1, sticky=tk.W+tk.E, pady=10, padx=10)
        e3.grid(row=3, column=1, sticky=tk.W+tk.E, pady=10, padx=10)
        e4.grid(row=4, column=1, sticky=tk.W+tk.E, pady=10, padx=10)
        e5.grid(row=5, column=1, sticky=tk.W+tk.E, pady=10, padx=10)
        e6.grid(row=6, column=1, sticky=tk.W+tk.E, pady=10, padx=10)

        e1.insert(0,"Enter Your Name")
        e2.insert(0,"Enter Your Email Id")
        e5.insert(0,"Enter Your Admin Id")
        e6.insert(0,"Enter Your Phone Number")


        e1.bind('<Button-1>', lambda event : e1.delete(0,tk.END))
        e2.bind('<Button-1>',lambda event : e2.delete(0,tk.END))
        e5.bind('<Button>', lambda event : e5.delete(0,tk.END))
        e6.bind('<Button>', lambda event : e6.delete(0,tk.END))

        def Submit(Name, Phone, Email, Password, Admin_ID):
                
                frame.destroy()
                '''create account for the user and store it in a table of given database'''
                global Id

                p = hashlib.sha256(Password.get().encode()).hexdigest()
                
                Id = School_name.get()[:2]+'_'+(hashlib.sha256(f'{Name.get()} {Phone.get()} {Email.get()} {Password.get()} {Admin_ID.get()}{School_name.get()}'.encode()).hexdigest())[0: 5]+ Name.get()[0:2] 
                
                cursor.execute(f'insert into Admins values("{Name.get()}","{Email.get()}","{Phone.get()}","{p}","{Id}","{Admin_ID.get()}")')
                db.commit()
                db.close()
                
                
                frame4 = tk.LabelFrame(Start_win, borderwidth=5, bg='#895ee3')
                frame4.grid(row=1, column=0, padx=200, pady=2, sticky=tk.W+tk.E)

                tk.Label(frame4, text=f'Name:- {Name.get()}', bg='#895ee3', anchor=tk.W).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
                tk.Label(frame4, text=f'Phone_number:- {Phone.get()}', bg='#895ee3', anchor=tk.W).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
                tk.Label(frame4, text=f'Email_ID:- {Email.get()}', bg='#895ee3', anchor=tk.W).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
                tk.Label(frame4, text=f'Your Unique School id is {Id}', bg='#895ee3', anchor=tk.W).grid(row=0, column=1, padx=100, pady=5, sticky=tk.W+tk.E)
                tk.Label(frame4, text=f'Admin iD {Admin_ID.get()}', bg='#895ee3', anchor=tk.W).grid(row=1, column=1, padx=100, pady=5, sticky=tk.W+tk.E)

                with open('_info_.py','w') as file:
                    file.write(f'database_info = "{database_info.get()}"\n')
                    file.write(f'database_info_T = "{database_info_T.get()}"\n')
                    file.write(f'database_info_S = "{database_info_S.get()}"\n')
                    file.write(f'Classes = {Classes.get()}\n')
                    file.write(f'password = "{pass_info.get()}"\n')
                    file.write(f'School_name = "{School_name.get()}"\n')

                def Show():
                    Thread(target=make.startup,args=(pass_info.get(), database_info_T.get(),database_info_S.get(), Classes.get())).start()
                    showinfo('INFO','Everthing saved please run the file again')
                    Start_win_.destroy()
                    
                b = ttk.Button(frame4, text='Next', command=Show, width=20)
                b.grid(row=2, column=2, padx=10)
                    
                    

        def Upadte():
            '''checks whether the password is right'''
            if Password1.get() == Password2.get() and (Phone_number.get() not in ['', "Enter Your Phone Number"]) and (Name.get() not in ['',"Enter Your Name"]) and (Email_ID.get() not in ['',"Enter Your Email Id"] and (Admin_ID.get() not in ["Enter Your Admin Id"])):
                b1 = tk.Button(frame, text='create', relief=tk.RAISED, padx=10, command=lambda :Submit(Name, Phone_number, Email_ID, Password1, Admin_ID), state=tk.NORMAL)
            else:
                b1 = tk.Button(frame, text='create', relief=tk.RAISED, padx=10, command=lambda :Submit(Name, Phone_number, Email_ID, Password1, Admin_ID), state=tk.DISABLED)
            b1.grid(row=3, column=2, pady=5, sticky=tk.W+tk.E, columnspan=2)



        def Suggest():
            '''Suggest the  admin the admin id'''
            global ad_id
            salt = choice(string.printable[0:62])
            if (Name.get() not in ['',"Enter Your Name"]): 
                ad_id = f'{School_name.get()[:2]}_{hashlib.sha256(salt.encode()).hexdigest()[0:5]}{Name.get()[0:2]}'
                e5.delete(0, tk.END)
                e5.insert(0,ad_id)
                
            
        b1 = tk.Button(frame, text='create', relief=tk.RAISED, padx=10, command=lambda :Submit(Name, Phone_number, Email_ID, Password1, Admin_ID), state=tk.DISABLED)
        b1.grid(row=3, column=2, pady=5, sticky=tk.W+tk.E, columnspan=2)

        b2 = tk.Button(frame, text='Confirm', relief=tk.RAISED, padx=10, command=Upadte, state=eval(state1.get()))
        b2.grid(row=4, column=2, sticky=tk.W+tk.E, pady=10, columnspan=2)

        b3 = tk.Button(frame, text='Suggest', relief=tk.RAISED, padx=10, command=Suggest, state=eval(state1.get()))
        b3.grid(row=5, column=2, pady=5, sticky=tk.W+tk.E, columnspan=2)


    b = ttk.Button(frame, text='Next', command=lambda:Terms(frame), width=20)
    b.grid(row=2, column=1, padx=10)

    Start_win_.mainloop()
