import os
import json
import logging

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
		return defaultConfig
	with open("config.json", "r") as f:
		file_config = json.loads(f.read())
	if "nameList" not in file_config:
		with open("config.json", "w") as f:
			f.write(json.dumps(defaultConfig))
		return defaultConfig
	with open(file_config["nameList"], "r", encoding="utf-8") as f:
		names = f.read()
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


if __name__ == "__main__":
	config = load_config()
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG if config["debug"] else logging.INFO)
	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG if config["debug"] else logging.INFO)
	fh = logging.FileHandler(filename=config["log"])
	fh.setLevel(logging.DEBUG)
	fmt = logging.Formatter(fmt="%(asctime)s {%(name)s} [%(levelname)-9s] %(filename)-8s - %(message)s",
	                        datefmt="%Y/%m/%d %H:%M:%S")
	sh.setFormatter(fmt)
	fh.setFormatter(fmt)
	logger.addHandler(sh)
	logger.addHandler(fh)
	logging.critical("You Shouldn't Run This File")
