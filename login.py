import tkinter as tk
from tkinter.ttk import Notebook
from tkinter.messagebox import showwarning
from mysql.connector import connect
import _info_
from Add_ import*
from threading import Thread

def change_password(position,scid):
    def Secure(Password):
        '''create a hash value for  input password
        which is to be compaired with the hashvalue of the user password(which the user gave durig signup) ,stored in db
        and hashvalue is of no use it is just for comparison and its quality is its unique for a given input
        '''    
        return hashlib.sha256(Password.encode()).hexdigest()
    def take():
        if position=='teacher':
            db=connect(host='localhost',user='root',database=_info_.database_info_T,passwd=_info_.password,charset='utf8')
            query = f"update teacher set password='{Secure(e2.get())}' where school_id='{scid}'"
        else:
            db=connect(host='localhost',user='root',database=_info_.database_info_S,passwd=_info_.password,charset='utf8')
            query = f"update student set password='{Secure(e2.get())}' where school_id='{scid}'"
        dbc = db.cursor()
        dbc.execute(f"select password from {position} where school_id = '{scid}'")
        oldpass = dbc.fetchall()[0][0]
        if oldpass == Secure(e1.get()):
            dbc.execute(query)
            db.commit()
        else:
            showwarning('Warning','Old password not matched\nhence no changes saved')
        db.close()
        win.destroy()
        
    win = tk.Tk()
    win.title('Change Password'),win.resizable(0,0),win.config(background='blue'),win.geometry('750x300')
    tk.Label(win,text='Enter old password',bg='blue',fg='white',font=('Rockwell', 18, 'italic'),width=25).grid(row=0,column=0,padx=20,pady=10)
    tk.Label(win,text='Enter new password',bg='blue',fg='white',font=('Rockwell', 18, 'italic'),width=25).grid(row=1,column=0,padx=20,pady=10)
    e1 = tk.Entry(win,show='*',font=('Rockwell', 18, 'italic'),width=25)
    e2 = tk.Entry(win,show='*',font=('Rockwell', 18, 'italic'),width=25)
    e1.grid(row=0,column=1,padx=20,pady=10),e2.grid(row=1,column=1,padx=20,pady=10)
    tk.Button(win,text='Confirm',font=('Rockwell', 18, 'italic'),width=25,command=take).grid(row=3,column=0,columnspan=2,padx=40,pady=10)
    tk.Label(win,text='Caution:-This information of your passwords is not with\nadmin.Therefore please remember it',bg='blue',fg='white',font=('Rockwell', 18, 'italic')).grid(row=4,column=0,columnspan=2,pady=10)
    win.mainloop()
    
