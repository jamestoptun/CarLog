import tkinter as tk                                                           #rely/x = changes pistion relative to window
from tkinter import filedialog, messagebox
import sqlite3
from PIL import ImageTk, Image
from datetime import datetime
from tkcalendar import DateEntry

expenses = [] #List for expenses
total_money_spent = 0.0  #Track total money spent

#Setting up database
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
            license_plate TEXT NOT NULL UNIQUE,
            date_of_ownership TEXT,
            total_money_spent REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close() #Close database

def show_carlog_page():
    main_page.pack_forget()
    carlog_page.pack(expand=True, fill=tk.BOTH)
    fetch_user_data() #Fetch user data to display

def fetch_user_data():
    conn = sqlite3.connect('carlog.db')
    cursor = conn.cursor()
    #Fetch the date of ownership and total money spent for the user with id = 1
    cursor.execute('SELECT date_of_ownership, total_money_spent FROM users WHERE id = 1')  #Assuming single user
    user_data = cursor.fetchone() #Get result of the query
    conn.close()

    if user_data:
        #Set date of ownership entry to the fetched date
        date_of_ownership_entry.set_date(datetime.strptime(user_data[0], "%d/%m/%Y"))
        #Updates the total money spent using var
        total_money_spent_var.set(f"Total Money Spent: ${user_data[1]:.2f}")
#Open image
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    if file_path:
        img = Image.open(file_path) #Open selected image
        img = img.resize((300, 225), Image.LANCZOS) #Resize
        img = ImageTk.PhotoImage(img) #Convert to PhotoImage
        car_img_label.config(image=img) #Populate image label with image
        upload_img_button.place_forget()  #Hide the "Upload Image" button

def update_odometer():
    new_odometer = odometer_entry.get() #
    real_odometer = new_odometer.replace(",", "") #Removes commas from value 
    if real_odometer.isdigit(): #Check if the value is a valid postive number using isdigit
        messagebox.showinfo("Update", f"Odometer updated to {new_odometer} km")
    else:
        messagebox.showerror("Error", "Please enter a valid positive number")

def update_ownership_date():
    new_date = date_of_ownership_entry.get() #Get date from DateEntry
    try:
        datetime.strptime(new_date, "%d/%m/%Y")
        conn = sqlite3.connect('carlog.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET date_of_ownership = ? WHERE id = 1', (new_date,))
        conn.commit()
        conn.close()
        fetch_user_data() #Refreshes display
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid date")

def add_expense():
    global total_money_spent
    expense_type = expense_type_entry.get()
    expense_amount = expense_amount_entry.get()

    try:
        expense_amount_float = float(expense_amount.replace(",", "")) #Convert to float and removes commas
        if expense_amount_float < 0:
            raise ValueError

        expense_date = datetime.now().strftime("%d/%m/%Y") #Gets current date
        expenses.append((expense_type, expense_amount_float, expense_date)) #Add user input to list

        total_money_spent += expense_amount_float #Updates total)money_spent
        total_money_spent_var.set(f"Total Money Spent: ${total_money_spent:.2f}") #Display

        update_history_log() #Update history log display

        #Clears entry fields
        expense_type_entry.delete(0, tk.END)
        expense_amount_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number for the amount spent.")

def update_history_log():
    for widget in history_frame.winfo_children(): #Returns list of child widgets of history_frame
        widget.destroy()

    for expense in expenses:
        expense_label = tk.Label(history_frame, text=f"{expense[0]}: ${expense[1]:.2f} on {expense[2]}", font=("Lato", 10), anchor="w")
        expense_label.pack(fill=tk.X) #Add each expense entry to the log display

def calculate_average():
    try:
        months = int(months_entry.get()) #Get number of months
        if months <= 0:
            raise ValueError
        average_spending = total_money_spent / months #Calculate average spending
        average_spending_var.set(f"Avg. Spending per Month: ${average_spending:.2f}") #Update
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number for months.")

root = tk.Tk()
root.title("CarLog - Car Maintenance App")
root.attributes('-fullscreen', True)
root.iconbitmap('carr.ico')

#Main Page
main_page = tk.Frame(root)
main_page.pack(expand=True, fill=tk.BOTH)

main_label = tk.Label(main_page, text="Welcome to CarLog - Your Personal Car Maintenance App", font=("Lato", 18, "bold"))
main_label.pack(pady=20)

enter_button = tk.Button(main_page, text="Enter", command=show_carlog_page, font=("Lato", 16), bg="#4CAF50", fg="white", padx=20, pady=10)
enter_button.pack(pady=20)

