import os
import json
from win32api import MessageBox
from win32con import MB_OK

hardCodeNameList = []
defaultConfig = {
    "debug": {
        "enabled": False,
        "seed": None
    },
    "sideLoad": {
        "wide": 50,
        "high": 100,
        "side": "right",
        "button": "点\n名",
        "font": ("微软雅黑", 20, "bold")
    },
    "nameList": {
        "path": None,
        "preventDuplication": True,
        "preventSimilarities": {
            "enabled": True,
            "threshold": 0.8
        },
        "doubleCheck": {
            "enabled": True,
            "trict": False,
            "info": True,
            "nameList": []
        },
        "hardCodeCheck": {
            "enabled": False,
            "trict": False,
            "info": True
        },
        "dynamicLoad": True
    },
    "animation": {
        "enabled": True,
        "diff": True,
        "diffSymbol": "|",
        "delayPauseCheck": 3,
        "goldVideo": None,
        "purpleVideo": None,
        "doubleClickSkip": True
    },
    "endPage": {
        "showInto": True,
        "showPic": True,
        "animation": True,
        "noLiner": True,
        "font1": ("微软雅黑", 50, "bold"),
        "font2": ("微软雅黑", 20, "bold"),
        "font3": ("微软雅黑", 17, "bold"),
        "defaultPic": None,
        "closeTime": 6,
        "backgroundColor": "#272733",
        "backgroundImg": None
    },
    "random": {
        "optimizeRandom": False,
        "decreaseRepeat": True,
        "deleteRepeat": False
    },
    "global": {
        "multi-instancePrevent": True,
        "defaultMode": "sideLoad"
    },
    "testFeatures": {
        "jpgSupport": False,
        "multi-starEnable": False,
        "globalNotification": {
            "enabled": False,
            "message": None,
        }
    }
}


def extract(val: str, cfg, default=None):
    if cfg and val in cfg.keys():
        return cfg[val]
    return default


