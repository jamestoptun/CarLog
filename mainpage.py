import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import ImageTk, Image

car_makes = {
    "BMW": ["3 Series", "5 Series", "X5", "X3", "1 Series", "X1", "2 Series", "4 Series", "X6", "X7"],
    "Toyota": ["Corolla", "Camry", "Hilux", "RAV4", "Yaris", "Prius", "Land Cruiser", "Highlander", "Fortuner", "Innova"],
    "Honda": ["Civic", "Accord", "CR-V", "Jazz", "HR-V", "City", "Fit", "Pilot", "Odyssey", "Brio"],
    "Ford": ["F-150", "Escape", "Explorer", "Ranger", "Mustang", "Edge", "Fusion", "Focus", "Expedition", "Bronco"],
    "Chevrolet": ["Silverado", "Equinox", "Traverse", "Tahoe", "Malibu", "Camaro", "Colorado", "Blazer", "Trailblazer", "Impala"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder", "Murano", "Maxima", "Frontier", "Versa", "Armada", "Titan"],
    "Hyundai": ["Elantra", "Sonata", "Santa Fe", "Tucson", "Palisade", "Accent", "Kona", "Ioniq", "Venue", "Nexo"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "A-Class", "GLA", "S-Class", "GLS", "G-Class", "CLA"],
    "Volkswagen": ["Golf", "Polo", "Tiguan", "Passat", "Jetta", "Touareg", "Arteon", "T-Roc", "Atlas", "ID.4"],
    "Audi": ["A4", "Q5", "A6", "Q7", "A3", "Q3", "A5", "Q8", "A7", "E-Tron"]
}

car_years = [str(year) for year in range(1980, 2026)]

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
        show_main_page()
    conn.close()

def update_car_model(event):
    selected_make = car_make_entry.get()
    if selected_make in car_makes:
        car_model_entry['values'] = car_makes[selected_make]
    else:
        car_model_entry['values'] = []

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
car_make_entry = ttk.Combobox(second_page, font=("Lato", 14), values=list(car_makes.keys()))
car_make_entry.place(x=550, y=90)
car_make_entry.bind("<<ComboboxSelected>>", update_car_model)

car_model_label = tk.Label(second_page, text="Car Model:", font=("Lato", 14), padx=10, pady=5)
car_model_label.place(x=430, y=130)
car_model_entry = ttk.Combobox(second_page, font=("Lato", 14))
car_model_entry.place(x=550, y=130)

car_year_label = tk.Label(second_page, text="Car Year:", font=("Lato", 14), padx=10, pady=5)
car_year_label.place(x=430, y=170)
car_year_entry = ttk.Combobox(second_page, font=("Lato", 14), values=car_years)
car_year_entry.place(x=550, y=170)

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