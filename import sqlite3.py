import sqlite3
from tkinter import *
from tkinter import messagebox
import subprocess

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def open_mainpage():
    name = name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    with open("users.txt", "a") as f:
        f.write(f"{name}:{username}:{password}\n")

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", 
                       (name, username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Account created successfully")
        root.destroy()
        subprocess.run(["python", "mainpage.py"])
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def open_login():
    root.destroy()
    subprocess.run(["python", "login.py"])

setup_database()

root = Tk()
root.title("Sign Up")
root.attributes('-fullscreen', True)
root.iconbitmap('carr.ico')

label_font = ("Helvetica", 14, "bold")
entry_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")
button_bg = "#ffffff"
button_fg = "#000000"
label_fg = "#000000"
entry_bg = "#ffffff"
entry_fg = "#000000"

orange_color = "#ffb12d"

root.configure(bg=orange_color)

form_frame = Frame(root, bg=orange_color)
form_frame.place(relx=0.01, rely=0.01)

Label(form_frame, text="Name:", font=label_font, fg=label_fg, bg=orange_color).grid(row=0, column=0, padx=5, pady=4, sticky='e')
name_entry = Entry(form_frame, font=entry_font, bg=entry_bg, fg=entry_fg)
name_entry.grid(row=0, column=1, padx=10, pady=4, sticky='w')

Label(form_frame, text="Username:", font=label_font, fg=label_fg, bg=orange_color).grid(row=2, column=0, padx=5, pady=4, sticky='e')
username_entry = Entry(form_frame, font=entry_font, bg=entry_bg, fg=entry_fg)
username_entry.grid(row=2, column=1, padx=10, pady=4, sticky='w')

Label(form_frame, text="Password:", font=label_font, fg=label_fg, bg=orange_color).grid(row=3, column=0, padx=5, pady=4, sticky='e')
password_entry = Entry(form_frame, show="*", font=entry_font, bg=entry_bg, fg=entry_fg)
password_entry.grid(row=3, column=1, padx=10, pady=4, sticky='w')

Label(form_frame, text="Confirm Password:", font=label_font, fg=label_fg, bg=orange_color).grid(row=4, column=0, padx=5, pady=4, sticky='e')
confirm_password_entry = Entry(form_frame, show="*", font=entry_font, bg=entry_bg, fg=entry_fg)
confirm_password_entry.grid(row=4, column=1, padx=10, pady=4, sticky='w')

register_button = Button(root, text="Sign Up", font=button_font, height=2, width=7, command=open_mainpage, bg=button_bg, fg=button_fg)
register_button.place(relx=0.26, rely=0.22, anchor='nw')

Label(root, text="Already signed in?", font=("Helvetica", 12), fg=label_fg, bg=orange_color).place(relx=0.33, rely=0.01, anchor='nw')

login_button = Button(root, text="Login", font=button_font, height=1, width=5, command=open_login, bg=button_bg, fg=button_fg)
login_button.place(relx=0.33, rely=0.05, anchor='nw')

exit_button = Button(root, text="Exit", font=button_font, height=2, width=6, command=root.destroy, bg=button_bg, fg=button_fg)
exit_button.place(relx=0.92, rely=0.90)

root.mainloop()