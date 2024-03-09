from mysql.connector import connect
from tkinter.messagebox import showinfo,showerror,showwarning

def newone(x,y,z): 
    try:
        connobj = connect(host='localhost',user='root',passwd=x,database=y, charset='utf8')
    except:
        showerror('Error','An unexpected error occured')
    if not connobj.is_connected() :
        showwarning('Warning','Unable to connect to mysql')
    else:
        curobj = connobj.cursor()
        curobj.execute(f"insert into timetable (tablename) values('{z}')")
        connobj.commit()
        connobj.close()
