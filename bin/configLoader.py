import os
import json
from win32api import MessageBox
from win32con import MB_OK
defaultConfig = {
	"debug": False,
	"log": "log\\log.log",
	"defaultMode": "sideLoad",
	"nameList": "res\\name.txt",
	"goldVideoPath": "res\\gold.mp4",
	"purpleVideoPath": "res\\purple.mp4",
	"font1": ("微软雅黑", 50, "bold"),
	"font2": ("微软雅黑", 20, "bold"),
	"font3": ("微软雅黑", 17, "bold"),
	"sideLoad": {
		"wide": 50,
		"high": 100,
		"side": "right",
		"button": "点\n名",
		"font": ("微软雅黑", 20, "bold"),
	}
}


def load_config():
	if not os.path.exists("config.json"):
		with open("config.json", "w") as f:
			f.write(json.dumps(defaultConfig))
		return load_config()
	try:
		with open("config.json", "r") as f:
			file_config = json.loads(f.read())
	except:
		with open("config.json", "w") as f:
			f.write(json.dumps(defaultConfig))
		return load_config()
	if "nameList" not in file_config:
		with open("config.json", "w") as f:
			f.write(json.dumps(defaultConfig))
		return load_config()
	try:
		with open(file_config["nameList"], "r", encoding="utf-8") as f:
			names = f.read()
	except FileNotFoundError:
		MessageBox(0,  "是哪个大聪明把名单给删了!?", "aaaa", MB_OK)
		raise FileNotFoundError
	names = names.split("\n")
	temp = []
	for x in range(len(names)):
		if names[x] != "" and names[x] != " " and names[x] not in temp:
			temp.append(names[x])
	file_config["nameList"] = temp
	return file_config

def save_config(config):
	with open("config.json", "w") as f:
		f.write(json.dumps(config))
