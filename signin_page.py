import tkinter as tk
import sqlite3
from tkinter import messagebox
import subprocess

#Set up the database tables
def setup_database():
    conn = sqlite3.connect('carlog.db') #Connects to SGL
    cursor = conn.cursor()
    #Creates the table "Users"
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
    #Creates the table "User_logins"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logins (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit() #Commits the changes then closes database
    conn.close()

def open_mainpage():
    username = username_entry.get() #Retrives user inputs from entry fields
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    email = email_entry.get()

    #Checks if password matches
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    #Checks for errors in email
    if "@" not in email:
        messagebox.showerror("Error", "Invalid email address, no \"@\"")
        return

    try:
        conn = sqlite3.connect('carlog.db')
        cursor = conn.cursor()
        #Inserts the new user login details into "User_logins"
        cursor.execute("INSERT INTO user_logins (username, password, email) VALUES (?, ?, ?)", 
                       (username, password, email))
        conn.commit()

        #Gets the ID for new user login data
        cursor.execute("SELECT id FROM user_logins WHERE username = ?", (username,))
        user_login_id = cursor.fetchone()[0]
        #Inserts it into "User"
        cursor.execute('''
            INSERT INTO users (user_login_id)
            VALUES (?)
        ''', (user_login_id,))
        
        conn.commit()
        conn.close()
        #Shows success creating account
        messagebox.showinfo("Success", "Account created successfully")
        #Closes current window and open main page
        root.destroy()
        subprocess.run(["python", "mainpage.py"])
    except Exception as e:
        #Incase of database errors
        messagebox.showerror("Database Error", str(e))

def check_login():
    username = entry_login_username.get()
    password = entry_login_password.get()

    try:
        conn = sqlite3.connect('carlog.db')
        cursor = conn.cursor()
        #Checks if the username and password match entry in the "User_logins" table
        cursor.execute("SELECT * FROM user_logins WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        #If user found, notify success and open main page
        if user:
            messagebox.showinfo("Success", "Login successful")
            root.destroy()
            subprocess.run(["python", "carlog.py"])
        # If user not found, notify of error
        else:
            messagebox.showerror("Error", "Invalid username or password")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

#Sets up database
setup_database()

def main():
    #Declare global variables for widgets
    global root, username_entry, password_entry, confirm_password_entry, email_entry, entry_login_username, entry_login_password

    #Creates the main window
    root = tk.Tk()
    root.title("Sign-Up and Log-In Page") #Title
    root.attributes('-fullscreen', True) #Makes window fullscreen

    #Create frames for signin and login
    frame_signup = tk.Frame(root, padx=20, pady=20, bg="lightblue")
    frame_login = tk.Frame(root, padx=20, pady=20, bg="lightgreen")

    #Placing frames
    frame_signup.place(relx=0, rely=0, relwidth=0.5, relheight=1.0)
    frame_login.place(relx=0.5, rely=0, relwidth=0.5, relheight=1.0)

    #Setting up signin section
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

    #Creates button to process signin
    tk.Button(frame_signup, font=("Arial", 12, "bold"), text="Sign Up", command=open_mainpage).place(relx=0.5, y=310, anchor="n")

    #Login section
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

    #Start loop
    root.mainloop()

#Run the function if the program is executed
if __name__ == "__main__":
    main()