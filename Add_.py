from tkinter import *
from tkinter.ttk import Combobox, Spinbox
from timetable_fin import *
import hashlib
from use_for_teacher import *
import _info_
import mysql.connector as mysql
from functools import partial
from tkinter.messagebox import askyesno, showinfo
from threading import Thread
from tkinter import scrolledtext

rec_T = []
rec_S = []

def Id_create(*argvs):
    S = ''
    for val in argvs:
        S += val
    S = S.encode()
    return f"{_info_.School_name[:2]}_{(hashlib.sha256(S)).hexdigest()[0:5]}{argvs[0][0:2]}" 

def Secure(Password):
        '''create a hash value for  input password
        which is to be compaired with the hashvalue of the user password(which the user gave durig signup) ,stored in db
        and hashvalue is of no use it is just for comparison and its quality is its unique for a given input
        '''    
        return hashlib.sha256(Password.encode()).hexdigest()

class Add:
    @staticmethod
    def Students(win):
        global refresh_S
        root = LabelFrame(win,text='ADD STUDENTS HERE',font=('Rockwell',30,'italic'),width=40,fg='white',bg='black',relief='ridge',bd=25)
        root.pack(pady=50)
        var1 = StringVar()
        var2 = StringVar()
        var3 = StringVar()
        var4 = StringVar()
        
        
        Frame = LabelFrame(root, borderwidth=4, bg='blue', width=50,padx=30, pady=30)
        Frame.grid(row=0, column=0, rowspan=5, columnspan=5, padx=100, pady=30)

        l1 = Label(Frame, text='Student Name', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        l2 = Label(Frame, text='Class', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        l3 = Label(Frame, text='Email Id', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        l4 = Label(Frame, text='Phone Number', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        
        l1.grid(row=0, column=0, sticky=W+E, padx=20, pady=5)
        l2.grid(row=1, column=0, sticky=W+E, padx=20, pady=5)
        l3.grid(row=2, column=0, sticky=W+E, padx=20, pady=5)
        l4.grid(row=3, column=0, sticky=W+E, padx=20, pady=5)
        

        e1 = Entry(Frame, textvariable=var1, borderwidth=4, relief=SUNKEN, font=('helvetica', 20), fg='grey')
        e2 = Entry(Frame, textvariable=var3, borderwidth=4, relief=SUNKEN, font=('helvetica', 20), fg='grey')
        e4 = Entry(Frame, textvariable=var4, borderwidth=4, relief=SUNKEN, font=('helvetica', 20), fg='grey')
        available = ()
        for  i in range(1,_info_.Classes+1):
            available += (f'{i}A',)
            available += (f'{i}B',)
        box = Combobox(Frame, textvariable=var2, values=available, font=('helvetica',20), state='readonly')
        
        
        

        e1.grid(row=0, column=1, padx=20, pady=5)

        box.grid(row=1, column=1, pady=5, padx=20)
        box.current(0)
        
        e2.grid(row=2, column=1, padx=20, pady=5)
        e4.grid(row=3, column=1, padx=20, pady=5)
        

        e1.insert(0,'Enter the Student name')
        e2.insert(0,'Enter the Email Id')
        e4.insert(0,'Enter the Phone Number')

        e1.bind('<Button-1>', lambda event: e1.delete(0,END))
        e2.bind('<Button-1>', lambda event: e2.delete(0,END))
       
        e4.bind('<Button-1>', lambda event: e4.delete(0,END))
       

        def Show(*argvs):
            show_win = Tk()
            show_win.title("Added"),show_win.resizable(0,0)
            n, cls, Id, ph = argvs
            frame2 = LabelFrame(show_win, borderwidth=4 , bg='blue', padx=30, pady=30)
            frame2.grid(row=6, column=0, rowspan=5, columnspan=5)

            Sc_ID = Id_create(n.get(), Id.get(), ph.get(), cls.get())

            Label(frame2, text=f'Student Name:- {n.get()}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=0, column=0, sticky=W+E, padx=20, pady=5)
            Label(frame2, text=f'Email ID:- {Id.get()}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=1, column=0, sticky=W+E, padx=20, pady=5)
            Label(frame2, text=f'Phone Number:- {ph.get()}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=2, column=0, sticky=W+E, padx=20, pady=5)
            Label(frame2, text=f'School_Id:- {Sc_ID}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=3, column=0, sticky=W+E, padx=20, pady=5)
            Button(frame2,text='Done', font=('helvetica', 15), relief=GROOVE, fg='white',bg='black',command= lambda:show_win.destroy()).grid(row=4,column=0,sticky=W+E,padx=20,pady=5)
          
            db = mysql.connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_S, charset='utf8')
            cursor = db.cursor()
            
            query = f"insert into student value('{n.get()}','{Id.get()}','{ph.get()}','{cls.get()}','{Secure('')}','{Sc_ID}')"
            
            cursor.execute(query)

            db.commit()
            rec_S.append(' -- '.join([n.get(),Id.get(),ph.get(),cls.get(),Sc_ID]))
            

            refresh_S()
            var1.set('')
            var2.set('')
            var3.set('')
            var4.set('')

            e1.insert(0,'Enter the Student name')
            e2.insert(0,'Enter the Email Id')
            e4.insert(0,'Enter the Phone Number')
            box.current(0)
            show_win.mainloop()
            


        b1 = Button(Frame, text='Add', bg='red', command=lambda: Show(var1, var2, var3, var4), padx=30, font=('helvetica', 20))
        b1.grid(row=4, column=2, padx=20, pady=5)

    @staticmethod
    def Teachers(win):
        global refresh_T
        root = LabelFrame(win,text='ADD TEACHERS HERE',font=('Rockwell',30,'italic'),width=40,fg='white',bg='black',relief='ridge',bd=25)
        root.pack(pady=50)

        var1 = StringVar()
        var2 = StringVar()
        var3 = StringVar()
        var4 = StringVar()
        
        Frame = LabelFrame(root, borderwidth=4, bg='blue',width=50, padx=30, pady=30)
        Frame.grid(row=0, column=0, rowspan=5, columnspan=5, padx=100, pady=30)

        l1 = Label(Frame, text='Teacher Name', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        l2 = Label(Frame, text='Subject', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        l3 = Label(Frame, text='Email Id', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        l4 = Label(Frame, text='Phone Number', font=('helvetica', 20), relief=RAISED, anchor=W, bg='magenta')
        
        

        l1.grid(row=0, column=0, sticky=W+E, padx=20, pady=5)
        l2.grid(row=1, column=0, sticky=W+E, padx=20, pady=5)
        l3.grid(row=2, column=0, sticky=W+E, padx=20, pady=5)
        l4.grid(row=3, column=0, sticky=W+E, padx=20, pady=5)
        

        e1 = Entry(Frame, textvariable=var1, borderwidth=4, relief=SUNKEN, font=('helvetica', 20), fg='grey')
        e2 = Entry(Frame, textvariable=var2, borderwidth=4, relief=SUNKEN, font=('helvetica', 20), fg='grey')
        e3 = Entry(Frame, textvariable=var3, borderwidth=4, relief=SUNKEN, font=('helvetica', 20), fg='grey')
        e4 = Entry(Frame, textvariable=var4, borderwidth=4, relief=SUNKEN, font=('helvetica', 20), fg='grey')
        

        e1.grid(row=0, column=1, padx=20, pady=5)
        e2.grid(row=1, column=1, padx=20, pady=5)
        e3.grid(row=2, column=1, padx=20, pady=5)
        e4.grid(row=3, column=1, padx=20, pady=5)
        

        e1.insert(0,'Enter the teacher name')
        e2.insert(0,'Enter the Subject')
        e3.insert(0,'Enter the Email Id')
        e4.insert(0,'Enter the Phone Number')
        
        e1.bind('<Button-1>', lambda event: e1.delete(0,END))
        e2.bind('<Button-1>', lambda event: e2.delete(0,END))
        e3.bind('<Button-1>', lambda event: e3.delete(0,END))
        e4.bind('<Button-1>', lambda event: e4.delete(0,END))
        
        


        def Show(*argvs):
            global Sc_ID
            show_win = Tk()
            show_win.title("Added"),show_win.resizable(0,0)
            n, sub, Id, ph = argvs
            frame2 = LabelFrame(show_win, borderwidth=4 , bg='blue', padx=30, pady=30)
            frame2.grid(row=6, column=0, rowspan=5, columnspan=5)

            Sc_ID = Id_create(n.get(), sub.get(), Id.get(), ph.get())

            Label(frame2, text=f'Teacher Name:- {n.get()}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=0, column=0, sticky=W+E, padx=20, pady=5)
            Label(frame2, text=f'Subjects:- {sub.get()}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=1, column=0, sticky=W+E, padx=20, pady=5)
            Label(frame2, text=f'Email ID:- {Id.get()}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=2, column=0, sticky=W+E, padx=20, pady=5)
            Label(frame2, text=f'Phone Number:- {ph.get()}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=3, column=0, sticky=W+E, padx=20, pady=5)
            Label(frame2, text=f'School_Id:- {Sc_ID}' , font=('helvetica', 15), relief=RAISED, anchor=W, bg='magenta').grid(row=4, column=0, sticky=W+E, padx=20, pady=5)
            Button(frame2,text='Done', font=('helvetica', 15), relief=GROOVE, fg='white',bg='black',command= lambda:show_win.destroy()).grid(row=4,column=0,sticky=W+E,padx=20,pady=5)

            db = mysql.connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_T, charset='utf8')
            cursor = db.cursor()
            
            query = f"insert into teacher value('{n.get()}','{Id.get()}','{ph.get()}','{Secure('')}','{Sc_ID}','{sub.get()}')"
            
            cursor.execute(query)
            db.commit()
            rec_T.append(' -- '.join([n.get(),Id.get(),ph.get(),Sc_ID,sub.get()]))
            rec_of_tables.append(n.get()+'_'+Sc_ID)
            refresh_T()
            Thread(target=newone,args=(_info_.password, _info_.database_info_T, n.get()+'_'+Sc_ID)).start()
            var1.set('')
            var2.set('')
            var3.set('')
            var4.set('')

            e1.insert(0,'Enter the teacher name')
            e2.insert(0,'Enter the Subject')
            e3.insert(0,'Enter the Email Id')
            e4.insert(0,'Enter the Phone Number')


        b1 = Button(Frame, text='Add', bg='red', command=lambda: Show(var1, var2, var3, var4), padx=30, font=('helvetica', 20))
        b1.grid(row=4, column=2, padx=20, pady=5)

      
    @staticmethod
    def Remove_S(win):
        global refresh_S
        root = LabelFrame(win,text='REMOVE STUDENTS HERE',font=('Rockwell',30,'italic'),fg='white',bg='black',relief='ridge',bd=25)
        root.grid(padx=100,pady=50)
        db_S = mysql.connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_S, charset='utf8')
        cursor_S = db_S.cursor()                
        cursor_S.execute('select * from student')
        rec = cursor_S.fetchall()
        for i in range(len(rec)):
            toShow = rec[i][:4] + rec[i][5:]
            rec_S.append(' -- '.join(toShow))

        frame_S = LabelFrame(root, text='Student\'s Record', bd=3, bg='blue',width=40, font=('helvetica', 15), fg='white')
        frame_S.grid(row=0, column=0, padx=100, pady=30, columnspan=4, rowspan=5)
        Label(frame_S, text= ' -- '.join(['Name','Email Id','Phone Number','Class','School id']), font=('helvetica', 15), width=80,anchor=W, justify='center').grid(row=0, column=0,columnspan=2, padx=10, pady=15, sticky=W+E)
        
        def refresh_S():
            for i in list(frame_S.children.values())[1:]:
                i.destroy()
            frame_of_info_S = Frame(frame_S)
            frame_of_info_S.grid(row=1,column=0,columnspan=2,padx=10,pady=15,ipadx=10)

            globals()['list_of_info_S'] = Listbox(frame_of_info_S,font=('helvetica', 15),height=3,width=80,justify='center',selectmode='single',selectbackground='red')
            list_of_info_S.pack(side='left')
            scroll = Scrollbar(frame_of_info_S,orient='vertical',command=list_of_info_S.yview)
            scroll.pack(side='right',fill='y'),list_of_info_S.config(yscrollcommand=scroll.set)
            for i in range(len(rec_S)):
                list_of_info_S.insert(i,rec_S[i])
            Button(frame_S,text="REMOVE STUDENT",font=('Helvetica',20,'bold'),fg='white',bg='black',bd=10,command=remove_S).grid(row=2,columnspan=3,padx=100,pady=10)

        def remove_S():
            selection = list_of_info_S.curselection()
            choosed = askyesno('Confirm',f"Are you sure you want to remove \n{rec_S[selection[0]]}")
                
            if choosed:
                data = rec_S[selection[0]].split(' -- ')
                query = f"delete from student where school_id='{data[-1]}'"
                rec_S.remove(' -- '.join(data))
                cursor_S.execute(query)
                db_S.commit()
                refresh_S()
        refresh_S()

    @staticmethod
    def Remove_T(win):
        global refresh_T
        root = LabelFrame(win,text='REMOVE TEACHERS HERE',font=('Rockwell',30,'italic'),fg='white',bg='black',relief='ridge',bd=25)
        root.grid(padx=100,pady=50)
        db_T = mysql.connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_T, charset='utf8')
        cursor_T = db_T.cursor()
        cursor_T.execute('select * from teacher')
        rec = cursor_T.fetchall()
        for i in range(len(rec)):
            toShow = rec[i][:3] + rec[i][4:]
            rec_T.append(' -- '.join(toShow))

        frame_T = LabelFrame(root, text=f'Teacher\'s Record', bd=3, bg='blue',width=40, font=('helvetica', 15), fg='white')
        frame_T.grid(row=0, column=0, padx=10, pady=30, columnspan=4, rowspan=5)
        Label(frame_T, text= ' -- '.join(['Name','Email Id','Phone Number','School id','Subject']), font=('helvetica', 15),width=80, anchor=W, justify='center').grid(row=0, column=0, columnspan=2,padx=10, pady=15, sticky=W+E)

        def refresh_T():
            for i in list(frame_T.children.values())[1:]:
                i.destroy()
            frame_of_info_T = Frame(frame_T)
            frame_of_info_T.grid(row=1,column=0,columnspan=2,padx=10,pady=15,ipadx=10)

            globals()['list_of_info_T'] = Listbox(frame_of_info_T,font=('helvetica', 15),height=3,width=80,justify='center',selectmode='single',selectbackground='red')
            list_of_info_T.pack(side='left')
            scroll = Scrollbar(frame_of_info_T,orient='vertical',command=list_of_info_T.yview)
            scroll.pack(side='right',fill='y'),list_of_info_T.config(yscrollcommand=scroll.set)
            for i in range(len(rec_T)):
                list_of_info_T.insert(i,rec_T[i])
            Button(frame_T,text="REMOVE TEACHER",font=('Helvetica',20,'bold'),fg='white',bg='black',bd=10,command=remove_T).grid(row=2,columnspan=3,padx=100,pady=10)
            
        
        def remove_T():
            selection = list_of_info_T.curselection()
            choosed = askyesno('Confirm',f"Are you sure you want to remove \n{rec_T[selection[0]]}")
            if choosed:
                data = rec_T[selection[0]].split(' -- ')
                query1 = f"delete from teacher where school_id='{data[-2]}' "
                query2 = "delete from timetable where tablename = '{}'".format('_'.join([data[0],data[-2]]))
                rec_of_tables.remove('_'.join([data[0],data[-2]]))
                rec_T.remove(' -- '.join(data))
                cursor_T.execute(query1)
                cursor_T.execute(query2)
                db_T.commit()
                refresh_T()
        refresh_T()        
        

class Time_Table:

    @staticmethod    
    def Edit(win):
        M(win)

