import tkinter as tk
from tkinter import filedialog
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
            vin TEXT NOT NULL UNIQUE,
            license_plate TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def show_carlog_page():
    main_page.pack_forget()
    carlog_page.pack(expand=True, fill=tk.BOTH)

def show_main_page():
    carlog_page.pack_forget()
    main_page.pack(expand=True, fill=tk.BOTH)

root = tk.Tk()
root.title("CarLog - Car Maintenance App")
root.attributes('-fullscreen', True)
root.iconbitmap('carr.ico')

main_page = tk.Frame(root)
main_page.pack(expand=True, fill=tk.BOTH)

main_label = tk.Label(main_page, text="Welcome to CarLog - Your Personal Car Maintenance App", font=("Lato", 18, "bold"))
main_label.pack(pady=20)

enter_button = tk.Button(main_page, text="Enter", command=show_carlog_page, font=("Lato", 16), bg="#4CAF50", fg="white", padx=20, pady=10)
enter_button.pack(pady=20)

exit_button_main = tk.Button(main_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_main.place(relx=1.0, rely=1.0, anchor="se", x=1, y=1)

carlog_page = tk.Frame(root)

car_img_label = tk.Label(carlog_page, text="No image selected", font=("Lato", 12))
car_img_label.place(relx=0.5, rely=0.05, anchor="n")

upload_img_button = tk.Button(carlog_page, text="Upload Image", font=("Lato", 12), bg="#4CAF50", fg="white")
upload_img_button.place(relx=0.5, rely=0.15, anchor="n")

notes_label = tk.Label(carlog_page, text="Description/Notes:", font=("Lato", 12))
notes_label.place(relx=0.5, rely=0.25, anchor="n")
notes_text = tk.Text(carlog_page, font=("Lato", 12))
notes_text.place(relx=0.5, rely=0.35, anchor="n", width=0.9, height=0.2)

history_label = tk.Label(carlog_page, text="History Log:", font=("Lato", 12))
history_label.place(relx=0.75, rely=0.6, anchor="n")
history_frame = tk.Frame(carlog_page, bg="white", bd=2)
history_frame.place(relx=0.75, rely=0.65, anchor="n", width=0.4, height=0.6)

odometer_label = tk.Label(carlog_page, text="Total Odometer:", font=("Lato", 12))
odometer_label.place(relx=0.25, rely=0.6, anchor="n")
odometer_entry = tk.Entry(carlog_page, font=("Lato", 12))
odometer_entry.place(relx=0.25, rely=0.65, anchor="n", width=0.2)

date_of_ownership_label = tk.Label(carlog_page, text="Date of Ownership (dd/mm/yyyy):", font=("Lato", 12))
date_of_ownership_label.place(relx=0.20, rely=0.29, anchor="nw")

exit_button_carlog = tk.Button(carlog_page, text="Exit", command=root.destroy, font=("Lato", 16), width=5, height=1, bg="#f44336", fg="white")
exit_button_carlog.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

setup_database()

root.mainloop()