import tkinter as tk
import sqlite3
from tkinter import messagebox
import subprocess

def setup_database():
    conn = sqlite3.connect('carlog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            car_make TEXT NOT NULL,
            car_model TEXT NOT NULL,
            car_year TEXT NOT NULL,
            vin TEXT NOT NULL UNIQUE,
            license_plate TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logins (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
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

    if "@" not in email:
        messagebox.showerror("Error", "Invalid email address, no \"@\"")
        return

    try:
        conn = sqlite3.connect('carlog.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_logins (username, password, email) VALUES (?, ?, ?)", 
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
        conn = sqlite3.connect('carlog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_logins WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful")
            root.destroy()
            subprocess.run(["python", "carlog.py"])
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

    frame_signup.place(relx=0, rely=0, relwidth=0.5, relheight=1.0)
    frame_login.place(relx=0.5, rely=0, relwidth=0.5, relheight=1.0)

    tk.Label(frame_signup, text="Sign Up", font=("Arial", 20), bg="lightblue").place(relx=0.5, y=10, anchor="n")
    
    tk.Label(frame_signup, text="Username:", font=("Arial", 14), bg="lightblue").place(relx=0.5, y=60, anchor="n")
    username_entry = tk.Entry(frame_signup, width=35)
    username_entry.place(relx=0.5, y=90, anchor="n")
    
    tk.Label(frame_signup, text="Password:", font=("Arial", 14), bg="lightblue").place(relx=0.5, y=120, anchor="n")
    password_entry = tk.Entry(frame_signup, width=35, show="*")
    password_entry.place(relx=0.5, y=150, anchor="n")
    
    tk.Label(frame_signup, text="Confirm Password:", font=("Arial", 14), bg="lightblue").place(relx=0.5, y=180, anchor="n")
    confirm_password_entry = tk.Entry(frame_signup, width=35, show="*")
    confirm_password_entry.place(relx=0.5, y=210, anchor="n")
        
    tk.Label(frame_signup, text="Email:", font=("Arial", 14), bg="lightblue").place(relx=0.5, y=240, anchor="n")
    email_entry = tk.Entry(frame_signup, width=35)
    email_entry.place(relx=0.5, y=270, anchor="n")

    tk.Button(frame_signup, font=("Arial", 12, "bold"), text="Sign Up", command=open_mainpage).place(relx=0.5, y=310, anchor="n")

    tk.Label(frame_login, text="Log In", font=("Arial", 20), bg="lightgreen").place(relx=0.5, y=10, anchor="n")
    
    tk.Label(frame_login, text="Username:", font=("Arial", 14), bg="lightgreen").place(relx=0.5, y=60, anchor="n")
    entry_login_username = tk.Entry(frame_login, width=35)
    entry_login_username.place(relx=0.5, y=90, anchor="n")
    
    tk.Label(frame_login, text="Password:", font=("Arial", 14), bg="lightgreen").place(relx=0.5, y=120, anchor="n")
    entry_login_password = tk.Entry(frame_login, width=35, show="*")
    entry_login_password.place(relx=0.5, y=150, anchor="n")

    tk.Button(frame_login, font=("Arial", 12, "bold"), text="Log In", command=check_login).place(relx=0.5, y=210, anchor="n")

    exit_button_second = tk.Button(text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
    exit_button_second.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    root.mainloop()

if __name__ == "__main__":
    main()