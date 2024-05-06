from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Learn to get images")

root.iconbitmap('imgs/penicon.ico')

my_img = Image.open('c:\\Users\\james\\Downloads\\Python quiz\\miinimetr diss trac aginest ksi.jpg')

resized = my_img.resize((300,225),Image.LANCZOS)

new_pic = ImageTk.PhotoImage(resized)

my_Lable = Label(root, image = new_pic)
my_Lable.pack(pady=20)

button_exit = Button(root, text="Exit Program", command=root.quit)
button_exit.pack()

root.mainloop()