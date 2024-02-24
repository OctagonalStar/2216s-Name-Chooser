import bin.configLoader as configLoader
import bin.randomName as randomName
import bin.select as select
import bin.sideLoad as sideLoad
import socket

config = configLoader.load_config()
rand = randomName.Random(config)

if __name__ == "__main__":
    if config.global_set.multi_instance_prevent:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", 14785))
            if config.global_set.default_mode == "sideLoad":
                load = sideLoad.SideLoad(cfg=config, call=select.func, call2=select.on_board, random=rand)
        except WindowsError:
            configLoader.MessageBox(0, "请勿开启多个实例", "错误", configLoader.MB_OK)
