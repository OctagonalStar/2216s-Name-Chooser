import bin.configLoader as configLoader
import bin.randomName as randomName
import bin.select as select
import bin.sideLoad as sideLoad
import multiprocessing
import socket

def launch(cfg: configLoader.Config):
    if cfg.global_set.default_mode == "sideLoad":
        if cfg.test_features.multi_process:
            sideLoad.SideLoad(cfg=cfg, call=select.process_func, call2=select.on_board, random=rand)
        else:
            sideLoad.SideLoad(cfg=cfg, call=select.func, call2=select.on_board, random=rand)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    config = configLoader.load_config()
    rand = randomName.Random(config)
    if config.global_set.multi_instance_prevent:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", 14785))
            launch(cfg=config)
        except WindowsError:
            configLoader.MessageBox(0, "请勿开启多个实例", "错误", configLoader.MB_OK)
    else:
        launch(cfg=config)
