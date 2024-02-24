import difflib
import bin.nonlinear as nonlinear
from bin.configLoader import Config
from bin.randomName import Random
import bin.videoPlay as videoPlay
from tkinter import *
import os.path
import time
from PIL import Image, ImageTk


def resize_image(image_path, height):
    original_image = Image.open(image_path)
    aspect_ratio = height / original_image.height
    width = int(original_image.width * aspect_ratio)
    resized_image = original_image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)


def func(button: Button, root, config: Config, random: Random) -> None:
    # 变量定义
    click = False
    skip = False
    destroy_list = []
    info_label = Label(root, text="在\n抽", font=config.end_page.font3)
    button.pack_forget()
    info_label.pack(expand=True, fill=X)
    chosen = random.choice(config.name_list.list)
    if difflib.SequenceMatcher(None, chosen["name"], chosen["nick"]).quick_ratio() < 0.6:
        into = f"[原名:{chosen['name']}] " + chosen["into"]
    else:
        into = chosen["into"]
    if os.path.exists("res\\pic\\%s.png" % chosen["name"]):
        file = "res\\pic\\%s.png" % chosen["name"]
    elif config.test_features.jpg_support and os.path.exists("res\\pic\\%s.jpg" % chosen["name"]):
        file = "res\\pic\\%s.jpg" % chosen["name"]
    else:
        file = config.end_page.default_pic
    # 动画
    if config.animation.enabled:
        root = Toplevel(bg="#FFFFFF")
        root.geometry("1280x720+%i+%i" % ((root.winfo_screenwidth() - 1280) / 2, (root.winfo_screenheight() - 720) / 2))
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        vp = videoPlay.video_play(root, config.animation.gold_video if chosen["gold"] and chosen["gold"] != 4
        else config.animation.purple_video)

        def wait_double_click(_):
            nonlocal skip, click, vp, root

            def unclick():
                nonlocal click
                click = False

            if click:
                vp.pause()
                skip = True
            else:
                click = True
                root.after(500, unclick)
        # 双击跳过
        if config.animation.double_click_skip:
            vp.bind("<ButtonRelease-1>", wait_double_click)
        for _ in range(config.animation.delay_pause_check * 50):
            time.sleep(0.02)
            if skip:
                break
        while not skip:
            if vp.is_paused():
                break
            time.sleep(0.02)

        root.withdraw()
        destroy_list.append(root)
    # 结果页面
    root = Toplevel(bg=config.end_page.background_color)
    root.geometry("1280x720+%i+%i" % ((root.winfo_screenwidth() - 1280) / 2, (root.winfo_screenheight() - 720) / 2))
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    img = resize_image(file, 650)
    if config.end_page.background_img:
        bg_img = resize_image(config.end_page.background_img, 720)
        img_bg = Label(root, image=bg_img, bg=config.end_page.background_color)
        img_bg.place(x=0, y=0)
    if config.end_page.show_pic:
        img_label = Label(root, image=img, bg=config.end_page.background_color)
        img_label.place(x=1100, y=50)
        nonlinear.animation(config, img_label, 1200, -450, img=img)
    if config.end_page.show_into:
        text2_label = Label(root, text=into, fg="white", bg=config.end_page.background_color,
                            font=config.end_page.font2, anchor="nw", justify="left")
        text2_label.place(x=-100, y=490)
        time.sleep(0.05)
        nonlinear.animation(config, text2_label, 950, 350)
    if config.test_features.global_notification.enabled and config.test_features.global_notification.message:
        notification_label = Label(root, text=config.test_features.global_notification.message, fg="white",
                                   bg=config.end_page.background_color, font=config.end_page.font2,
                                   anchor="nw", justify="left")
        notification_label.place(x=0, y=50)
        time.sleep(0.05)
        nonlinear.animation(config, notification_label, 950, 50)
    text1_label = Label(root, text=chosen["nick"], fg="white", bg=config.end_page.background_color,
                        font=config.end_page.font1)
    text1_label.place(x=-100, y=350)
    time.sleep(0.1)
    nonlinear.animation(config, text1_label, 900, 400)
    starts = 4
    if chosen["gold"] and isinstance(chosen["gold"], bool):
        starts = 5
    elif isinstance(chosen["gold"], int) and config.test_features.multi_star_enable:
        starts = chosen["gold"]
    sta_img = resize_image("res\\pic\\star.png", 30)
    for i in range(starts):
        sta_label = Label(root, image=sta_img, bg=config.end_page.background_color)
        sta_label.place(x=0, y=445)
        sta_label.lift()
        nonlinear.animation(config, sta_label, 900, 350 + i * 30)
    info_label.pack_forget()
    button.pack(expand=True, fill=X)
    time.sleep(config.end_page.close_time - 0.5)
    root.withdraw()
    destroy_list.append(root)
    for i in destroy_list:
        i.destroy()


def on_board(button, root, config: Config, random: Random):
    chosen = random.choice(config.name_list.list)
    temp = ""
    for x in chosen["name"]:
        temp += x + "\n"
    chosen = temp[:-1]

    def dis_show(label, button_tar):
        label.destroy()
        button_tar.pack(expand=True, fill=X)
        button_tar.config(state=NORMAL)

    name_label = Label(root, text=chosen, font=config.end_page.font3)
    button.config(state=DISABLED)
    button.pack_forget()
    name_label.pack(expand=True, fill=X)
    name_label.after(2000, lambda: dis_show(name_label, button))
