import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import ImageTk, Image

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
            vin TEXT NOT NULL,
            license_plate TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def show_second_page():
    main_page.pack_forget()
    second_page.pack(expand=True, fill=tk.BOTH)

def show_main_page():
    second_page.pack_forget()
    main_page.pack(expand=True, fill=tk.BOTH)

def get_information():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    car_make = car_make_entry.get()
    car_model = car_model_entry.get()
    car_year = car_year_entry.get()
    vin = vin_entry.get()
    license_plate = license_plate_entry.get()

    conn = sqlite3.connect('carlog.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (first_name, last_name, car_make, car_model, car_year, vin, license_plate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, car_make, car_model, car_year, vin, license_plate))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Information stored successfully")
    show_main_page()

root = tk.Tk()
root.title("CarLog - Car Maintenance App")
root.attributes('-fullscreen', True)
root.iconbitmap('carr.ico')

my_img = Image.open("placeholder.carlog.jpg")
resized = my_img.resize((300, 225), Image.LANCZOS)
new_pic = ImageTk.PhotoImage(resized)

main_page = tk.Frame(root)
main_page.pack(expand=True, fill=tk.BOTH)

my_label = tk.Label(main_page, image=new_pic)
my_label.pack(pady=20)

info_label = tk.Label(main_page, text="Welcome to CarLog - Your Personal Car Maintenance App", font=(16))
info_label.pack()

enter_button = tk.Button(main_page, text="Enter", command=show_second_page, font=(12))
enter_button.pack(pady=20)

exit_button_second = tk.Button(main_page, text="Exit", command=root.destroy, font=(16), width=10, height=2)
exit_button_second.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

second_page = tk.Frame(root)

first_name_label = tk.Label(second_page, text="First Name:", font=(12))
first_name_label.grid(row=0, column=0, padx=10, pady=5)
first_name_entry = tk.Entry(second_page, font=(12))
first_name_entry.grid(row=0, column=1, padx=10, pady=5)

last_name_label = tk.Label(second_page, text="Last Name:", font=(12))
last_name_label.grid(row=1, column=0, padx=10, pady=5)
last_name_entry = tk.Entry(second_page, font=(12))
last_name_entry.grid(row=1, column=1, padx=10, pady=5)

car_make_label = tk.Label(second_page, text="Car Make:", font=(12))
car_make_label.grid(row=2, column=0, padx=10, pady=5)
car_make_entry = tk.Entry(second_page, font=(12))
car_make_entry.grid(row=2, column=1, padx=10, pady=5)

car_model_label = tk.Label(second_page, text="Car Model:", font=(12))
car_model_label.grid(row=3, column=0, padx=10, pady=5)
car_model_entry = tk.Entry(second_page, font=(12))
car_model_entry.grid(row=3, column=1, padx=10, pady=5)

car_year_label = tk.Label(second_page, text="Car Year:", font=(12))
car_year_label.grid(row=4, column=0, padx=10, pady=5)
car_year_entry = tk.Entry(second_page, font=(12))
car_year_entry.grid(row=4, column=1, padx=10, pady=5)

vin_label = tk.Label(second_page, text="VIN:", font=(12))
vin_label.grid(row=5, column=0, padx=10, pady=5)
vin_entry = tk.Entry(second_page, font=(12))
vin_entry.grid(row=5, column=1, padx=10, pady=5)

license_plate_label = tk.Label(second_page, text="License Plate Number:", font=(12))
license_plate_label.grid(row=6, column=0, padx=10, pady=5)
license_plate_entry = tk.Entry(second_page, font=(12))
license_plate_entry.grid(row=6, column=1, padx=10, pady=5)

submit_button = tk.Button(second_page, text="Submit", command=get_information, font=(12))
submit_button.grid(row=7, column=0, columnspan=2, pady=10)

return_button = tk.Button(second_page, text="Return to Main Page", command=show_main_page, font=(12))
return_button.grid(row=8, column=0, columnspan=2, pady=10)

exit_button_second = tk.Button(second_page, text="Exit", command=root.destroy, font=(16), width=10, height=2)
exit_button_second.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

second_page.grid_rowconfigure(10, weight=1)
second_page.grid_columnconfigure(10, weight=1)

setup_database()
root.mainloop()