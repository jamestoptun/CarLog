import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from PIL import ImageTk, Image
import subprocess

car_makes = {
    "Toyota": ["Corolla", "Camry", "RAV4", "Highlander", "Prius", "Tacoma", "Land Cruiser", "4Runner", "Avalon", "Yaris"],
    "BMW": ["3 Series", "5 Series", "7 Series", "X5", "X3", "M3", "M5", "i3", "i8", "Z4"],
    "Ford": ["F-150", "Escape", "Explorer", "Mustang", "Fusion", "Edge", "Ranger", "Expedition", "Bronco", "Focus"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Fit", "Odyssey", "Ridgeline", "HR-V", "Passport", "Insight"],
    "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe", "Traverse", "Colorado", "Blazer", "Camaro", "Suburban", "Trax"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLA", "GLS", "A-Class", "CLA", "SL"],
    "Volkswagen": ["Golf", "Passat", "Tiguan", "Jetta", "Atlas", "Beetle", "Touareg", "Arteon", "ID.4", "Polo"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Murano", "Pathfinder", "Frontier", "Maxima", "Versa", "GT-R", "Kicks"],
    "Audi": ["A3", "A4", "A6", "Q5", "Q7", "Q3", "A8", "Q8", "e-tron", "TT"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Palisade", "Accent", "Kona", "Veloster", "Venue", "Ioniq"]
}

car_years = [str(year) for year in range(1980, 2025)]

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

def show_second_page():
    main_page.pack_forget()
    second_page.pack(expand=True, fill=tk.BOTH)

def show_main_page():
    second_page.pack_forget()
    main_page.pack(expand=True, fill=tk.BOTH)

def update_car_models(event):
    selected_make = car_make_combo.get()
    models = car_makes.get(selected_make, [])
    car_model_combo['values'] = models
    if models:
        car_model_combo.current(0)

def get_information():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    car_make = car_make_combo.get()
    car_model = car_model_combo.get()
    car_year = car_year_combo.get()
    vin = vin_entry.get()
    license_plate = license_plate_entry.get()

    if not (first_name and last_name and car_make and car_model and car_year and vin and license_plate):
        messagebox.showerror("Error", "All fields must be filled")
        return

    conn = sqlite3.connect('carlog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE vin=? OR license_plate=?', (vin, license_plate))
    result = cursor.fetchone()
    
    if result[0] > 0:
        messagebox.showerror("Error", "VIN or License Plate already exists")
    else:
        cursor.execute('''
            INSERT INTO users (first_name, last_name, car_make, car_model, car_year, vin, license_plate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, car_make, car_model, car_year, vin, license_plate))
        conn.commit()
        messagebox.showinfo("Success", "Information stored successfully")
        root.destroy()
        subprocess.run(["python", "carlog.py"])
    conn.close()

root = tk.Tk()
root.title("CarLog - Car Maintenance App")
root.attributes('-fullscreen', True)
root.iconbitmap('carr.ico')

my_img = Image.open("car1.png")
resized = my_img.resize((225, 225), Image.LANCZOS)
new_pic = ImageTk.PhotoImage(resized)

main_page = tk.Frame(root)
main_page.pack(expand=True, fill=tk.BOTH)

my_label = tk.Label(main_page, image=new_pic)
my_label.pack(pady=20)

info_label = tk.Label(main_page, text="Welcome to CarLog - Your Personal Car Maintenance App", font=("Lato", 18, "bold"))
info_label.pack()

enter_button = tk.Button(main_page, text="Enter", command=show_second_page, font=("Lato", 16), bg="#4CAF50", fg="white", padx=20, pady=10)
enter_button.pack(pady=20)

exit_button_main = tk.Button(main_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_main.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

second_page = tk.Frame(root)

first_name_label = tk.Label(second_page, text="First Name:", font=("Lato", 14), padx=10, pady=5)
first_name_label.place(x=430, y=10)
first_name_entry = tk.Entry(second_page, font=("Lato", 14))
first_name_entry.place(x=550, y=10)

last_name_label = tk.Label(second_page, text="Last Name:", font=("Lato", 14), padx=10, pady=5)
last_name_label.place(x=430, y=50)
last_name_entry = tk.Entry(second_page, font=("Lato", 14))
last_name_entry.place(x=550, y=50)

car_make_label = tk.Label(second_page, text="Car Make:", font=("Lato", 14), padx=10, pady=5)
car_make_label.place(x=430, y=90)
car_make_combo = ttk.Combobox(second_page, font=("Lato", 14), values=list(car_makes.keys()))
car_make_combo.place(x=550, y=90)
car_make_combo.bind("<<ComboboxSelected>>", update_car_models)

car_model_label = tk.Label(second_page, text="Car Model:", font=("Lato", 14), padx=10, pady=5)
car_model_label.place(x=430, y=130)
car_model_combo = ttk.Combobox(second_page, font=("Lato", 14))
car_model_combo.place(x=550, y=130)

car_year_label = tk.Label(second_page, text="Car Year:", font=("Lato", 14), padx=10, pady=5)
car_year_label.place(x=430, y=170)
car_year_combo = ttk.Combobox(second_page, font=("Lato", 14), values=car_years)
car_year_combo.place(x=550, y=170)

vin_label = tk.Label(second_page, text="VIN:", font=("Lato", 14), padx=10, pady=5)
vin_label.place(x=430, y=210)
vin_entry = tk.Entry(second_page, font=("Lato", 14))
vin_entry.place(x=550, y=210)

license_plate_label = tk.Label(second_page, text="License Plate Number:", font=("Lato", 14), padx=10, pady=5)
license_plate_label.place(x=335, y=250)
license_plate_entry = tk.Entry(second_page, font=("Lato", 14))
license_plate_entry.place(x=550, y=250)

submit_button = tk.Button(second_page, text="Submit", command=get_information, font=("Lato", 14), bg="#4CAF50", fg="white", padx=8, pady=6)
submit_button.place(relx=0.5, y=295, anchor="n")

return_button = tk.Button(second_page, text="Return to Main Page", command=show_main_page, font=("Lato", 14), padx=10, pady=10)
return_button.place(relx=0.5, y=355, anchor="n")

exit_button_second = tk.Button(second_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_second.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

second_page.pack_forget()

setup_database()
root.mainloop()