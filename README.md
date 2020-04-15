# TurtyTalk

- Ubuntu 18.04
- ROS melodic
- Python 2

使用百度语音识别、合成API以及百度UNIT理解交互平台，实现自然语言交互以及用户意图获取。

订阅topic Talk_Msg，收到“start”字符串时启动语音识别，开始对话。

意图获取完成后发布topic Listen_Msg，内容为“姓名 物品”格式的字符串。

![image](https://github.com/sszxc/TurtyTalk/blob/master/2020-04-09_17-03.png)

# 3rd party
安装requests模块
```
sudo pip install requests
```

安装两个Python库pyaudio和python-vlc
```
sudo apt-get install python-pip portaudio19-dev vlc libvlc-dev
sudo pip install pyaudio
sudo pip install python-vlc
```

# 对照字典
与物品识别对接，以下为物品的中英文对照Python字典。
```
Object_dict = {'水杯': 'cup', '餐巾纸': 'napkin', '肥皂': 'soap', '薯片': 'crisps', '可乐': 'cola', '拖鞋': 'slippers', '香水': 'floral_water', '方便面': 'instant_noodles', '冰红茶': 'iced_tea', '凉茶': 'herbal_tea'}
```

# Demo
使用`./quick-demo.sh`快速启动Demo，使用`rostopic pub /Talk_Msg std_msgs/String 'start'`手动启动对话。  
向`/speak_string`话题发送String单独调用TTS引擎，用于返回后汇报，例如使用`rostopic pub /speak_string std_msgs/String '这是你要的东西'`。
以下为三轮典型对话，分别是正常获取意图、重复澄清、整句获取。

> 发送消息：请问有什么可以帮你？  
> 正在录音...  
> 收到消息：帮我拿杯快乐水。  
> 回复消息：你叫什么名字  
> 正在录音...  
> 收到消息：我叫小明。  
> 获取意图：小明想要可乐。明白了，马上就去拿。  

> 发送消息：请问有什么可以帮你？  
> 正在录音...  
> 收到消息：龟龟，帮我拿个东西。  
> 回复消息：不好意思，需要我帮你拿什么  
> 正在录音...  
> 收到消息：水杯。  
> 回复消息：你叫什么名字  
> 正在录音...  
> 收到消息：张三。  
> 获取意图：张三想要水杯。明白了，马上就去拿。  

> 发送消息：请问有什么可以帮你？  
> 正在录音...  
> 收到消息：我是玛丽，帮我拿一包泡面。  
> 获取意图：玛丽想要方便面。明白了，马上就去拿。  


Robot Perception & HRI 2020
