import random
import os
from bin.configLoader import Config
import time

class Random(object):
    def __init__(self, cfg: Config):
        self.config = cfg
        self.__repeat = []
        self.force_seed = None
        if self.config.debug.enabled and self.config.debug.seed:
            self.force_seed = self.config.debug.seed

    def choice(self, names: list):
        seed = 0
        if self.config.random.delete_repeat or self.config.random.decrease_repeat:
            self.flash_repeat(names)
        if self.config.random.optimize_random and not self.force_seed:
            seed = time.time_ns() / 86321454537
            seed *= 2
            seed += os.getpid()
            seed -= ord(random.choice(names)["name"][1])
            random.seed(int(seed))
        elif self.force_seed:
            random.seed(self.force_seed)
        name = random.choice(names)
        if self.config.random.delete_repeat and name["name"] in self.__repeat:
            if self.config.debug.enabled:
                print("重复删除")
            temp_name = {}
            for name in names:
                temp_name[name["name"]] = name
            temp = list(set(temp_name).difference(self.__repeat))
            if self.config.random.optimize_random and not self.force_seed:
                random.seed(seed+1)
            name = temp_name[random.choice(temp)]
        if self.config.random.decrease_repeat and name["name"] in self.__repeat:
            if self.config.debug.enabled:
                print("重复重抽")
            for _ in range(self.__repeat.count(name["name"])):
                if self.config.random.optimize_random and not self.force_seed:
                    seed += 1
                    random.seed(seed)
                temp = random.choice(names)
                if self.config.debug.enabled:
                    print(f"重抽结果{str(_)}: {str(temp)}")
                if temp["name"] not in self.__repeat:
                    if self.config.debug.enabled:
                        print("重抽结果有效")
                    name = temp
                    break
                if self.config.debug.enabled:
                    print("重抽结果无效")
        self.__repeat.append(name["name"])
        return name

    def flash_repeat(self, names: list):
        temp = []
        if self.config.debug.enabled:
            print(self.__repeat)
        for x in names:
            temp.append(x["name"])
        if self.config.debug.enabled:
            print(set(self.__repeat).symmetric_difference(set(temp)))
        if not set(self.__repeat).symmetric_difference(set(temp)):
            for name in temp:
                self.__repeat.remove(name)

