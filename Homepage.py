from tkinter import *
import hashlib
import mysql.connector as mysql
from Add_ import *
import login
from _info_ import *
from tkinter.ttk import Combobox

def Home(win, position):
    global db
    win.destroy()
    root = Tk()
    root.title('Login'),root.config(background='black')
    root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0')
    
    
    Name = StringVar()
    School_ID = StringVar()
    Password = StringVar()
    Admin_ID = StringVar()
    Cls = StringVar()
   
 
    var = StringVar()
    var1 = StringVar()

    if position == 'admin':
        db = mysql.connect(host='localhost', user='root', passwd=password, database=database_info, charset='utf8') 
        Table = 'admins'
    elif position == 'Student':
        db = mysql.connect(host='localhost', user='root', passwd=password, database=database_info_S, charset='utf8')
        Table = 'student'
    elif position == 'Teacher':
        db = mysql.connect(host='localhost', user='root', passwd=password, database=database_info_T, charset='utf8')
        Table = 'teacher'


    
   
    var1.set('DISABLED')
    var.set('DISABLED')

    frame = LabelFrame(root, bg='dark orange', borderwidth=20, padx=50, pady=20)
    frame.grid(row=0, column=0, padx=50, pady=50, columnspan=5)

    label = Label(frame, text='Welcome', font=('helvetica', 50), padx=100, pady=20, relief=RAISED)
    label.grid(row=0, column=0, columnspan=5, padx=100)

    L1 = Label(frame, text='Name', font=('Helvetica', 20), anchor=W, relief=RAISED)
    L2 = Label(frame, text='School ID', font=('Helvetica', 20), anchor=W, relief=RAISED)
    L3 = Label(frame, text='Password', font=('Helvetica', 20), anchor=W, relief=RAISED)
    if position =='admin':
        L4 = Label(frame, text='Admin ID', font=('Helvetica', 20), anchor=W, relief=RAISED)
        L4.grid(row=4, column=0, sticky=W+E, pady=10)
    else:
        text = 'If you are logging in for first time then leave password\nYou can change it any time but other details must match'
        L4 = Label(frame, text=text, font=('Rockwell', 20), anchor=W,bg='dark orange')
        L4.grid(row=4, column=0, columnspan=2,sticky=W+E, pady=10)

    L1.grid(row=1, column=0, sticky=W+E, pady=10)
    L2.grid(row=2, column=0, sticky=W+E, pady=10)
    L3.grid(row=3, column=0, sticky=W+E, pady=10)

    if position == 'Student':
        L5 = Label(frame, text='Class', font=('Helvetica', 20), anchor=W, relief=RAISED)
        L5.grid(row=5, column=0, sticky=W+E, pady=10)

    def Set(var):
        '''it enable or disable signup and login buttons and this function is called through radio buttons'''
        if position == 'Student':
            b1 = Button(frame, text='Login', relief=RAISED, padx=100, command=lambda:Login(Name, School_ID, Password, Cls), state=eval(var.get()))
        else:
            b1 = Button(frame, text='Login', relief=RAISED, padx=100, command=lambda:Login(Name, School_ID, Password, Cls), state=eval(var.get()))
        b1.grid(row=4, column=2, pady=10, padx=100, columnspan=5)

    frame2 = LabelFrame(frame, borderwidth=10, bg='red', pady=5)
    frame2.grid(row=1, column=4)
    r1 = Radiobutton(frame2, text='Enable', indicatoron=0, variable=var, relief=SUNKEN, value='NORMAL', command=lambda : Set(var), bg='red')
    r2 = Radiobutton(frame2, text='Disable',  indicatoron=0, variable=var, relief=SUNKEN, value='DISABLED', command=lambda : Set(var), bg='red')
    r1.grid(row=0, column=1)
    r2.grid(row=0, column=2)

    e1 = Entry(frame, textvariable=Name, borderwidth=3, fg='grey', width=50, font=('helvetica, 15'), relief=SUNKEN)
    e2 = Entry(frame, textvariable=School_ID, borderwidth=3, fg='grey', font=('helvetica, 15'), relief=SUNKEN)
    e3 = Entry(frame, textvariable=Password, show='*', borderwidth=3, fg='grey', font=('helvetica, 15'), relief=SUNKEN)
    if position =='admin':
        e4 = Entry(frame, textvariable=Admin_ID, borderwidth=3, fg='grey', font=('helvetica, 15'), relief=SUNKEN)
        e4.grid(row=4, column=1, sticky=W+E, pady=10, padx=10)
        e4.insert(0,"Enter Your Admin Id")
        e4.bind('<Button-1>',  lambda event: e4.delete(0,END))
        
    e1.grid(row=1, column=1, sticky=W+E, pady=10, padx=10)
    e2.grid(row=2, column=1, sticky=W+E, pady=10, padx=10)
    e3.grid(row=3, column=1, sticky=W+E, pady=10, padx=10)
    
    e1.insert(0,"Enter Your Name")
    e2.insert(0,"Enter Your School Id")
    e3.insert(0,"")

    e1.bind('<Button-1>',  lambda event: e1.delete(0,END))
    e2.bind('<Button-1>',  lambda event: e2.delete(0,END))

    if position == 'Student':
        available = ()
        for  i in range(1,Classes+1):
            available += (f'{i}A',)
            available += (f'{i}B',)
        box = Combobox(frame, textvariable=Cls, values=available, font=('helvetica',15), state='readonly')
        box.grid(row=5, column=1, sticky=W+E, pady=10, padx=10)
        box.current(0)


    def Secure(Password):
        '''create a hash value for  input password
        which is to be compaired with the hashvalue of the user password(which the user gave durig signup) ,stored in db
        and hashvalue is of no use it is just for comparison and its quality is its unique for a given input
        '''    
        return hashlib.sha256(Password.encode()).hexdigest()

    def Login(Name, School_ID, Password, Cls):
        global db
        '''called when user press login button,
        first create connection between db in case it is lost, then excute the query based on the given 
        input in the entry boxes and show the result if found
        '''

        cursor = db.cursor()
        if position =='Student':
           
            query = f" select * from {Table} where Name = '{Name.get()}'and School_ID = '{School_ID.get()}' and Class = '{Cls.get()}' and password  = '{Secure(Password.get())}' "
            
        else:
            query = f" select * from {Table} where Name = '{Name.get()}'and School_ID = '{School_ID.get()}' and password = '{Secure(Password.get())}'"
        
        cursor.execute(query)
        Record = cursor.fetchall()
     
        
        if Record:
            if position == 'Student':
                root.destroy()
                login.logged_stu(School_ID.get())
            elif position == 'Teacher':
                root.destroy()
                login.logged_tea(School_ID.get())
            elif position == 'admin':
                root.destroy()
                login.logged_adm()
        
        else:
            root3 = Toplevel(root)
            root3.title("NO RECORD")
            root3.geometry('600x300')
            root3.resizable(0,0)
            
            frame4 = LabelFrame(root3, borderwidth=4, bg='black', padx=20, pady=5)
            frame4.pack(fill='both',expand=1)
            t='>>No Record Found\n>>Please check if everything filled\nis same as given by admin.\n>>If yes, then please contact admin.\nor maybe you have changed your password\n'
            db_ = mysql.connect(host='localhost', user='root', passwd=password, database=database_info, charset='utf8')
            dbc= db_.cursor()
            dbc.execute('select email_id,phone_number from admins')
            info = dbc.fetchall()[0]
            db_.close()
            t+=f'Phone number :- >>{info[1]}.\n>>Email_id :- {info[0]}.'
            l2 = Label(frame4, text=t, bg='dark orange', font=('helvetica', 20), padx=10, justify='left')
            l2.pack(expand=1,fill='both')
            root3.mainloop()
                      

    b1 = Button(frame, text='Login', relief=RAISED, padx=100, command=lambda:Login(Name, School_ID, Password, Cls), state=eval(var.get()))
    b1.grid(row=4, column=2, pady=10, padx=100, columnspan=5)
    
    root.mainloop()