class Config(object):
    class __Debug(object):
        def __init__(self, cfg):
            debug_cfg = extract("debug", cfg)
            self.enabled = extract("enabled", debug_cfg, defaultConfig["debug"]["enabled"])
            self.seed = extract("seed", debug_cfg, defaultConfig["debug"]["seed"])

    class __SideLoad(object):
        def __init__(self, cfg):
            side_load_cfg = extract("sideLoad", cfg)
            self.wide = extract("wide", side_load_cfg, defaultConfig["sideLoad"]["wide"])
            self.high = extract("high", side_load_cfg, defaultConfig["sideLoad"]["high"])
            self.side = extract("side", side_load_cfg, defaultConfig["sideLoad"]["side"])
            self.button = extract("button", side_load_cfg, defaultConfig["sideLoad"]["button"])
            self.font = extract("font", side_load_cfg, defaultConfig["sideLoad"]["font"])

    class __NameList(object):
        class DoubleCheck(object):
            def __init__(self, cfg):
                double_check_cfg = extract("doubleCheck", cfg,
                                           defaultConfig["nameList"]["doubleCheck"])
                self.enabled = extract("enabled", double_check_cfg,
                                       defaultConfig["nameList"]["doubleCheck"]["enabled"])
                self.trict = extract("trict", double_check_cfg,
                                     defaultConfig["nameList"]["doubleCheck"]["trict"])
                self.info = extract("info", double_check_cfg,
                                    defaultConfig["nameList"]["doubleCheck"]["info"])
                self.name_list = extract("nameList", double_check_cfg,
                                         defaultConfig["nameList"]["doubleCheck"]["nameList"])

        class HardCodeCheck(object):
            def __init__(self, cfg):
                hard_code_check_cfg = extract("hardCodeCheck", cfg,
                                              defaultConfig["nameList"]["hardCodeCheck"])
                self.enabled = extract("enabled", hard_code_check_cfg,
                                       defaultConfig["nameList"]["hardCodeCheck"]["enabled"])
                self.trict = extract("trict", hard_code_check_cfg,
                                     defaultConfig["nameList"]["hardCodeCheck"]["trict"])
                self.info = extract("info", hard_code_check_cfg,
                                    defaultConfig["nameList"]["hardCodeCheck"]["info"])

        class PreventSimilarities(object):
            def __init__(self, cfg):
                prevent_similarities_cfg = extract("preventSimilarities", cfg,
                                                   defaultConfig["nameList"]["preventSimilarities"])
                self.enabled = extract("enabled", prevent_similarities_cfg,
                                       defaultConfig["nameList"]["preventSimilarities"]["enabled"])
                self.threshold = extract("threshold", prevent_similarities_cfg,
                                         defaultConfig["nameList"]["preventSimilarities"]["threshold"])

        def __init__(self, cfg):
            name_list_cfg = extract("nameList", cfg)
            self.path = extract("path", name_list_cfg)  # 名单是必要参数
            if not self.path:
                raise KeyError("nameList path is required")
            self.prevent_duplication = extract("preventDuplication", name_list_cfg,
                                               defaultConfig["nameList"]["preventDuplication"])
            self.dynamic_load = extract("dynamicLoad", name_list_cfg,
                                        defaultConfig["nameList"]["dynamicLoad"])
            self.prevent_similarities = self.PreventSimilarities(name_list_cfg)
            self.double_check = self.DoubleCheck(name_list_cfg)
            self.hard_code_check = self.HardCodeCheck(name_list_cfg)
            self.list = []

    class __Animation(object):
        def __init__(self, cfg):
            animation_cfg = extract("animation", cfg)
            self.enabled = extract("enabled", animation_cfg,
                                   defaultConfig["animation"]["enabled"])
            self.diff = extract("diff", animation_cfg, defaultConfig["animation"]["diff"])
            self.diff_symbol = extract("diffSymbol", animation_cfg,
                                       defaultConfig["animation"]["diffSymbol"])
            self.delay_pause_check = extract("delayPauseCheck", animation_cfg,
                                             defaultConfig["animation"]["delayPauseCheck"])
            self.gold_video = extract("goldVideo", animation_cfg,
                                      defaultConfig["animation"]["goldVideo"])
            self.purple_video = extract("purpleVideo", animation_cfg,
                                        defaultConfig["animation"]["purpleVideo"])
            self.double_click_skip = extract("doubleClickSkip", animation_cfg,
                                             defaultConfig["animation"]["doubleClickSkip"])

    class __EndPage(object):
        def __init__(self, cfg):
            end_page_cfg = extract("endPage", cfg)
            self.show_into = extract("showInto", end_page_cfg,
                                     defaultConfig["endPage"]["showInto"])
            self.show_pic = extract("showPic", end_page_cfg,
                                    defaultConfig["endPage"]["showPic"])
            self.animation = extract("animation", end_page_cfg,
                                     defaultConfig["endPage"]["animation"])
            self.no_liner = extract("noLiner", end_page_cfg,
                                    defaultConfig["endPage"]["noLiner"])
            self.font1 = extract("font1", end_page_cfg, defaultConfig["endPage"]["font1"])
            self.font2 = extract("font2", end_page_cfg, defaultConfig["endPage"]["font2"])
            self.font3 = extract("font3", end_page_cfg, defaultConfig["endPage"]["font3"])
            self.default_pic = extract("defaultPic", end_page_cfg,
                                       defaultConfig["endPage"]["defaultPic"])
            self.close_time = extract("closeTime", end_page_cfg,
                                      defaultConfig["endPage"]["closeTime"])
            self.background_color = extract("backgroundColor", end_page_cfg,
                                            defaultConfig["endPage"]["backgroundColor"])
            self.background_img = extract("backgroundImg", end_page_cfg,
                                          defaultConfig["endPage"]["backgroundImg"])

    class __Random(object):
        def __init__(self, cfg):
            random_cfg = extract("random", cfg)
            self.optimize_random = extract("optimizeRandom", random_cfg,
                                           defaultConfig["random"]["optimizeRandom"])
            self.decrease_repeat = extract("decreaseRepeat", random_cfg,
                                           defaultConfig["random"]["decreaseRepeat"])
            self.delete_repeat = extract("deleteRepeat", random_cfg,
                                         defaultConfig["random"]["deleteRepeat"])

    class __Global(object):
        def __init__(self, cfg):
            global_cfg = extract("global", cfg)
            self.default_mode = extract("defaultMode", global_cfg,
                                        defaultConfig["global"]["defaultMode"])
            self.multi_instance_prevent = extract("multi-instancePrevent", global_cfg,
                                                  defaultConfig["global"]["multi-instancePrevent"])

    class __TestFeatures(object):
        class GlobalNotification(object):
            def __init__(self, cfg):
                global_notification_cfg = extract("globalNotification", cfg)
                self.enabled = extract("enabled", global_notification_cfg,
                                       defaultConfig["testFeatures"]["globalNotification"]["enabled"])
                self.message = extract("message", global_notification_cfg,
                                       defaultConfig["testFeatures"]["globalNotification"]["message"])

        def __init__(self, cfg):
            test_features_cfg = extract("testFeatures", cfg)
            self.jpg_support = extract("jpgSupport", test_features_cfg,
                                       defaultConfig["testFeatures"]["jpgSupport"])
            self.multi_star_enable = extract("multi-starEnable", test_features_cfg,
                                             defaultConfig["testFeatures"]["multi-starEnable"])
            self.global_notification = self.GlobalNotification(test_features_cfg)

    def __init__(self, cfg):
        self.debug = self.__Debug(cfg)
        self.side_load = self.__SideLoad(cfg)
        self.name_list = self.__NameList(cfg)
        self.animation = self.__Animation(cfg)
        self.end_page = self.__EndPage(cfg)
        self.random = self.__Random(cfg)
        self.global_set = self.__Global(cfg)
        self.test_features = self.__TestFeatures(cfg)


