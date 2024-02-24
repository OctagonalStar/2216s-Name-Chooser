from tkinter import *
import threading
from typing import Optional
from bin.configLoader import Config


class SideLoad(object):
    def __init__(self, cfg: Config, random, call: callable, call2: Optional[callable] = None) -> None:
        self.thread = None
        self.random = random
        self.side = cfg.side_load.side
        self.call = call
        self.config = cfg
        self._timer = None
        if call2:
            self.call2 = call2
        else:
            self.call2 = print
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.4)
        if self.config.side_load.side == "left":
            self.pos = (self.config.side_load.wide, self.config.side_load.high, 0, (self.root.winfo_screenheight() -
                                                                                    self.config.side_load.high) / 2)
        else:
            self.pos = (self.config.side_load.wide, self.config.side_load.high, self.root.winfo_screenwidth() -
                        self.config.side_load.wide, (self.root.winfo_screenheight() - self.config.side_load.high) / 2)
        self.root.geometry("%ix%i+%i+%i" % self.pos)
        self.module_button = Button(self.root, text=self.config.side_load.button, font=self.config.side_load.font)
        self.module_button.bind("<ButtonRelease-1>", self.left)
        self.module_button.bind("<ButtonRelease-3>", self.right)
        self.module_button.pack(fill=X, expand=True)
        self.root.mainloop()

    def left(self, _):
        self.thread = threading.Thread(target=self.call, args=(self.module_button, self.root, self.config, self.random))
        self.thread.start()

    def right(self, _):
        self.thread = threading.Thread(target=self.call2,
                                       args=(self.module_button, self.root, self.config, self.random))
        self.thread.start()
