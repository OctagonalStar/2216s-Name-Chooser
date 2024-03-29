from multiprocessing import freeze_support
from tkinter import *
from tkVideoPlayer import TkinterVideo


def video_play(_root, _file_path):
    videoplayer = TkinterVideo(master=_root)
    videoplayer.load(_file_path)
    videoplayer.place(x=0, y=0, relwidth=1, relheight=1)
    videoplayer.play()
    return videoplayer


if __name__ == "__main__":
    freeze_support()
    root = Tk()
    root.geometry("1280x720+%i+%i" % ((root.winfo_screenwidth() - 1280)/2, (root.winfo_screenheight() - 720)/2))
    file_path = "../res/gold.mp4"
    vp = video_play(root, file_path)
    root.after(8000, lambda: print(vp.is_paused()))
    root.mainloop()
