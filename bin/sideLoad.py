from tkinter import *
import threading
import logging
import os
import tkinter.font
from typing import Optional

# 检查log文件夹是否存在
if not os.path.exists("log"):
    os.mkdir("log")
if not os.path.exists("log\\log.log"):
    with open("log\\log.log", "w") as f:
        f.write("")


class SideLoad(object):
    def __init__(self, side: str, call: callable, call2: Optional[callable] = None, **kwargs) -> None:
        self.thread = None
        self.side = side
        self.call = call
        self._timer = False

        if "wide" in kwargs:
            self.wide = kwargs["wide"]
        else:
            self.wide = 50
        if "high" in kwargs:
            self.high = kwargs["high"]
        else:
            self.high = 150
        if "button" in kwargs:
            button = kwargs["button"]
        else:
            button = "Run"
        if "font" in kwargs:
            self.font = kwargs["font"]
        else:
            self.font = ("微软雅黑", 20, tkinter.font.BOLD)
        if call2:
            self.call2 = call2
        else:
            self.call2 = print
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.4)
        self.button = button
        if side == "left":
            self.pos = (self.wide, self.high, 0, (self.root.winfo_screenheight() - self.high) / 2)
        elif side == "right":
            self.pos = (self.wide, self.high, self.root.winfo_screenwidth() - self.wide,
                        (self.root.winfo_screenheight() - self.high) / 2)
        else:
            logging.warning("side must be 'left' or 'right', default to 'right'")
            self.pos = (self.wide, self.high, self.root.winfo_screenwidth() - self.wide,
                        (self.root.winfo_screenheight() - self.high) / 2)
        self.root.geometry("%ix%i+%i+%i" % self.pos)
        self.module_button = Button(self.root, text=self.button, font=self.font)
        self.module_button.bind("<Button-1>", self._on_push)
        self.module_button.bind("<ButtonRelease-1>", self._on_release)
        self.module_button.pack(fill=X, expand=True)
        logging.info("Start up SideLoad UI successfully")
        self.root.mainloop()

    def run_module(self):
        logging.info("Start call %s module" % self.call.__name__)
        self.thread = threading.Thread(target=self.call, args=(self.module_button, self.root))
        self.thread.start()

    def _on_push(self, event):
        if not self._timer:
            self._timer = self.module_button.after(500, self._long_press)

    def _on_release(self, event):
        if self._timer:
            self.run_module()
            self.module_button.after_cancel(self._timer)
            self._timer = None

    def _long_press(self):
        logging.info("Start call2 %s module" % self.call2.__name__)
        self.thread = threading.Thread(target=self.call2, args=(self.module_button, self.root))
        self.thread.start()
        self.module_button.after_cancel(self._timer)
        self._timer = None


if __name__ == '__main__':
    debugMode = True
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG if debugMode else logging.INFO)
    fh = logging.FileHandler(filename="log\\log.log")
    fh.setLevel(logging.DEBUG)
    fmt = logging.Formatter(fmt="%(asctime)s {%(name)s} [%(levelname)-9s] %(filename)-8s - %(message)s",
                            datefmt="%Y/%m/%d %H:%M:%S")
    sh.setFormatter(fmt)
    fh.setFormatter(fmt)
    logger.addHandler(sh)
    logger.addHandler(fh)
    SideLoad("right", lambda: print("hello world"))
