from tkinter import *
from PIL import ImageTk, Image

def show_second_page():
    main_page.pack_forget()
    second_page.pack()

def show_main_page():
    second_page.pack_forget()
    main_page.pack()

def get_information():
    name = name_entry.get()
    last_name = last_name_entry.get()
    car_make = car_make_entry.get()
    car_model = car_model_entry.get()
    car_year = car_year_entry.get()
    password = password_entry.get()

root = Tk()
root.title("CarLog - Car Maintenance App")
root.geometry("400x400")
root.iconbitmap('carr.ico')

my_img = Image.open("palceholder,carlog.jpg")
resized = my_img.resize((300, 225), Image.LANCZOS)
new_pic = ImageTk.PhotoImage(resized)

main_page = Frame(root)
main_page.pack()

my_label = Label(main_page, image=new_pic)
my_label.pack(pady=20)

info_label = Label(main_page, text="Welcome to CarLog - Your Personal Car Maintenance App", font=(16))
info_label.pack()

enter_button = Button(main_page, text="Enter", command=show_second_page, font=(12))
enter_button.pack(pady=20)

second_page = Frame(root)

name_label = Label(second_page, text="First Name:", font=(12))
name_label.grid(row=0, column=0, padx=10, pady=5)
name_entry = Entry(second_page, font=(12))
name_entry.grid(row=0, column=1, padx=10, pady=5)

last_name_label = Label(second_page, text="Last Name:", font=(12))
last_name_label.grid(row=1, column=0, padx=10, pady=5)
last_name_entry = Entry(second_page, font=(12))
last_name_entry.grid(row=1, column=1, padx=10, pady=5)

car_make_label = Label(second_page, text="Car Make:", font=(12))
car_make_label.grid(row=2, column=0, padx=10, pady=5)
car_make_entry = Entry(second_page, font=(12))
car_make_entry.grid(row=2, column=1, padx=10, pady=5)

car_model_label = Label(second_page, text="Car Model:", font=(12))
car_model_label.grid(row=3, column=0, padx=10, pady=5)
car_model_entry = Entry(second_page, font=(12))
car_model_entry.grid(row=3, column=1, padx=10, pady=5)

car_year_label = Label(second_page, text="Car Year:", font=(12))
car_year_label.grid(row=4, column=0, padx=10, pady=5)
car_year_entry = Entry(second_page, font=(12))
car_year_entry.grid(row=4, column=1, padx=10, pady=5)

password_label = Label(second_page, text="Password:", font=(12))
password_label.grid(row=5, column=0, padx=10, pady=5)
password_entry = Entry(second_page, show="*", font=(12))  # hiding the password
password_entry.grid(row=5, column=1, padx=10, pady=5)

submit_button = Button(second_page, text="Submit", command=get_information, font=(12))
submit_button.grid(row=6, column=0, columnspan=2, pady=10)

return_button = Button(second_page, text="Return to Main Page", command=show_main_page, font=(12))
return_button.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
