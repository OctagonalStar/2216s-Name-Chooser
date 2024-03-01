import ctypes
import os
import multiprocessing
import requests
import fastapi
import uvicorn
import sys
import win32api
import win32com.client
import datetime
from pydantic import BaseModel
import random
import time

root_path = os.getcwd()
sys.path.append(root_path)

app = fastapi.FastAPI()
locked = False
processes = []


class Password(BaseModel):
    password: int


class Path(BaseModel):
    path: str


@app.get("/")
async def alive():
    return {"alive": True, "locked": locked}


@app.post("/unlock")
async def unlock(password: Password):
    if password.password == int(datetime.datetime.now().strftime("%H")) + 72:
        global locked, processes
        locked = False
        for process in processes:
            if process.is_alive():
                process.terminate()
        return {"unlock": True}
    else:
        return {"unlock": False}


@app.post("/lock/")
def lock(path: Path):
    print(0)
    global locked
    print(path.path)
    if locked:
        return {"lock": True}
    else:
        global processes
        path = path.path
        locked = True
        if os.path.isdir(path):
            files = os.listdir(path)
            processes = []
            for file in files:
                if os.path.isfile(path + "/" + file):
                    processes.append(multiprocessing.Process(target=occupy,
                                                             name="Intel(R) FileManager %i" % random.randint(0, 999999),
                                                             args=(path + "/" + file,), daemon=True))
            for process in processes:
                process.start()
        else:
            processes = [multiprocessing.Process(target=occupy,
                                                 name="Intel(R) FileManager %i" % random.randint(0, 999999),
                                                 args=(path,), daemon=True)]
            for process in processes:
                process.start()
        return {"lock": True}


def occupy(path: str, **kwargs):
    ctypes.windll.kernel32.SetConsoleTitleW("Intel(R) FileManager")
    for args in kwargs:
        print(args)
    if os.path.exists(path) and os.path.isfile(path):
        with open(path, "rb") as f:
            while True:
                try:
                    f.read(1)
                except:
                    break
                time.sleep(0.01)


def locks():
    name_app = os.path.basename(__file__)[0:-3]  # Get the name of the script
    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {
            "file_handler": {
                "class": "logging.FileHandler",
                "filename": "logfile.log",
            },
        },
        "root": {
            "handlers": ["file_handler"],
            "level": "INFO",
        },
    }
    uvicorn.run(f'{name_app}:app', port=8011, log_config=log_config)


if __name__ == "__main__":
    multiprocessing.freeze_support()


    def launch():
        print("尝试链接至锁定服务")
        try:
            press = requests.get("http://127.0.0.1:8011/")
            if press.status_code == 200:
                if press.json()["locked"]:
                    print("锁定服务已启动 锁定已开启")
                else:
                    press = requests.post("http://127.0.0.1:8011/lock/", json={"path": "res\\pic"})
                    if press.status_code == 200:
                        print("锁定服务已启动 锁定已启用")
                    else:
                        print("锁定服务启动异常 服务器返回 %i" % press.status_code)
        except:
            print("链接锁定服务失败 尝试重启")
            win32api.ShellExecute(0, 'open', 'file.exe', 'up', os.getcwd(), 0)
            while True:
                time.sleep(2)
                try:
                    press = requests.post("http://127.0.0.1:8011/lock/", json={"path": "res\\pic"})
                    if press.status_code == 200:
                        print("锁定服务已启动")
                        break
                except (ConnectionError, WindowsError):
                    print("等待服务启动")
                    time.sleep(1)


    if len(sys.argv) < 2:
        launch()
    elif sys.argv[1] == "lock":
        launch()
    elif sys.argv[1] == "unlock":
        print("尝试链接至锁定服务")
        try:
            res = requests.get("http://127.0.0.1:8011/")
            if res.status_code == 200:
                print("锁定服务链接成功")
            if not res.json()["locked"]:
                print("锁定服务尚未启用")
        except:
            print("链接锁定服务失败")
        else:
            if res.status_code == 200 and res.json()["locked"]:
                print("尝试进行身份验证")
                wmiService = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer('.', 'root\\cimv2')
                devices = wmiService.ExecQuery("SELECT * FROM Win32_PnPEntity")
                allow = False
                for device in devices:
                    if "USB\\VID_0C76&PID_2131" in device.DeviceID:
                        allow = True
                if not allow:
                    print("硬件密钥ID 验证失败")
                    pwd = input("请输入动态密钥:")
                    if int(pwd) != int(datetime.datetime.now().strftime("%H%M")) + 7:
                        print("动态密钥 验证失败")
                    else:
                        allow = True
                        print("动态密钥 验证成功")
                else:
                    print("硬件密钥ID 验证成功")
                if allow:
                    print("正在计算即时解锁密钥")
                    print("正在向解锁服务发送请求")
                    res = requests.post("http://127.0.0.1:8011/unlock",
                                        json={"password": int(int(datetime.datetime.now().strftime("%H")) + 72)})
                    if res.status_code == 200:
                        if res.json()["unlock"]:
                            print("解锁成功")
                        else:
                            print("解锁失败")
                    else:
                        print("解锁服务返回状态码:%s" % res.status_code)
    elif sys.argv[1] == "up":
        locks()
