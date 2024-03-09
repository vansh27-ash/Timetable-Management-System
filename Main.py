''' T i m e - T a b l e   M a n a g e m e n t '''

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Notebook
import Homepage as Hm
from installer_file import install
import _info_
if  _info_.database_info != '' and _info_.database_info_T !='' and _info_.database_info_S !='' :

    '''----------------------------------------------------------------------------- D I F F E R E N T  L O G I N S -----------------------------------------------------------------------------------'''

        
    def login_as_student(win, position):
        Hm.Home(win, position)

    def login_as_teacher(win, position):
        Hm.Home(win, position)
        
    def login_as_admin(win, position):
        Hm.Home(win, position)
        

    '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'''


    mainwin = tk.Tk()
    mainwin.title(' T i m e - T a b l e   M a n a g e m e n t ')
    mainwin.geometry(f'{mainwin.winfo_screenwidth()}x{mainwin.winfo_screenheight()}+0+0')
    mainwin.config(background='dark orange')
    icon = tk.PhotoImage(file = 'icon.png')
    mainwin.iconphoto(1,icon)
    img1 = ((tk.PhotoImage(file='stu.png')).zoom(1)).subsample(5)
    img2 = ((tk.PhotoImage(file='tea.png')).zoom(1)).subsample(4)
    img3 = ((tk.PhotoImage(file='adm.png')).zoom(1)).subsample(4)  

    tk.Label(mainwin,text='TimeTable Management',font=('Rockwell',55,('underline','italic')),bg='black',fg='white',relief='ridge').pack(fill='x')
    tk.Label(mainwin,text='LOGIN AS',font=('Rockwell',40,('underline','italic')),bg='black',fg='white',relief='ridge').pack(pady=50,fill='x')

    area = tk.Frame(mainwin,bg='dark orange') 

    tk.Label(area,image=img1,font=('Rockwell',120,'bold'),width=170,bg='dark orange',fg='white',borderwidth=0,relief='groove').pack(padx=100,side='left')
    tk.Label(area,image=img2,font=('Rockwell',120,'bold'),width=170,bg='dark orange',fg='white',borderwidth=0,relief='groove').pack(padx=100,side='left')
    tk.Label(area,image=img3,font=('Rockwell',120,'bold'),width=170,bg='dark orange',fg='white',borderwidth=0,relief='groove').pack(padx=100,side='left')


    area.pack(fill='x',padx=85)
    sub_area = tk.Frame(mainwin,bg='dark orange')

    las = tk.Button(sub_area,text='Student',font=('Rockwell',30,('underline','italic')),bg='black',fg='white',relief='groove',command=lambda:login_as_student(mainwin, 'Student'))
    las.pack(side='left',padx=(100,75))

    lat = tk.Button(sub_area,text='Teacher',font=('Rockwell',30,('underline','italic')),bg='black',fg='white',relief='groove',command=lambda:login_as_teacher(mainwin, 'Teacher'))
    lat.pack(side='left',padx=120)

    laa = tk.Button(sub_area,text='Admin',font=('Rockwell',30,('underline','italic')),bg='black',fg='white',relief='groove',command=lambda:login_as_admin(mainwin, 'admin'))
    laa.pack(side='left',padx=75,ipadx=10)


    sub_area.pack(fill='x',padx=80,pady=10)

    '''--------------------------------------------------------------------------------Other Bindings--------------------------------------------------------------'''

    las.bind('<Enter>', lambda x : las.config(background='blue'))
    las.bind('<Leave>',lambda x : las.config(background='black'))
    lat.bind('<Enter>', lambda x : lat.config(background='blue'))
    lat.bind('<Leave>',lambda x : lat.config(background='black'))
    laa.bind('<Enter>', lambda x : laa.config(background='blue'))
    laa.bind('<Leave>',lambda x : laa.config(background='black'))


    mainwin.mainloop()
else :
    install()
