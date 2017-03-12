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
action = 'RunInstancesHour'

parameters = {
        'instanceName': 'zeng-test',
        'imageId': 'img-3wnd9xpl',
        'cpu': 1,
        'mem': 1,
        'zoneId': 100001
    }



import json
@with_qcloud_client('cvm')
def CreateInstances(qcloud_client_cvm, **_):
    #print qcloud_client_cvm.generateUrl(action, params)
    # 调用接口，发起请求

    qcloud_client_cvm.setRequestMethod('post')
    body = qcloud_client_cvm.call(action, parameters)
    result = json.loads(body)
    code = result.get('code', 0)

    print result
    print code


import json
@with_qcloud_client('cvm')
def DescribeInstances(qcloud_client_cvm, **_):
    action = 'DescribeInstances'
    parameters = {}
    print qcloud_client_cvm.generateUrl(action, parameters)

    body = qcloud_client_cvm.call(action, parameters)
    result = json.loads(body)

    instances = result.get('instanceSet')


    print instances[0]

DescribeInstances()
