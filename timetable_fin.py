import tkinter as tk
from tkinter.ttk import Combobox, Spinbox
from tkinter.messagebox import showwarning, showinfo
from mysql.connector import connect
from functools import partial
import _info_
rec_of_tables=[]
column_dict = {1: ('mon',(1,8)), 2: ('tue',(9,16)) ,3: ('wed',(17,24)),4: ('thurs',(25,32)), 5: ('fri',(33,40)), 6: ('sat',(41,48))}
def form_matrix(l):
    l1,l2=[1],[2]
    l3,l4=[3],[4]
    l5,l6=[5],[6]
    l7,l8=[7],[8]
    for i in range(0,41,8):
        l1.append(l[i]),l2.append(l[i+1])
        l3.append(l[i+2]),l4.append(l[i+3])
        l5.append(l[i+4]),l6.append(l[i+5])
        l7.append(l[i+6]),l8.append(l[i+7])
    return [l1,l2,l3,l4,l5,l6,l7,l8]

def M(win):
    def ask(x, unique):
        def done(column):
            for i in range(8):
                if globals()['cv'+str(i+1)].get() != 'Free':
                    mycur.execute(f"select * from classes where class = 'class{globals()['cv'+str(i+1)].get()}'")
                    data = mycur.fetchall()[0]
                    data=data[(column_dict[column][1][0]):(column_dict[column][1][1]+1)]
                    if data[i]==unique or data[i]==None:
                        query = f"update timetable set {column_dict[column][0]+str(i+1)}='{globals()['cv'+str(i+1)].get()}' where tablename='{unique}'"
                        query2 = f"update classes  set {column_dict[column][0]+str(i+1)}='{unique}' where class = 'class{globals()['cv'+str(i+1)].get()}'"
                        mycur.execute(query2)
                        cur_obj.execute(query)
                    else:
                        msg = f"The teacher with id = {data[i]} has class at that time in class{globals()['cv'+str(i+1)].get()}.\n So the change for that is not made.\nTherfore in order to make changes first change the class to free for that teacher"
                        showwarning('CLASH',msg)
                else:
                    query = f"update timetable set {column_dict[column][0]+str(i+1)}=null where tablename = '{unique}'"
                    if info2[i]!=None:
                        query2 = f"update classes set {column_dict[column][0]+str(i+1)}=null where class = '{info2[i]}'"
                        mycur.execute(query2)
                        cur_obj.execute(query)
                mycon.commit()
                con_obj.commit()
            confirm_win.destroy()
            refresh(unique)
        column = x.grid_info()['column']
        cur_obj.execute(f'select *  from timetable where tablename="{unique}"')
        info = cur_obj.fetchall()
        if  info:
            info = info[0]
        else:
            info = [None for i in range(48)]
        info2 = info[(column_dict[column][1][0]):(column_dict[column][1][1]+1)]
        
        confirm_win = tk.Toplevel(time_win)
        confirm_win.title(column_dict[column][0])
        confirm_win.geometry('400x300+100+100'), confirm_win.resizable(0, 0)
        confirm_win.config(background='black')
        
        classvalues = ['Free']
        for i in range(1,_info_.Classes+1):
            classvalues.append(str(i)+'A')
            classvalues.append(str(i)+'B')
            
        for i in range(len(info2)):
            globals()['cv'+str(i+1)] = tk.StringVar()
            tk.Label(confirm_win,text=f'{i+1}'+' period',font=('Calibri', 15, 'italic'),bg='black',fg='cyan').grid(row=i,padx=10)
            globals()['c'+str(i+1)] = Combobox(confirm_win, font=('Calibri', 15, 'italic'), textvariable = globals()['cv'+str(i+1)],values = classvalues, state='readonly')
            globals()['c'+str(i+1)].grid(row=i,column=1,padx=20)
            if info2[i]==None:
                globals()['c' + str(i+1)].current(0)
            else:
                globals()['c' + str(i+1)].current(classvalues.index(str(info2[i])))
            
        tk.Button(confirm_win, text='Confirm', font=('Calibri', 12, 'italic'),width=14, height=2, bg='black', fg='cyan', command=lambda:done(column)).grid(row=9,column=0,columnspan=2)
        
        confirm_win.mainloop()

    def refresh(unique):
        cur_obj.execute(f'select*from timetable where tablename="{unique}"')
        info = cur_obj.fetchall()
        if list(info)==[]:
            info_of_all = [None for i in range(48)]
        else:
            info_of_all = info[0][1:]
        info_of_all = form_matrix(info_of_all)
        list_of_headings = ['PERIOD NUMBER', 'MONDAY', 'TUESDAY','WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
        for i in range(len(list_of_headings)):
            tk.Button(timetable_show, text=list_of_headings[i], font=('Calibri', 12, 'italic'), width=14, height=2, bg='black', fg='cyan').grid(row=0, column=i)
            
        for i in range(len(info_of_all)):
            for j in range(len(info_of_all[i])):
                tk.Button(timetable_show, text=info_of_all[i][j], font=('Calibri', 12, 'italic'), width=14, height=2, bg='black', fg='cyan').grid(row=i+1, column=j)
        tk.Button(timetable_show, text='Click', font=('Calibri', 12, 'italic'),width=14, height=2, bg='black', fg='cyan').grid(row=9, column=0)
        
        for k in range(6):
            obj = tk.Button(timetable_show, text='Enter/update data', font=('Calibri', 12, 'italic'), width=14, height=2, bg='black', fg='cyan')
            obj.grid(row=9, column=k+1)
            obj.config(command=partial(ask, obj, unique))
    
    con_obj = connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_T, charset='utf8')
    mycon = connect(host='localhost', user='root', passwd=_info_.password, database=_info_.database_info_S, charset='utf8')
    mycur = mycon.cursor()
    cur_obj = con_obj.cursor()
    
    cur_obj.execute('select tablename from timetable')
    time_win = tk.LabelFrame(win,bg='black',relief='ridge',bd=25)
    time_win.pack(pady=20)
    
    Sc_ID = [names[0] for names in (cur_obj.fetchall())]
    if Sc_ID == []:
        tk.Label(time_win,text='Nothing to show first add teachers',font=('Rockwell', 16, 'italic'), fg='white', bg='black').grid(pady=50, padx=50)
        tk.Label(time_win,text='Note:-Please login again if you added your first teacher recently',font=('Rockwell', 16, 'italic'), fg='white', bg='black').grid(row=1,pady=50, padx=50)
        return
    else:
        rec_of_tables.extend(Sc_ID)
        unique = Sc_ID[0]

    timetable_show = tk.Frame(time_win)
    refresh(unique)
    timetable_show.pack(side='left', pady=10, padx=40)
    def refresh_values():
        availiable = rec_of_tables
        if availiable == []:
            for i in list(time_win.children.values()):
                i.destroy()
            tk.Label(time_win,text='Nothing to show first add teachers',font=('Rockwell', 16, 'italic'), fg='white', bg='black').grid(pady=50, padx=50)
            tk.Label(time_win,text='Note:-Please login again if you added your first teacher recently',font=('Rockwell', 16, 'italic'), fg='white', bg='black').grid(row=1,pady=50, padx=50)
        else:
            tochoose.config(values=availiable)
            tochoose.current(0)
            Show()
    def Show():
        global unique
        unique = tea_selected.get()
        refresh(unique)
        
    tea_show = tk.Frame(time_win, bg='blue')
    tk.Label(tea_show, text='SELECT TEACHER School ID', font=('Rockwell', 16, 'italic'), fg='white', bg='black').pack(pady=5, padx=5)
    tk.Label(tea_show, text='His/Her name_ is added in front of id', font=('Rockwell', 16, 'italic'), fg='white', bg='black').pack(pady=5, padx=5)
    tea_selected = tk.StringVar()
    availiable = Sc_ID 
    tochoose = Combobox(tea_show, textvariable=tea_selected, font=('Arial', 18, 'italic'), values=availiable, state='readonly')
    tochoose.current(0), tochoose.pack(pady=5, padx=5)
    
    tk.Button(tea_show, text='SHOW', font=('Rockwell', 18, 'italic'),fg='white', bg='black', command=Show).pack(pady=10, padx=5)
    tk.Button(tea_show, text='REFRESH', font=('Rockwell', 18, 'italic'),fg='white', bg='black', command=refresh_values).pack(pady=10, padx=5)
    tea_show.pack(side='left', pady=100, padx=10)

