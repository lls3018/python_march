#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/3/29'

import itchat
from itchat.content import *

name = "zengwenqi"

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], True, False, False)
# get text and send to XiaoIce # 将文字等信息转发给小冰
def send_xiaoice(msg):
    global name
    name = msg['FromUserName']
    itchat.send(msg['Text'], toUserName='xiaoice-ms')


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], True, False, False)
# get img and send to XiaoIce # 将图片等信息转发给小冰
def send_xiaoice(msg):
    global name
    name = msg['FromUserName']
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),
                toUserName='xiaoice-ms')


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], False, False, True)
# get text and send to Sender # 将小冰回复的文字等信息转发给发送者
def send_reply(msg):
    global name
    itchat.send(msg['Text'], name)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], False, False, True)
# get img and send to Sender 将小冰回复的图片等信息转发给发送者
def send_xiaoice(msg):
    global name
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), name)


itchat.auto_login(hotReload=True)
itchat.run()