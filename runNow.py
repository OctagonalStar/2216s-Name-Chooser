from tkinter import *
import random
from PIL import Image, ImageTk
import bin.configLoader as configLoader
from bin import videoPlay, nonlinear
from time import sleep
import os
import threading

def resize_image(image_path, height):
    original_image = Image.open(image_path)
    aspect_ratio = height / original_image.height
    width = int(original_image.width * aspect_ratio)
    resized_image = original_image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)


def func1():
    vp = videoPlay.video_play(root, config["goldVideoPath"] if gold else config["purpleVideoPath"])
    sleep(4)
    while True:
        if vp.is_paused():
            break
        sleep(0.02)
    vp.place_forget()
    img = resize_image(file, 650)
    img_label = Label(root, image=img, bg="#272733")
    text1_label = Label(root, text=name, fg="white", bg="#272733", font=config["font1"])
    text2_label = Label(root, text=into, fg="white", bg="#272733", font=config["font2"])
    img_label.place(x=1000, y=50)
    text1_label.place(x=0, y=350)
    text2_label.place(x=0, y=490)
    nonlinear.move_right_animation(img_label, 1200, -350, img=img)
    sleep(0.1)
    nonlinear.move_right_animation(text1_label, 900, 300)
    sleep(0.05)
    nonlinear.move_right_animation(text2_label, 950, 250)
    starts = 4
    if gold:
        starts = 5
    sta_img = resize_image("res\\pic\\star.png", 30)
    for i in range(starts):
        sta_label = Label(root, image=sta_img, bg="#272733")
        sta_label.place(x=0, y=445)
        sta_label.lift()
        nonlinear.move_right_animation(sta_label, 900, 350 + i * 30)
    sleep(6)
    root.withdraw()
    root.quit()


config = configLoader.load_config()
chosen = random.choice(config["nameList"])
gold = False
if chosen[0] == "|":
    gold = True
    chosen = chosen[1:]
if " " in chosen:
    chosen = [chosen[:chosen.find(" ")], chosen[chosen.find(" ") + 1:]]
else:
    chosen = [chosen]
if len(chosen) == 1:
    name = chosen[0]
    into = "这个人很神秘 什么都没有写"
else:
    name = chosen[0]
    into = chosen[1]
if os.path.exists("res\\pic\\%s.png" % name):
    file = "res\\pic\\%s.png" % name
else:
    file = "res\\pic\\default.png"

root = Tk()
root.config(bg="#272733")
root.geometry("1280x720+%i+%i" % ((root.winfo_screenwidth() - 1280) / 2, (root.winfo_screenheight() - 720) / 2))
root.overrideredirect(True)
root.attributes("-topmost", True)
t1 = threading.Thread(target=func1, daemon=True)
root.after(1, lambda: t1.start())
root.mainloop()
