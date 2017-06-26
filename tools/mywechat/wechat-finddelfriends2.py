#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function


import itchat

try:
    from urllib import urlencode, quote_plus
except ImportError:
    from urllib.parse import urlencode, quote_plus

try:
    import urllib2 as wdf_urllib
    from cookielib import CookieJar
except ImportError:
    import urllib.request as wdf_urllib
    from http.cookiejar import CookieJar

import re
import time
import requests
import xml.dom.minidom
import json
import sys
import math
import subprocess
import ssl
import thread



DEBUG = False

MAX_GROUP_NUM = 30  # 每组人数
INTERFACE_CALLING_INTERVAL = 100  # 接口调用时间间隔, 间隔太短容易出现"操作太频繁", 会被限制操作半小时左右
MAX_PROGRESS_LEN = 60

base_uri = ''
redirect_uri = ''
push_uri = ''

skey = ''
wxsid = ''
wxuin = ''
pass_ticket = ''
deviceId = 'e000000000000000'

BaseRequest = {}

ContactList = []
My = []
SyncKey = []

try:
    xrange
    range = xrange
except:
    # python 3
    pass


def responseState(func, BaseResponse):
    ErrMsg = BaseResponse['ErrMsg'].encode('utf-8')
    Ret = BaseResponse['Ret']
    if DEBUG or Ret != 0:
        print('func: %s, Ret: %d, ErrMsg: %s' % (func, Ret, ErrMsg))

    print('func: %s, Ret: %d, ErrMsg: %s' % (func, Ret, ErrMsg))

    if Ret != 0:
        return False

    return True


def getRequest(url, data=None):
    try:
        data = data.encode('utf-8')
    except:
        pass
    finally:
        return wdf_urllib.Request(url=url, data=data)


# def create_chatroom(self, memberList, topic=''):
#     url = '%s/webwxcreatechatroom?pass_ticket=%s&r=%s' % (
#         self.loginInfo['url'], self.loginInfo['pass_ticket'], int(time.time()))
#     data = {
#         'BaseRequest': self.loginInfo['BaseRequest'],
#         'MemberCount': len(memberList),
#         'MemberList': [{'UserName': member['UserName']} for member in memberList],
#         'Topic': topic, }
#     headers = {
#         'content-type': 'application/json; charset=UTF-8',
#         'User-Agent' : config.USER_AGENT }
#     r = requests.session().post(url, headers=headers,
#         data=json.dumps(data, ensure_ascii=False).encode('utf8', 'ignore'))
#     return ReturnValue(rawResponse=r)


def createChatroom(UserNames):
    MemberList = [{'UserName': UserName} for UserName in UserNames]

    url = base_uri + \
        '/webwxcreatechatroom?pass_ticket=%s&r=%s' % (
            pass_ticket, int(time.time()))
    params = {
        'BaseRequest': BaseRequest,
        'MemberCount': len(MemberList),
        'MemberList': MemberList,
        'Topic': '',
    }

    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    # print(data)

    dic = json.loads(data)
    ChatRoomName = dic['ChatRoomName']
    MemberList = dic['MemberList']
    DeletedList = []
    BlockedList = []
    for Member in MemberList:
        if Member['MemberStatus'] == 4:  # 被对方删除了
            DeletedList.append(Member['UserName'])
        elif Member['MemberStatus'] == 3:  # 被加入黑名单
            BlockedList.append(Member['UserName'])

    state = responseState('createChatroom', dic['BaseResponse'])

    return ChatRoomName, DeletedList, BlockedList


def deleteMember(ChatRoomName, UserNames):
    url = base_uri + \
        '/webwxupdatechatroom?fun=delmember&pass_ticket=%s' % (pass_ticket)
    params = {
        'BaseRequest': BaseRequest,
        'ChatRoomName': ChatRoomName,
        'DelMemberList': ','.join(UserNames),
    }

    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    # print(data)

    dic = json.loads(data)

    state = responseState('deleteMember', dic['BaseResponse'])
    return state


def addMember(ChatRoomName, UserNames):
    import time
    time.sleep(3)
    url = base_uri + \
        '/webwxupdatechatroom?fun=addmember&pass_ticket=%s' % (pass_ticket)
    params = {
        'BaseRequest': BaseRequest,
        'ChatRoomName': ChatRoomName,
        'AddMemberList': ','.join(UserNames),
    }

    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')

    # print(data)

    dic = json.loads(data)
    MemberList = dic['MemberList']
    DeletedList = []
    BlockedList = []
    for Member in MemberList:
        if Member['MemberStatus'] == 4:  # 被对方删除了
            DeletedList.append(Member['UserName'])
        elif Member['MemberStatus'] == 3:  # 被加入黑名单
            BlockedList.append(Member['UserName'])

    state = responseState('addMember', dic['BaseResponse'])

    return DeletedList, BlockedList


def main():

    itchat.auto_login(hotReload=True)

    MemberList = itchat.get_friends(update=True)[0:]

    MemberCount = len(MemberList)
    print('通讯录共%s位好友' % MemberCount)

    ChatRoomName = ''
    result = []
    d = {}
    for Member in MemberList:
        d[Member['UserName']] = (Member['NickName'].encode(
            'utf-8'), Member['RemarkName'].encode('utf-8'))
    print('开始查找...')
    group_num = int(math.ceil(MemberCount / float(MAX_GROUP_NUM)))
    for i in range(0, group_num):
        UserNames = []
        for j in range(0, MAX_GROUP_NUM):
            if i * MAX_GROUP_NUM + j >= MemberCount:
                break
            Member = MemberList[i * MAX_GROUP_NUM + j]
            UserNames.append(Member['UserName'])

        # 新建群组/添加成员
        if ChatRoomName == '':
            (ChatRoomName, DeletedList, BlockedList) = createChatroom(
                UserNames)
        else:
            (DeletedList, BlockedList) = addMember(ChatRoomName, UserNames)

        # todo BlockedList 被拉黑列表

        DeletedCount = len(DeletedList)
        if DeletedCount > 0:
            result += DeletedList

        # 删除成员
        deleteMember(ChatRoomName, UserNames)

        # 进度条
        progress = MAX_PROGRESS_LEN * (i + 1) / group_num
        print('[', '#' * progress, '-' * (MAX_PROGRESS_LEN - progress), ']', end='')
        print('新发现你被%d人删除' % DeletedCount)
        for i in range(DeletedCount):
            if d[DeletedList[i]][1] != '':
                print(d[DeletedList[i]][0] + '(%s)' % d[DeletedList[i]][1])
            else:
                print(d[DeletedList[i]][0])

        if i != group_num - 1:
            print('正在继续查找,请耐心等待...')
            # 下一次进行接口调用需要等待的时间
            time.sleep(INTERFACE_CALLING_INTERVAL)
    # todo 删除群组

    print('\n结果汇总完毕,90s后可重试...')
    resultNames = []
    for r in result:
        if d[r][1] != '':
            resultNames.append(d[r][0] + '(%s)' % d[r][1])
        else:
            resultNames.append(d[r][0])

    print('---------- 被删除的好友列表(共%d人) ----------' % len(result))
    # 过滤emoji
    resultNames = map(lambda x: re.sub(r'<span.+/span>', '', x), resultNames)
    if len(resultNames):
        print('\n'.join(resultNames))
    else:
        print("无")
    print('---------------------------------------------')


if __name__ == '__main__':

    print('本程序的查询结果可能会引起一些心理上的不适,请小心使用...')
    main()
    print('回车键退出...')