def logged_tea(idt):

    mainwin = tk.Tk()
    mainwin.geometry(f'{mainwin.winfo_screenwidth()}x{mainwin.winfo_screenheight()}+0+0')
    mainwin.title('LOGGED IN')
    
    root = Notebook(mainwin)
    root.pack(expand=1,fill='both')
    
    con_obj = connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_T, charset='utf8')
    cur_obj = con_obj.cursor()
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Info<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    
    frame1 = tk.Frame(root,bg='blue')
    frame1.pack(fill='both',expand=1)
    frame1i = tk.Frame(frame1,bg='blue')
    frame1i.pack(pady = 50)
    
    cur_obj.execute(f"select*from teacher where school_id='{idt}'")
    
    information = cur_obj.fetchall()[0]
    information = information[:3] + information[4:]
   
    heading = ['Name','email_id','phone_number','school_id','subject']
    name=information[0]
    
    for i in range(0,len(information),2):
        if i!= 4:
            tk.Label(frame1i, text=f'{heading[i].capitalize()} :- {information[i]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=0,ipadx=50,padx=20,pady=20)
            tk.Label(frame1i, text=f'{heading[i+1].capitalize()} :- {information[i+1]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=1,ipadx=50,padx=20,pady=20)
            
        else:
            tk.Label(frame1i, text=f'{heading[4].capitalize()} :- {information[4]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=0,ipadx=50,padx=20,pady=20)
    tk.Button(frame1,text='Change My Password',font=('Rockwell', 18, 'italic'),bg='black',fg='cyan',relief='groove',command=lambda:change_password('teacher',idt)).pack(side = 'bottom',pady=20)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Timetable Show<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame2 = tk.Frame(root,bg='blue')
    frame2.pack(fill='both',expand=1)
    
    cur_obj.execute(f"select*from timetable where tablename='{name}_{idt}'")
    
    info_of_all = cur_obj.fetchall()[0][1:]
    l_side=['PERIOD',1,2,3,4,5,6,7,8]
    list_of_headings = ['MONDAY', 'TUESDAY','WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
    f2=tk.Frame(frame2,bg='blue')
    f2.pack(side='left',pady=25)
    frame2i = tk.Frame(frame2,bg='blue')
    frame2i.pack(pady=25,side='left')
    tk.Label(frame2,text='\n\n'.join(['T','I','M','E','T','A','B','L','E']), font=('Calibri', 20, 'italic'), width=14,bg='black', fg='cyan',relief='groove',bd=5).pack(side='left',pady=32,fill='y')
    for i in range(9):
        tk.Label(f2,text=l_side[i], font=('Calibri', 17, 'italic'), width=14, height=2, bg='black', fg='cyan',relief='groove',bd=5).grid(row=i, column=0)
    for i in range(len(list_of_headings)):
        tk.Label(frame2i, text=list_of_headings[i], font=('Calibri', 17, 'italic'), width=14, height=2, bg='black', fg='cyan',relief='groove',bd=5).grid(row=0, column=i)
        
    k = 0
    i = 0
    for j in range(len(info_of_all)):
        i+=1
        tk.Label(frame2i, text=info_of_all[j], font=('Calibri', 17, 'italic'), width=14, height=2, bg='black', fg='cyan',relief='groove',bd=5).grid(row=i, column=k)
        if (j+1)%8==0 and j!=0:
            i = 0
            k += 1
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    root.add(frame1,text = '                   INFORMATION                 ')        
    root.add(frame2,text = '                    TIMETABLE                  ')
    
    mainwin.mainloop()

def logged_stu(ids):
    mainwin = tk.Tk()
    mainwin.geometry(f'{mainwin.winfo_screenwidth()}x{mainwin.winfo_screenheight()}+0+0')
    mainwin.title('LOGGED IN')
    
    root = Notebook(mainwin)
    root.pack(expand=1,fill='both')
    
    con_obj = connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_S, charset='utf8')
    cur_obj = con_obj.cursor()
    mycon = connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_T, charset='utf8')
    mycur = mycon.cursor()
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Info<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame1 = tk.Frame(root,bg='blue')
    frame1.pack(fill='both',expand=1)
    
    frame1i = tk.Frame(frame1,bg='blue')
    frame1i.pack(pady = 50)
    
    cur_obj.execute(f"select*from student where school_id='{ids}'")
    
    information = cur_obj.fetchall()[0]
    information = information[:4] + (information[-1],)
    
    heading = ['Name','email_id','phone_number','class','school_id']
    cls=information[3]
    for i in range(0,len(information),2):
        if i!= 4:
            tk.Label(frame1i, text=f'{heading[i].capitalize()} :- {information[i]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=0,ipadx=50,padx=20,pady=20)
            tk.Label(frame1i, text=f'{heading[i+1].capitalize()} :- {information[i+1]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=1,ipadx=50,padx=20,pady=20)
            
        else:
            tk.Label(frame1i, text=f'{heading[4].capitalize()} :- {information[4]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=0,ipadx=50,padx=20,pady=20)
    tk.Button(frame1,text='Change My Password',font=('Rockwell', 18, 'italic'),bg='black',fg='cyan',relief='groove',command=lambda:change_password('student',ids)).pack(side = 'bottom',pady=20)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Timetable Show<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame2 = tk.Frame(root,bg='blue')
    frame2.pack(fill='both',expand=1)
    
    cur_obj.execute(f"select*from classes where class='{'class'+information[3]}' ")
    
    info_of_all = cur_obj.fetchall()[0][1:]
    l_side=['PERIOD',1,2,3,4,5,6,7,8]
    list_of_headings = ['MONDAY', 'TUESDAY','WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
    f2=tk.Frame(frame2,bg='blue')
    f2.pack(side='left')  
    frame2i = tk.Frame(frame2,bg='blue')
    frame2i.pack(pady=25,side='left')
    tk.Label(frame2,text='\n\n'.join(['C','L','A','S','S','\u2193']+[i for i in cls]), font=('Calibri', 20, 'italic'), width=14,bg='black', fg='cyan',relief='groove',bd=5).pack(side='left',pady=32,fill='y')
    for i in range(9):
       tk.Label(f2,text=l_side[i], font=('Calibri', 17, 'italic'), width=14, height=2, bg='black', fg='cyan',relief='groove',bd=5).grid(row=i, column=0)
   
    for i in range(len(list_of_headings)):
        tk.Label(frame2i, text=list_of_headings[i], font=('Calibri', 17, 'italic'), width=14, height=2, bg='black', fg='cyan',relief='groove',bd=5).grid(row=0, column=i,)

    def decode(x):
        for i in range(len(x)):
            if x[i] =='_': break
        idt = x[i+1:]
        mycur.execute(f"select subject from teacher where school_id ='{idt}'")
        try : return (mycur.fetchall()[0][0]).capitalize()
        except IndexError : return x
    

    k = 0
    i = 0
    for j in range(len(info_of_all)):
        i+=1
        if info_of_all[j] != None:
            tk.Label(frame2i, text=decode(info_of_all[j]), font=('Calibri', 17, 'italic'), width=14, height=2, bg='black', fg='cyan',relief='groove',bd=5).grid(row=i, column=k)
        else:
            tk.Label(frame2i, text=info_of_all[j], font=('Calibri', 17, 'italic'), width=14, height=2, bg='black', fg='cyan',relief='groove',bd=5).grid(row=i, column=k)
        if (j+1)%8==0 and j!=0:
            i = 0
            k += 1

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    root.add(frame1,text = '                   INFORMATION                 ')        
    root.add(frame2,text = '                    TIMETABLE                  ')
    
    mainwin.mainloop()

def logged_adm():
    mainwin = tk.Tk()
    mainwin.geometry(f'{mainwin.winfo_screenwidth()}x{mainwin.winfo_screenheight()}+0+0')
    mainwin.title('LOGGED IN')
    
    root = Notebook(mainwin)
    root.pack(expand=1,fill='both')

    con_obj = connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info, charset='utf8')
    cur_obj = con_obj.cursor()
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>INFO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame1 = tk.Frame(root,bg='blue')
    frame1.pack(fill='both',expand=1)
    frame1i = tk.Frame(frame1,bg='blue')
    frame1i.pack(pady = 50)
    cur_obj.execute('select*from admins')
    
    information = cur_obj.fetchall()[0]
    information = information[:3] + information[4:]
    
    heading = ['Name','email_id','phone_number','school_id','admin_id']
    for i in range(0,len(information),2):
        if i!= 4:
            tk.Label(frame1i, text=f'{heading[i].capitalize()} :- {information[i]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=0,ipadx=50,padx=20,pady=20)
            tk.Label(frame1i, text=f'{heading[i+1].capitalize()} :- {information[i+1]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=1,ipadx=50,padx=20,pady=20)
        else:
            tk.Label(frame1i, text=f'{heading[4].capitalize()} :- {information[4]}', font=('Rockwell', 18, 'italic'), width=30, height=2, bg='black', fg='cyan',relief='groove',bd=25).grid(row=i//2,column=0,ipadx=50,padx=20,pady=20)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD STUDENTS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#      
    frame2 = tk.Frame(root,bg='blue')
    frame2.pack(fill='both',expand=1)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD TEACHERS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame3 = tk.Frame(root,bg='blue')
    frame3.pack(fill='both',expand=1)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>REMOVE STUDENTS<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame4 = tk.Frame(root,bg='blue')
    frame4.pack(expand=1,fill='both')
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>REMOVE TEACHERS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame5 = tk.Frame(root,bg='blue')
    frame5.pack(expand=1,fill='both')
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EDIT TIMETABLES<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    frame6 = tk.Frame(root,bg='blue')
    frame6.pack(expand=1,fill='both')
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
    root.add(frame1,text = '                      INFORMATION                      ')
    root.add(frame2,text = '                     ADD STUDENTS                     ')
    root.add(frame3,text = '                     ADD TEACHERS                     ')
    root.add(frame4,text = '                  REMOVE STUDENTS                 ')
    root.add(frame5,text = '                  REMOVE TEACHERS                  ')
    root.add(frame6,text = '                   EDIT TIMETABLES                      ')
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Calling functions after adding<<<<<<<<<<<<<<<<<<<<<<<<<#
    Add.Students(frame2) ,Add.Teachers(frame3)
    Add.Remove_S(frame4), Add.Remove_T(frame5)
    Time_Table.Edit(frame6)

