from tkinter import PhotoImage
from typing import Optional


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


def move_right_animation(sub, tim=500, tarx=100, img: Optional[PhotoImage] = None):
    start_x = sub.winfo_x()
    duration = tim  # 持续时间（毫秒）

    def animate(t):
        nonlocal start_x

        if t < duration:
            new_x = ease_out(t, start_x, tarx, duration)
            sub.place(x=new_x)
            if img is not None:
                sub.configure(image=img)
                sub.image = img
            sub.after(10, animate, t + 10)
        else:
            sub.place(x=start_x + tarx)  # 确保最终位置准确

    animate(0)
