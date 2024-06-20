import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import messagebox
import subprocess

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def open_mainpage():
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    email = email_entry.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                       (username, password, email))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Account created successfully")
        root.destroy()
        subprocess.run(["python", "mainpage.py"])
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def check_login():
    username = entry_login_username.get()
    password = entry_login_password.get()

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful")
            root.destroy()
            subprocess.run(["python", "mainpage.py"])
        else:
            messagebox.showerror("Error", "Invalid username or password")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

setup_database()

def main():
    global root, username_entry, password_entry, confirm_password_entry, email_entry, entry_login_username, entry_login_password

    root = tk.Tk()
    root.title("Sign-Up and Log-In Page")
    root.attributes('-fullscreen', True)

    frame_signup = tk.Frame(root, padx=20, pady=20, bg="lightblue")
    frame_login = tk.Frame(root, padx=20, pady=20, bg="lightgreen")
    frame_signup.pack(side="left", expand=True, fill="both")
    frame_login.pack(side="right", expand=True, fill="both")

    tk.Label(frame_signup, text="Sign Up", font=("Arial", 20), bg="lightblue").pack(pady=10)
    
    tk.Label(frame_signup, text="Username:",  font=("Arial", 14),bg="lightblue").pack(anchor="w")
    username_entry = tk.Entry(frame_signup, width=15)
    username_entry.pack(fill="x", pady=2)
    
    tk.Label(frame_signup, text="Password:",  font=("Arial", 14),bg="lightblue").pack(anchor="w")
    password_entry = tk.Entry(frame_signup, width=15, show="*")
    password_entry.pack(fill="x", pady=2)
    
    tk.Label(frame_signup, text="Confirm Password:",  font=("Arial", 14),bg="lightblue").pack(anchor="w")
    confirm_password_entry = tk.Entry(frame_signup, width=18, show="*")
    confirm_password_entry.pack(fill="x", pady=2)
        
    tk.Label(frame_signup, text="Email:",  font=("Arial", 14),bg="lightblue").pack(anchor="w")
    email_entry = tk.Entry(frame_signup, width=18)
    email_entry.pack(fill="x", pady=2)

    tk.Button(frame_signup, font=(12), text="Sign Up", command=open_mainpage).pack(pady=20)

    tk.Label(frame_login, text="Log In", font=("Arial", 20), bg="lightgreen").pack(pady=10)
    
    tk.Label(frame_login, text="Username:",  font=("Arial", 14),bg="lightgreen").pack(anchor="w")
    entry_login_username = tk.Entry(frame_login, width=15)
    entry_login_username.pack(fill="x", pady=2)
    
    tk.Label(frame_login, text="Password:",  font=("Arial", 14),bg="lightgreen").pack(anchor="w")
    entry_login_password = tk.Entry(frame_login, width=15, show="*")
    entry_login_password.pack(fill="x", pady=2)

    tk.Button(frame_login, font=(12), text="Log In", command=check_login).pack(pady=20)

    exit_button = tk.Button(root, text="Exit", width= 4, height=1, command=root.quit, font=("Arial", 14), bg="white", fg="black")
    exit_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    root.mainloop()

if __name__ == "__main__":
    main()