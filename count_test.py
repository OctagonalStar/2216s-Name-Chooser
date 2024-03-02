import bin.configLoader as configLoader
from collections import Counter
import random, time, os
import numpy as np
class Random(object):
    def __init__(self, cfg: configLoader.Config):
        self.config = cfg
        self.__repeat = []
        self.force_seed = None
        if self.config.debug.enabled and self.config.debug.seed:
            self.force_seed = self.config.debug.seed

    def choice(self, names: list):
        if self.config.random.delete_repeat or self.config.random.decrease_repeat:
            self.flash_repeat(names)
        elif self.force_seed:
            random.seed(self.force_seed)
        name = random.choice(names)
        if self.config.random.delete_repeat and name in self.__repeat:
            temp_name = {}
            for name in names:
                temp_name[name] = name
            temp = list(set(temp_name).difference(self.__repeat))
            name = temp_name[random.choice(temp)]
        if self.config.random.decrease_repeat and name in self.__repeat:
            for _ in range(self.__repeat.count(name)):
                temp = random.choice(names)
                if temp not in self.__repeat:
                    name = temp
                    break
        self.__repeat.append(name)
        return name

    def flash_repeat(self, names: list):
        temp = []
        for x in names:
            temp.append(x)
        if not set(self.__repeat).symmetric_difference(set(temp)):
            for name in temp:
                self.__repeat.remove(name)


config = configLoader.load_config()
rand = Random(config)
print("配置加载完成")
print("名单总人数: %s" % str(len(config.name_list.list)))
gold = 0
for x in config.name_list.list:
    if x["gold"] and isinstance(x["gold"], bool):
        gold += 1
    elif isinstance(x["gold"], int):
        if x["gold"] >= 5:
            gold += 1
print("五星(以上)人数为: %i\t\t理论出金概率为: %.4f" % (gold, gold / len(config.name_list.list)))
name_temp = []
gold_temp = []
names = []
gold_list = []
for x in config.name_list.list:
    names.append(x["name"])
    if x["gold"] and isinstance(x["gold"], bool):
        gold_list.append(True)
        continue
    elif isinstance(x["gold"], int):
        if x["gold"] >= 5:
            gold_list.append(True)
            continue
    gold_list.append(False)

for _ in range(1, 100001):
    i = rand.choice(list(range(len(config.name_list.list))))
    name_temp.append(names[i])
    gold_temp.append(gold_list[i])
    print("\r十万次随机进度: %i/100000\t\t出金率:%f" % (_, gold_temp.count(True) / _), end="")
print("\n此次随机的名称重复排列:")
count_dict = Counter(name_temp)
counts = list(count_dict.values())
sorted_dict = dict(sorted(count_dict.items(), key=lambda x: x[1], reverse=True))
for x in sorted_dict.keys():
    if len(x) >= 4:
        print("%s\t%i" % (x, sorted_dict[x]))
    else:
        print("%s\t\t%i" % (x, sorted_dict[x]))
variance = np.var(counts)
print("综合方差为: %f" % variance)
