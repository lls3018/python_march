#!/usr/bin/python
# -*- coding: utf-8 -*-

# 引入云API入口模块
from QcloudApi.qcloudapi import QcloudApi
from qcloud_plugin.connection import with_qcloud_client

'''
module 设置需要加载的模块
已有的模块列表：
cvm      对应   cvm.api.qcloud.com
cdb      对应   cdb.api.qcloud.com
lb       对应   lb.api.qcloud.com
trade    对应   trade.api.qcloud.com
sec      对应   csec.api.qcloud.com
image    对应   image.api.qcloud.com
monitor  对应   monitor.api.qcloud.com
cdn      对应   cdn.api.qcloud.com
wenzhi   对应   wenzhi.api.qcloud.com
'''
module = 'cdb'

'''
action 对应接口的接口名，请参考产品文档上对应接口的接口名
'''
action = 'RunInstances'

#parameters = {'mem': 2, 'period': 1, 'imageId': 'img-31tjrtph', 'PayMode': 'Month', 'bandwidth': 1, 'wanIp': 1, 'instanceName': 'qcloud-4i70qc', 'cpu': 1}

parameters = {'mem': 2, u'period': 1, 'imageId': u'img-31tjrtph', u'PayMode': u'Month', u'bandwidth': 1, u'wanIp': 1, 'storageSize': 0, 'instanceName': u'qcloud-tqpnpm', 'cpu': 1}

@with_qcloud_client('cvm')
def CreateInstances(qcloud_client_cvm, **_):
    #print qcloud_client_cvm.generateUrl(action, params)
    # 调用接口，发起请求
    import json
    body = qcloud_client_cvm.call(action, parameters)
    result = json.loads(body)
    print result

    print result.get('message').encode("UTF-8")


#CreateInstances()


import json
@with_qcloud_client('trade')
def DescribeDealsByCond(qcloud_client_trade, **_):
    action = 'DescribeDealsByCond'
    parameters = {'startTime': '2017-03-01 00:00:00', 'endTime': '2017-04-01 00:00:00'}
    body = qcloud_client_trade.call(action, parameters)
    result = json.loads(body)

    print result
    print result.get('message').encode("UTF-8")

#DescribeDealsByCond()



import json
@with_qcloud_client('trade')
def DescribeDeals(qcloud_client_trade, **_):
    action = 'DescribeDeals'
    parameters = {}
    body = qcloud_client_trade.call(action, parameters)
    result = json.loads(body)

    #print result
    #print result.get('message').encode("UTF-8")

    for deal in result.get('dealDetails'):
        print deal

DescribeDeals()



import json
@with_qcloud_client('trade')
def PayDeals(qcloud_client_trade, **_):
    action = 'PayDeals'
    parameters = {'dealIds.1': '3755578'}
    body = qcloud_client_trade.call(action, parameters)
    result = json.loads(body)

    print result
    print result.get('message').encode("UTF-8")


PayDeals()