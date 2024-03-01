from tkinter import *
import threading
from typing import Optional
from bin.configLoader import Config
import multiprocessing

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
        if self.config.test_features.multi_process:
            self.processes_pool = multiprocessing.Pool(processes=4)
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
        if self.config.test_features.multi_process:
            chosen = self.random.choice(self.config.name_list.list)
            cfg = {
                "animation": {
                        "enabled": self.config.animation.enabled,
                        "delayPauseCheck": self.config.animation.delay_pause_check,
                        "video": self.config.animation.gold_video if chosen["gold"] and self.config.animation.diff
                        else self.config.animation.purple_video,
                        "doubleClickSkip": self.config.animation.double_click_skip
                    },
                "endPage": {
                    "showInto": self.config.end_page.show_into,
                    "showPic": self.config.end_page.show_pic,
                    "animation": self.config.end_page.animation,
                    "noLiner": self.config.end_page.no_liner,
                    "font1": self.config.end_page.font1,
                    "font2": self.config.end_page.font2,
                    "font3": self.config.end_page.font3,
                    "defaultPic": self.config.end_page.default_pic,
                    "closeTime": self.config.end_page.close_time,
                    "backgroundColor": self.config.end_page.background_color,
                    "backgroundImg": self.config.end_page.background_img
                },
                "testFeatures": {
                    "multi-starEnable": self.config.test_features.multi_star_enable,
                    "globalNotification": {
                        "enabled": self.config.test_features.global_notification.enabled,
                        "message": self.config.test_features.global_notification.message
                    }
                }
            }
            process = multiprocessing.Process(target=self.call, args=(chosen, cfg))
            process.start()
            process.join()
        else:
            self.thread = threading.Thread(target=self.call,
                                           args=(self.module_button, self.root, self.config, self.random))
            self.thread.start()

    def right(self, _):
        self.thread = threading.Thread(target=self.call2,
                                       args=(self.module_button, self.root, self.config, self.random))
        self.thread.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
