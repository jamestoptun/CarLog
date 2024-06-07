import sqlite3
from tkinter import *
from tkinter import messagebox
import subprocess

def Ok():
    uname = e1.get()
    password = e2.get()
    
    if uname == "" or password == "":
        messagebox.showinfo("", "Blank Not allowed")
        return
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, password))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        messagebox.showinfo("", "Login Success")
        root.destroy()
        subprocess.run(["python", "mainpage.py"])
    else:
        messagebox.showinfo("", "Incorrect Username/Password")

root = Tk()
root.title("Login")
root.geometry("400x300")
root.iconbitmap('carr.ico')

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(9, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(3, weight=1)

name_label = Label(root, text="Username:", font=("Helvetica", 12, "bold"))
name_label.grid(row=1, column=1, padx=7, pady=1, sticky='e')
e1 = Entry(root)
e1.grid(row=1, column=2, padx=7, pady=7, sticky='w')

password_label = Label(root, text="Password:", font=("Helvetica", 12, "bold"))
password_label.grid(row=2, column=1, padx=7, pady=1, sticky='e')
e2 = Entry(root, show="*")
e2.grid(row=2, column=2, padx=7, pady=7, sticky='w')

login_button = Button(root, text="Login", font=("bold", 12), command=Ok)
login_button.grid(row=3, column=1, columnspan=2, pady=10)

root.mainloop()
