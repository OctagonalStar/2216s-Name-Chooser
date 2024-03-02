# [ZZ2Z2216班的简单点名程序](https://github.com/OctagonalStar/2216s-Name-Chooser)
## 已实现功能 Feature
#### 主程序(`main.py`)
- 侧栏加载
- 减少/抵消 重复可能
- 双重检查(`config.json`文件校验+硬编码校验)
- 名单防重复/相似
- 名单动态加载
- 动画视频
- 双击跳过动画
- 末页显示个性化
- 自动关闭窗口
- 多实例保护
- 字体个性化
#### 推算程序(`count_test.py`)
- 推算理论随机概率
- 十万次模拟计算波动方差
#### 文件保护程序(`file.py`)
- 服务端与客户端同构
- 基于FastAPI
- 保护特定文件夹内文件 防止删除及修改
#### 条件概率推算(`rate_predict.cpp`)
- 递归推算
- 动态规划

## 待办清单 TODO List
- 在末页支持以视频展示

## 其他
如需详细了解请参照各个子程序的单独介绍 链接如下

[main.py](docs/main.md)

[count_test.py](docs/count_test.md)

[file.py](docs/file.md)

[rate_predict.cpp](docs/rate_predict.md)

[漏洞日志](docs/BugLog.md)