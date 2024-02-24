import time
from tkinter import PhotoImage
from typing import Optional
from bin.configLoader import Config

def ease_out(t, b, c, d):
    """
    缓动函数
    t: 当前时间
    b: 初始值
    c: 变化量
    d: 总时间
    """
    t = t / d - 1
    return c * (t * t * t + 1) + b


def linear_out(c, i, d):
    """
    线性函数
    c: 变化量
    i: 间隔时间
    d: 总时间
    """
    return c / (d / i)
def nonlinear_animation(sub, tim=500, tax=100, img: Optional[PhotoImage] = None):
    start_x = int(sub.winfo_x())
    while start_x <= 0 and img:
        time.sleep(0.02)
        start_x = int(sub.winfo_x())
    duration = tim  # 持续时间（毫秒）

    def animate(t):
        nonlocal start_x

        if t < duration:
            new_x = ease_out(t, start_x, tax, duration)
            sub.place(x=new_x)
            if img is not None:
                sub.configure(image=img)
                sub.image = img
            sub.after(10, animate, t + 10)
        else:
            sub.place(x=start_x + tax)  # 确保最终位置准确

    animate(0)

def linear_animation(sub, tim=500, tax=100, img: Optional[PhotoImage] = None):
    duration = tim  # 持续时间（毫秒）
    dx = linear_out(tax, 10, duration)

    def animate(t):
        nonlocal dx

        if t < duration:
            new_x = sub.winfo_x() + dx
            sub.place(x=new_x)
            if img is not None:
                sub.configure(image=img)
                sub.image = img
            sub.after(10, animate, t + 10)

    animate(0)

def animation(cfg: Config, sub, tim=500, tax=100, img: Optional[PhotoImage] = None):
    if cfg.end_page.animation:
        if cfg.end_page.no_liner:
            nonlinear_animation(sub, tim, tax, img)
        else:
            linear_animation(sub, tim, tax, img)