exit_button_main = tk.Button(main_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_main.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

#CarLog Page
carlog_page = tk.Frame(root)

#All widgets which display
car_img_label = tk.Label(carlog_page, text="No image selected", font=("Lato", 12))
car_img_label.place(relx=0.5, rely=0.05, anchor="n")
upload_img_button = tk.Button(carlog_page, text="Upload Image", command=open_image, font=("Lato", 12), bg="#4CAF50", fg="white")
upload_img_button.place(relx=0.5, rely=0.15, anchor="n")

notes_label = tk.Label(carlog_page, text="Description/Notes:", font=("Lato", 12))
notes_label.place(relx=0.02, rely=0.06, anchor="nw")
notes_text = tk.Text(carlog_page, font=("Lato", 12), wrap=tk.WORD)
notes_text.place(relx=0.02, rely=0.11, anchor="nw", relwidth=0.30, relheight=0.15)

history_label = tk.Label(carlog_page, text="Expense History Log:", font=("Lato", 12))
history_label.place(relx=0.65, rely=0.05, anchor="nw")
history_frame = tk.Frame(carlog_page, bg="white", bd=2)
history_frame.place(relx=0.65, rely=0.10, anchor="nw", relwidth=0.3, relheight=0.5)

odometer_label = tk.Label(carlog_page, text="Total Odometer:", font=("Lato", 12))
odometer_label.place(relx=0.02, rely=0.29, anchor="nw")
odometer_entry = tk.Entry(carlog_page, font=("Lato", 12))
odometer_entry.place(relx=0.02, rely=0.34, anchor="nw", relwidth=0.12)
update_odometer_button = tk.Button(carlog_page, text="Update Odometer", command=update_odometer, font=("Lato", 12), bg="#4CAF50", fg="white")
update_odometer_button.place(relx=0.02, rely=0.39, anchor="nw")

date_of_ownership_label = tk.Label(carlog_page, text="Date of Ownership:", font=("Lato", 12))
date_of_ownership_label.place(relx=0.16, rely=0.29, anchor="nw")
date_of_ownership_entry = DateEntry(carlog_page, font=("Lato", 12), date_pattern="dd/mm/yyyy")
date_of_ownership_entry.place(relx=0.16, rely=0.34, anchor="nw", relwidth=0.1)

expense_type_label = tk.Label(carlog_page, text="Type of Expense:", font=("Lato", 12))
expense_type_label.place(relx=0.02, rely=0.45, anchor="nw")
expense_type_entry = tk.Entry(carlog_page, font=("Lato", 12))
expense_type_entry.place(relx=0.02, rely=0.5, anchor="nw", relwidth=0.12)

expense_amount_label = tk.Label(carlog_page, text="Money Spent ($):", font=("Lato", 12))
expense_amount_label.place(relx=0.16, rely=0.45, anchor="nw")
expense_amount_entry = tk.Entry(carlog_page, font=("Lato", 12))
expense_amount_entry.place(relx=0.16, rely=0.5, anchor="nw", relwidth=0.12)

add_expense_button = tk.Button(carlog_page, text="Add Expense", command=add_expense, font=("Lato", 12), bg="#4CAF50", fg="white")
add_expense_button.place(relx=0.16, rely=0.55, anchor="nw")

total_money_spent_var = tk.StringVar(value=f"Total Money Spent: ${total_money_spent:.2f}")
total_money_spent_label = tk.Label(carlog_page, textvariable=total_money_spent_var, font=("Lato", 12))
total_money_spent_label.place(relx=0.02, rely=0.7, anchor="nw")

months_label = tk.Label(carlog_page, text="Number of Months:", font=("Lato", 12))
months_label.place(relx=0.02, rely=0.80, anchor="nw")
months_entry = tk.Entry(carlog_page, font=("Lato", 12))
months_entry.place(relx=0.13, rely=0.80, anchor="nw", relwidth=0.12)

calculate_button = tk.Button(carlog_page, text="Calculate Avg.", command=calculate_average, font=("Lato", 12), bg="#4CAF50", fg="white")
calculate_button.place(relx=0.26, rely=0.80, anchor="nw")

average_spending_var = tk.StringVar(value="Avg. Spending per Month: $0.00")
average_spending_label = tk.Label(carlog_page, textvariable=average_spending_var, font=("Lato", 12))
average_spending_label.place(relx=0.02, rely=0.75, anchor="nw")

update_date_button = tk.Button(carlog_page, text="Update Date", command=update_ownership_date, font=("Lato", 12), bg="#4CAF50", fg="white")
update_date_button.place(relx=0.16, rely=0.39, anchor="nw")

exit_button_carlog = tk.Button(carlog_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_carlog.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

setup_database()
root.mainloop()