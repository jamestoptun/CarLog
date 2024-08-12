import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from PIL import ImageTk, Image
from datetime import datetime

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
    conn.close()

def show_carlog_page():
    main_page.pack_forget()
    carlog_page.pack(expand=True, fill=tk.BOTH)
    #Display user data
    fetch_user_data()

def fetch_user_data():
    conn = sqlite3.connect('carlog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date_of_ownership, total_money_spent FROM users WHERE id = 1')  # Assuming single user
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        date_of_ownership_entry.delete(0, tk.END)
        date_of_ownership_entry.insert(0, user_data[0] if user_data[0] else "")
        total_money_spent_var.set(f"Total Money Spent: ${user_data[1]:.2f}")
        
        if user_data[0]:
            date_of_ownership = datetime.strptime(user_data[0], "%d/%m/%Y")
            months_owned = (datetime.now().year - date_of_ownership.year) * 12 + datetime.now().month - date_of_ownership.month
            avg_monthly_spent = user_data[1] / months_owned if months_owned > 0 else 0
            avg_monthly_spending_var.set(f"Average Monthly Spending: ${avg_monthly_spent:.2f}")

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((300, 225), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        car_img_label.config(image=img)
        car_img_label.image = img

def update_odometer():
    new_odometer = odometer_entry.get()
    messagebox.showinfo("Update", f"Odometer updated to {new_odometer} km")

def update_ownership_date():
    new_date = date_of_ownership_entry.get()
    try:
        datetime.strptime(new_date, "%d/%m/%Y")
        conn = sqlite3.connect('carlog.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET date_of_ownership = ? WHERE id = 1', (new_date,))
        conn.commit()
        conn.close()
        fetch_user_data()
    except ValueError:
        messagebox.showerror("Error", "Please enter the date in the format dd/mm/yyyy")

root = tk.Tk()
root.title("CarLog - Car Maintenance App")
root.attributes('-fullscreen', True)
root.iconbitmap('carr.ico')

# Main Page
main_page = tk.Frame(root)
main_page.pack(expand=True, fill=tk.BOTH)

main_label = tk.Label(main_page, text="Welcome to CarLog - Your Personal Car Maintenance App", font=("Lato", 18, "bold"))
main_label.pack(pady=20)

enter_button = tk.Button(main_page, text="Enter", command=show_carlog_page, font=("Lato", 16), bg="#4CAF50", fg="white", padx=20, pady=10)
enter_button.pack(pady=20)

exit_button_main = tk.Button(main_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_main.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

# CarLog Page
carlog_page = tk.Frame(root)

car_img_label = tk.Label(carlog_page, text="No image selected", font=("Lato", 12))
car_img_label.place(relx=0.5, rely=0.05, anchor="n")
upload_img_button = tk.Button(carlog_page, text="Upload Image", command=open_image, font=("Lato", 12), bg="#4CAF50", fg="white")
upload_img_button.place(relx=0.5, rely=0.15, anchor="n")

notes_label = tk.Label(carlog_page, text="Description/Notes:", font=("Lato", 12))
notes_label.place(relx=0.02, rely=0.06, anchor="nw") #Texts wraps when it reaches the end of the line.
notes_text = tk.Text(carlog_page, font=("Lato", 12), wrap=tk.WORD)
notes_text.place(relx=0.02, rely=0.11, anchor="nw", relwidth=0.35, relheight=0.15)

history_label = tk.Label(carlog_page, text="History Log:", font=("Lato", 12))
history_label.place(relx=0.75, rely=0.55, anchor="nw")
history_frame = tk.Frame(carlog_page, bg="white", bd=2)
history_frame.place(relx=0.75, rely=0.6, anchor="nw", relwidth=0.2, relheight=0.3)

odometer_label = tk.Label(carlog_page, text="Total Odometer:", font=("Lato", 12))
odometer_label.place(relx=0.02, rely=0.29, anchor="nw")
odometer_entry = tk.Entry(carlog_page, font=("Lato", 12))
odometer_entry.place(relx=0.02, rely=0.34, anchor="nw", relwidth=0.1)
update_odometer_button = tk.Button(carlog_page, text="Update Odometer", command=update_odometer, font=("Lato", 12), bg="#4CAF50", fg="white")
update_odometer_button.place(relx=0.02, rely=0.39, anchor="nw")

date_of_ownership_label = tk.Label(carlog_page, text="Date of Ownership (dd/mm/yyyy):", font=("Lato", 12))
date_of_ownership_label.place(relx=0.20, rely=0.29, anchor="nw")
date_of_ownership_entry = tk.Entry(carlog_page, font=("Lato", 12))
date_of_ownership_entry.place(relx=0.20, rely=0.34, anchor="nw", relwidth=0.2)
update_date_button = tk.Button(carlog_page, text="Update Date", command=update_ownership_date, font=("Lato", 12), bg="#4CAF50", fg="white")
update_date_button.place(relx=0.20, rely=0.39, anchor="nw")

return_button = tk.Button(carlog_page, text="Return to Main Page", command=show_carlog_page, font=("Lato", 12), bg="#4CAF50", fg="white")
return_button.place(relx=0.05, rely=0.95, anchor="nw")

exit_button_carlog = tk.Button(carlog_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_carlog.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

setup_database()
root.mainloop()
