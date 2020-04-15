#启动ORB-SLAM2 demo
gnome-terminal -x bash -c "roscore;"
sleep 2
gnome-terminal -x bash -c "rosrun baidu_speech simple_speek.py;"
gnome-terminal -x bash -c "rosrun baidu_speech voice_node.py;"
gnome-terminal -x bash -c "rosrun baidu_unit node_talk_main.py;"
