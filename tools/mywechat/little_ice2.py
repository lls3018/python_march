#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/3/29'

import itchat
from itchat.content import *
import random

name = ""


# 获取好友消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def friend_chat(msg):
    # 让小冰回答
    global name
    name = msg['FromUserName']
    if u'妮' in name:
        return
    print(getUserNickName(msg))
    ask_xiaoice(msg)


# 群信息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def group_chat(msg):
    fromUserName = msg['FromUserName']
    global name
    group = itchat.search_chatrooms(userName=fromUserName)
    if group:
        if u'吃饭群' in group['NickName']:
            name = msg['FromUserName']
            ask_xiaoice(msg)
        if u'吃喝玩乐' in group['NickName']:
            name = msg['FromUserName']
            k = random.randint(0, 3)
            if k == 0:
                ask_xiaoice(msg)
            else:
                return
        if u'新繁阳' in group['NickName']:
            name = msg['FromUserName']
            ask_xiaoice(msg)
        if u'CC' in group['NickName']:
            return

    if msg['isAt'] is True:
        name = msg['FromUserName']
        ask_xiaoice(msg)


# 向智能小冰提问
def ask_xiaoice(msg):
    if msg['Type'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
        msg['Text'](msg['FileName'])
        itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),
                    toUserName='xiaoice-ms')
    if msg['Type'] in [TEXT, MAP, CARD, NOTE, SHARING]:
        itchat.send(msg['Text'], toUserName='xiaoice-ms')

# 获取昵称
def getUserNickName(msg):
    fromUserName = msg['FromUserName']
    fromUser = itchat.search_friends(userName=fromUserName)
    nickName = fromUser['NickName']
    return nickName


# 将小冰回复转发给发送者
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat=True)
def xiaoice_reply(msg):
    global name
    if msg['Type'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
        msg['Text'](msg['FileName'])
        itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), name)
    if msg['Type'] in [TEXT, MAP, CARD, NOTE, SHARING]:
        itchat.send(msg['Text'], name)

itchat.auto_login(hotReload=True)
itchat.run()