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



import json
@with_qcloud_client('dfw')
def Describesg(qcloud_client_dfw, **_):
    action = 'DescribeSecurityGroupPolicy'
    parameters = {
        'sgId': 'sg-cvnhntrc'
    }
    print qcloud_client_dfw.generateUrl(action, parameters)
    body = qcloud_client_dfw.call(action, parameters)
    result = json.loads(body)

    print result


Describesg()
print '------------'


@with_qcloud_client('dfw')
def Modifysg(qcloud_client_dfw, **_):
    action = 'ModifySecurityGroupPolicy'
    sg_ingress_parameters = {
        'sgId': 'sg-cvnhntrc',
        'egress.0.ipProtocol': 'tcp',
        'egress.0.cidrIp': '12.0.0.0/16',
        'egress.0.action': 'ACCEPT',
        'egress.0.desc': 'abcd',
        'egress.0.portRange': 99,
        'abc': '123'

    }

    para = {'ingress.0.portRange': '100', 'ingress.0.action': 'ACCEPT', 'ingress.0.cidrIp': '100.0.0.0/16',
     'egress.0.ipProtocol': 'tcp', 'ingress.0.desc': 'ingress', 'egress.0.desc': 'egress', 'egress.0.portRange': '',
     'sgId': 'sg-cvnhntrc', 'ingress.0.ipProtocol': 'tcp', 'egress.0.action': 'ACCEPT',
     'egress.0.cidrIp': '200.0.0.0/16', 'other': 'other'}

    print qcloud_client_dfw.generateUrl(action, para)

    body = qcloud_client_dfw.call(action, para)
    result = json.loads(body)

    print result

Modifysg()




def _create_group_rules():
    """For each rule listed in the blueprint,
    this will add the rule to the group with the given id.
    :param group: The group object that you want to add rules to.
    :raises NonRecoverableError: src_group_id OR ip_protocol,
    from_port, to_port, and cidr_ip are not provided.
    """

    rules = [
        {
            'direction': 'ingress',
            'ipProtocol': 'tcp',
            'cidrIp': '12.0.0.0/16',
            'action': 'ACCEPT',
            'desc': 'ingress',
            'portRange': '80'
        },
        {
            'direction': 'egress',
            'ipProtocol': 'tcp',
            'cidrIp': '10.0.0.0/16',
            'action': 'ACCEPT',
            'desc': 'egress',
            'portRange': ''
        }
    ]

    if not rules:
        return
    rules_para = {'sgId': 'sg-cvnhntrc'}

    ingress_rules = []
    egress_rules = []
    for rule in rules:
        if rule.get('direction') == 'ingress':
            del rule['direction']
            ingress_rules.append(rule)
        elif rule.get('direction') == 'egress':
            del rule['direction']
            egress_rules.append(rule)

    if len(ingress_rules) + len(egress_rules) == 0:
        print ('the direction param (direction: ingress/egress) is empty')
    else:
        for i in range(len(ingress_rules)):
            for (k, v) in ingress_rules[i].items():
                rules_para['ingress.'+str(i)+'.'+k] = v

        for i in range(len(egress_rules)):
            for (k, v) in egress_rules[i].items():
                rules_para['egress.'+str(i)+'.'+k] = v

    print rules_para


_create_group_rules()