def load_name_list(cfg: Config) -> None:
    """
    :param cfg: Config类
    列表格式为 [{"gold": bool, "name": str, "nick": str, "into": str}]
    名单格式为 [diffSymbol]name$nick$into
    into中;代表\n
    """
    name_list = []
    name_cache = []
    with open(cfg.name_list.path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                line = line.replace("\n", "")
                line = line.split("\\")
                if not cfg.test_features.multi_star_enable:
                    gold = True if line[0][0] == cfg.animation.diff_symbol else False
                    if gold:
                        name = line[0][1:]
                    else:
                        name = line[0]
                else:
                    gold = 4
                    while line[0][0] == cfg.animation.diff_symbol:
                        gold += 1
                        line[0] = line[0][1:]
                    name = line[0]
                if name in name_cache and cfg.name_list.prevent_duplication:
                    continue
                name_cache.append(name)
                into = "这个人很神秘 什么都没有写"
                if len(line) == 3:
                    if line[2]:
                        into = line[2].replace(";", "\n")
                    name_list.append({"gold": gold, "name": name, "nick": line[1], "into": into})
                elif len(line) == 2:
                    name_list.append({"gold": gold, "name": name, "nick": line[1], "into": into})
    cfg.name_list.list = name_list


def check_name_list(cfg: Config) -> None:
    # 双检
    if cfg.name_list.double_check.enabled:
        temp = list(cfg.name_list.double_check.name_list)
        rm_list = []
        for name in cfg.name_list.list:
            if name["name"] not in cfg.name_list.double_check.name_list:
                if cfg.name_list.double_check.info:
                    MessageBox(0, f"双检错误\n{name['name']} 在名单中多余"
                                  f"\n已自动去除" if not cfg.name_list.double_check.trict else f"双检错误\n{name['name']} 在名单中多余 请重新检查名单或关闭严格模式",
                               "DC错误", MB_OK)
                if cfg.name_list.double_check.trict:
                    raise KeyError("Found name more than DCnameList during double check")
                rm_list.append(name)
            else:
                temp.remove(name["name"])
        for name in rm_list:
            cfg.name_list.list.remove(name)
        if temp:
            if cfg.name_list.double_check.info:
                MessageBox(0,
                           f"双检错误\n以下名称不存在于名单中\n{str(temp)}\n已自动加入" if not cfg.name_list.double_check.trict else f"双检错误\n以下名称不存在于名单中\n{str(temp)}\n请重新检查名单或关闭严格模式",
                           "DC错误", MB_OK)
            if cfg.name_list.double_check.trict:
                raise KeyError("Found name not in DCnameList during double check")
            for name in temp:
                cfg.name_list.list.append({"gold": False, "name": name, "nick": name, "into": "这个人很神秘 "
                                                                                          "什么都没有写"})
    # 硬检
    if cfg.name_list.hard_code_check.enabled:
        global hardCodeNameList
        temp = list(hardCodeNameList)
        rm_list = []
        for name in cfg.name_list.list:
            if name["name"] not in hardCodeNameList:
                if cfg.name_list.hard_code_check.info:
                    MessageBox(0, f"硬编码检查错误\n{name['name']} 在名单中多余"
                                  f"\n已自动去除" if not cfg.name_list.hard_code_check.trict
                    else f"硬编码检查错误\n{name['name']} 在名单中多余 请重新检查名单或关闭严格模式","HC错误", MB_OK)
                if cfg.name_list.hard_code_check.trict:
                    raise KeyError("Found name more than HCnameList during double check")
                rm_list.append(name)
            else:
                temp.remove(name["name"])
        for name in rm_list:
            cfg.name_list.list.remove(name)
        if temp:
            if cfg.name_list.hard_code_check.info:
                MessageBox(0, f"硬编码检查错误\n以下名称不存在于名单中"
                              f"\n{str(temp)}\n已自动加入" if not cfg.name_list.hard_code_check.trict
                           else f"硬编码检查错误\n以下名称不存在于名单中\n{str(temp)}\n请重新检查名单或关闭严格模式",
                           "HC错误", MB_OK)
            if cfg.name_list.hard_code_check.trict:
                raise KeyError("Found name not in HCnameList during double check")
            for name in temp:
                cfg.name_list.list.append({"gold": False, "name": name, "nick": name, "into": "这个人很神秘 "
                                                                                              "什么都没有写"})


def load_config():
    if not os.path.exists("config.json"):
        with open("config.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(defaultConfig))
        return load_config()
    with open("config.json", "r", encoding="utf-8") as f:
        file_config = json.load(f)
    config = Config(file_config)
    load_name_list(config)
    check_name_list(config)
    return config
