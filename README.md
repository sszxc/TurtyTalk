# TurtyTalk

- Ubuntu 18.04
- ROS melodic
- Python 2

使用百度语音识别、合成API以及百度UNIT理解交互平台，实现自然语言交互以及用户意图获取。

订阅topic Talk_Msg，收到“start”字符串时启动语音识别，开始对话。

意图获取完成后发布topic Listen_Msg，内容为“姓名 物品”格式的字符串。

![image](https://github.com/sszxc/TurtyTalk/blob/master/2020-04-09_17-03.png)

# Demo
使用`./quick-demo.sh`快速启动Demo，使用`rostopic pub /Talk_Msg std_msgs/String 'start'`手动启动对话。

> 收到消息：龟龟，帮我拿个东西  
> 回复消息：你想要拿什么东西  
> 收到消息：水杯。  
> 回复消息：你是谁  
> 收到消息：橘子。  
> 回复消息：明白你的意思了，马上帮你去拿。  
> 获取意图：许嘉禾 水杯  

Robot Perception & HRI 2020