from tkinter import *
import os.path
import time
import bin.configLoader as configLoader
import bin.videoPlay as videoPlay
import bin.sideLoad as sideLoad
import bin.nonlinear as nonlinear
import random
from PIL import Image, ImageTk

def resize_image(image_path, height):
    original_image = Image.open(image_path)
    aspect_ratio = height / original_image.height
    width = int(original_image.width * aspect_ratio)
    resized_image = original_image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)


config = configLoader.load_config()


def func(button: sideLoad.Button, root) -> None:
    info_label = Label(root, text="在\n抽", font=config["font3"])
    button.pack_forget()
    info_label.pack(expand=True, fill=X)
    root = Toplevel(bg="#2e2731")
    root.geometry("1280x720+%i+%i" % ((root.winfo_screenwidth() - 1280) / 2, (root.winfo_screenheight() - 720) / 2))
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    chosen = random.choice(config["nameList"])
    # logging.debug("完成随机选择: %s" % chosen)
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
    vp = videoPlay.video_play(root, config["goldVideoPath"] if gold else config["purpleVideoPath"])
    time.sleep(5)
    while True:
        if vp.is_paused():
            break
        time.sleep(0.05)
    vp.place_forget()
    vp.destroy()
    if os.path.exists("res\\pic\\%s.png" % name):
        file = "res\\pic\\%s.png" % name
    else:
        file = "res\\pic\\default.png"
    root.withdraw()
    root.destroy()
    root = Toplevel(bg="#272733")
    root.geometry("1280x720+%i+%i" % ((root.winfo_screenwidth() - 1280) / 2, (root.winfo_screenheight() - 720) / 2))
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    img = resize_image(file, 650)
    img_label = Label(root, image=img, bg="#272733")
    text1_label = Label(root, text=name, fg="white", bg="#272733", font=config["font1"])
    text2_label = Label(root, text=into, fg="white", bg="#272733", font=config["font2"])
    img_label.place(x=1000, y=50)
    text1_label.place(x=0, y=350)
    text2_label.place(x=0, y=490)
    nonlinear.move_right_animation(img_label, 1200, -350, img=img)
    time.sleep(0.1)
    nonlinear.move_right_animation(text1_label, 900, 300)
    time.sleep(0.05)
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
    info_label.pack_forget()
    button.pack(expand=True, fill=X)
    time.sleep(6)
    root.withdraw()
    root.destroy()


def on_board(button, root):
    chosen = random.choice(config["nameList"])
    if " " in chosen:
        chosen = chosen[:chosen.find(" ")]
    if chosen[0] == "|":
        chosen = chosen[1:]
    temp = ""
    for x in chosen:
        temp += x + "\n"
    chosen = temp[:-1]

    def dis_show(label, button_tar):
        label.destroy()
        button_tar.pack(expand=True, fill=X)
        button_tar.config(state=sideLoad.NORMAL)
    name_label = Label(root, text=chosen, font=config["font3"])
    button.config(state=sideLoad.DISABLED)
    button.pack_forget()
    name_label.pack(expand=True, fill=X)
    name_label.after(2000, lambda: dis_show(name_label, button))


if __name__ == "__main__":
    if config["defaultMode"] == "sideLoad":
        load = sideLoad.SideLoad(call=func, call2=on_board, **config["sideLoad"])
