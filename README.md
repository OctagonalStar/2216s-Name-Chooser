# 写给株洲市二中2216班的简单点名程序

---
## 使用方法
py或发行版直接运行是旁栏模式 在屏幕右方或左方(可在`config.json`中设置 详见config章节)
单击可唤出中心顶置窗口 播放视频后展示名字、个性签名与图片 6秒后自动关闭
长按可直接展示名字(直接在侧栏显示) 3秒后自动还原

其他的模式在以后会开发

---
## config 说明
默认设置
```
{  
	"debug": false,  
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
```
### debug
调试模式 目前无效
### log
日志路径 目前无效
### defaultMode
默认启动模式
### nameList
名单文件路径 可以用相对路径和绝对路径
### goldVideoPath
出金时播放的视频
### purpleVideoPath
出紫时播放的视频
### font1
中心显示名字时名字的字体
支持 `python.tkinter.font`  支持的元组类型
### font2
中心显示时个性签名的字体
支持 `python.tkinter.font`  支持的元组类型
### font3
侧边显示名字时名字的字体
支持 `python.tkinter.font`  支持的元组类型
### sideLoad
配置侧栏的样式
#### wide
侧边栏的宽度
#### high
侧边栏的高度
#### side
侧边栏的方位 支持`left`和`right`
#### button
按钮默认显示的文本
注：每个字都要间隔\\n 否则无法正常显示
#### font
按钮默认显示的文本的字体

---
## 名单格式
在名字前添加 `|` 表示为金
名字和个性签名间间隔一个空格
如
```
|张三 这是个性签名 允许空格
李四
```
其中
张三是金 个性签名为`这是个性签名 允许空格`
李四是紫 无个性签名 将显示为 `这个人很神秘 什么都没有写`