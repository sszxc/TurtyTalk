#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 zaizhizhuang.  All rights reserved.
This program is free software; you can redistribute it and/or modify.
"""

import rospy
from std_msgs.msg import String

import urllib
import urllib2
import sys
import ssl
import json
import requests

import signal

from pprint import pprint

class baidu_unit_talk_main():
    def __init__(self):
        self.define()

        rospy.Subscriber(self.token_topic, String, self.set_token)
        # wait for token...
        # while not self.access_token:
        #     rospy.logwarn('get token Retrying ...')
        #     rospy.sleep(1.0)
        #     self.access_token = rospy.get_param('/baidu_unit_token_string', '')
        
        # token 创建于Apr.6th, 2020 30天有效
        self.access_token = u'24.6d482d2ecddbf2192db1ef190234270d.2592000.1588754708.282335-19273548'
        rospy.loginfo("load token cache")

        # listen topic
        rospy.Subscriber(self.listen_topic, String, self.get_say)
        rospy.loginfo("wait for user")
        
        # self.load("今天北京天气怎么样？")
        rospy.spin()

    def get_say(self, data):
        self.load(data.data)

    def load(self, data):

        # url = 'https://aip.baidubce.com/rpc/2.0/solution/v1/unit_utterance?access_token=' + self.access_token
        # post_data = "{\"scene_id\":" + str(self.scene_id) + ",\
        #             \"query\":\""+str(data)+"\",\
        #             \"session_id\":\""+str(self.session_id)+"\"}"
        rospy.loginfo("收到消息：" + str(data))
                
        url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + self.access_token
        log_id = '7258521'  # 真实应用中自己生成，可是递增的数字，每轮请求需要一个id
        user_id = '234333'  # 真实应用中为用户分配的ID、设备号、ip地址等，方便在日志分析中分析定位问题
        bot_id = '1023448'  # 技能ID
        # post_data = '{\"session_id\":\"' + str(self.session_id) + '\",\
        #             \"log_id\":\"' + log_id + '\",\
        #             \"request\":{\"bernard_level\":1,\
        #                 \"client_session\":\"{\\\"client_results\\\":\\\"\\\", \\\"candidate_options\\\":[]}\",\
        #                 \"query\":\"' + str(data) + '\",\
        #                 \"query_info\":{\"asr_candidates\":[],\"source\":\"KEYBOARD\",\"type\":\"TEXT\"},\
        #                 \"updates\":\"\",\"user_id\":\"'+user_id+'\"},\
        #             \"bot_id\":'+bot_id+',\
        #             \"version\":\"2.0\"}'
        post_data = '{ "bot_session": "{\\"session_id\\":\\"' + str(self.session_id) + '\\"}",  "log_id": "' + log_id + '",  "request": {    "bernard_level": 1,    "query": "' + str(data) + '",     "query_info": {      "asr_candidates": [],      "source": "KEYBOARD",      "type": "TEXT"    },    "updates": "",    "user_id": "'+user_id+'"  },  "bot_id": "'+bot_id+'",  "version": "2.0"}'
        
        # print(post_data)
        request = urllib2.Request(url, post_data)
        request.add_header('Content-Type', 'application/Json_test;charset=UTF-8')
        # request.add_header('Content-Type', 'application/json; charset=UTF-8')#  原文
        #request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request)
        content = response.read()
        # if (content):
        #     print(content)
        #s = json.dumps(data)
        s1 = json.loads(content)
        # print(s1)        

        # unicode转json 获取session_id
        # if (s1[u"result"][u"bot_session"]):
            # self.session_id = s1[u"result"][u"bot_session"]
        if (self.session_id == ''):
            json_str = json.dumps(s1[u"result"][u"bot_session"])
            json_bot_session = json.loads(json_str).encode('utf-8')
            json_bot_session = json.loads(json_bot_session)
            self.session_id = json_bot_session[u"session_id"]
        if (s1[u"result"]['response'][u"action_list"][0][u"say"]):
            self.words = s1[u"result"]['response'][u"action_list"][0][u"say"]
            self.say.publish(self.words)
            rospy.loginfo("回复消息：" + self.words)        
        if (len(s1['result']['response']['schema']['slots']) == 2):  # 意图明确
            slots = s1['result']['response']['schema']['slots']
            ResultInfo = slots[0]['normalized_word'] + \
                " " + slots[1]['normalized_word']

            rospy.loginfo("获取意图：" + ResultInfo)

            self.sendResultInfo.publish(ResultInfo)  # 沟通结果发布
            self.LastWord.publish("stop")  # TTS最后一句
            self.session_id = ''

    def define(self):
        self.say = rospy.Publisher('speak_string', String, queue_size=1)
        self.sendResultInfo = rospy.Publisher(
            'Listen_Msg', String, queue_size=1)  # 沟通结果发布
        self.LastWord = rospy.Publisher(
            'TTS_LastWord', String, queue_size=1)  # TTS最后一句

        if not rospy.has_param('~baidu_unit_scene_id'):
            rospy.set_param('~baidu_unit_scene_id', '19273548')  # 加了一个ID
        if not rospy.has_param('~baidu_unit_token_topic'):
            rospy.set_param('~baidu_unit_token_topic',
                            'baidu_unit_token_string')
        if not rospy.has_param('~baidu_unit_listen_topic'):
            rospy.set_param('~baidu_unit_listen_topic',
                            'UNIT_Listen')
        # if not rospy.has_param('~baidu_unit_listen_topic'):
        #     rospy.set_param('~baidu_unit_listen_topic',
        #                     'baidu_unit_listen_string')

        self.token_topic = rospy.get_param('~baidu_unit_token_topic')
        self.listen_topic = rospy.get_param('~baidu_unit_listen_topic')
        self.scene_id = rospy.get_param('~baidu_unit_scene_id')
        self.access_token = ''
        self.session_id = ''


    def set_token(self, data):
        print(data)
        if data.data:
            self.access_token = data.data
        else:
            pass

def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit(0)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        # rospy.init_node('baidu_unit_talk')
        rospy.init_node('Baidu_UNIT')
        rospy.loginfo("initialization  baidu_unit talking")
        baidu_unit_talk_main()
        rospy.loginfo("process done and quit")
    except Exception, exc:
        print exc
