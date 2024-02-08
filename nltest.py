from tkinter import *
import bin.nonlinear as nonlinear

def com():
	nonlinear.move_right_animation(botton, 700, 300)
root = Tk()
root.geometry("600x600")
img = PhotoImage(file="res/pic/default.png")
botton = Label(root, image=img)
botton.place(x=100, y=100)
x = 100
root.mainloop()