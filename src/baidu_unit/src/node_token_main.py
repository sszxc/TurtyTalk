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


class baidu_unit_token_main():
   def __init__(self):
      self.define()
      self.get_token()
      #rospy.Subscriber(self.topic , String , self.talker)
      rospy.spin()

   def get_token(self):
      # client_id 为官网获取的AK， client_secret 为官网获取的SK
      host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
         self.baidu_unit_ak+'&client_secret='+self.baidu_unit_sk
      request = urllib2.Request(host)
      request.add_header('Content-Type', 'application/json; charset=UTF-8')
      response = urllib2.urlopen(request)
      content = response.read()
      if (content):
         print(content)
         #s = json.dumps(data)
         s1 = json.loads(content)
         if (s1['access_token']):
               self.token_string = s1['access_token']
               print(self.token_string)
               rospy.set_param('baidu_unit_token_string', self.token_string)
               # 这边很奇怪 publish的数据输出失败
               self.say.publish('you are here')
               self.say.publish(self.token_string)
               # self.say.publish(self.token_string)
         else:
               print('get token error!!!')

   def define(self):
      self.say = rospy.Publisher(
         'baidu_unit_token_string', String, queue_size=1)
      if not rospy.has_param('~baidu_unit_ak'):
         rospy.set_param('~baidu_unit_ak',
                           'Grqo20E6GDTqrxGYHYxw3te4')  # 这边加了两个参数
      if not rospy.has_param('~baidu_unit_sk'):
         rospy.set_param('~baidu_unit_sk',
                           'ZPanrQQbL9eeCc8zDESXmIIBop8p5sf0')

      if not rospy.has_param('~baidu_unit_token_topic'):
         rospy.set_param('~baidu_unit_token_topic',
                           'baidu_unit_token_topic')

      self.baidu_unit_ak = rospy.get_param('~baidu_unit_ak')
      self.baidu_unit_sk = rospy.get_param('~baidu_unit_sk')
      # self.topic=rospy.get_param('~baidu_unit_token_topic')

   def talker(self, data):
      if data.data == 'reset':
         self.get_token()

      else:
         pass


if __name__ == "__main__":
   rospy.init_node('baidu_unit_token')
   rospy.loginfo("initialization  baidu_unit token")
   baidu_unit_token_main()
   rospy.loginfo("process done and quit")
