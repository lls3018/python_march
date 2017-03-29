#!/usr/bin/python
# -*- coding: utf-8 -*-

from qingcloud_plugin.connection import with_qingcloud_client


@with_qingcloud_client
def Describesg(qingcloud_client, **_):
    body = qingcloud_client.describe_security_groups()
    print body


@with_qingcloud_client
def Describesg_id(qingcloud_client, sg_id,**_):
    body = qingcloud_client.describe_security_groups(security_groups=[sg_id])
    print body

@with_qingcloud_client
def Createsg(qingcloud_client, **_):
    result = qingcloud_client.create_security_group(security_group_name='zeng_test')
    print result


@with_qingcloud_client
def Createsg(qingcloud_client, **_):
    result = qingcloud_client.create_security_group(security_group_name='zeng_test')
    print result


@with_qingcloud_client
def Modifysg(qingcloud_client, sg_id,**_):
    rules_parameters = [{
        'protocol': 'tcp',
        'priority': 1,
        'action': 'accept',
        'direction': 0,
        'val1': 4,
        'val2': 201,
        'val3': ''
    }]

    result = qingcloud_client.add_security_group_rules(
        security_group=sg_id,
        rules=rules_parameters)

    print result



Describesg_id(sg_id='sg-i35jjtc6')
Modifysg(sg_id='sg-i35jjtc6')

# @with_qcloud_client('dfw')
# def Describesgs(qcloud_client_dfw, **_):
#     action = 'DescribeSecurityGroups'
#     param = {}
#     body = qcloud_client_dfw.call(action, param)
#     result = json.loads(body)
#
#     print result
#
#
# @with_qcloud_client('dfw')
# def Describesgs2(qcloud_client_dfw, **_):
#     action = 'DescribeSecurityGroups'
#     param = {}
#     body = qcloud_client_dfw.call(action, param)
#     result = json.loads(body)
#
#     print result
#
#
# Describesgs()
#
# @with_qcloud_client('dfw')
# def Modifysg(qcloud_client_dfw, **_):
#     action = 'ModifySecurityGroupPolicy'
#     sg_ingress_parameters = {
#         'sgId': 'sg-cvnhntrc',
#         'egress.0.ipProtocol': 'tcp',
#         'egress.0.cidrIp': '12.0.0.0/16',
#         'egress.0.action': 'ACCEPT',
#         'egress.0.desc': 'abcd',
#         'egress.0.portRange': 99,
#     }
#
#     # para = {'ingress.0.portRange': '100', 'ingress.0.action': 'ACCEPT', 'ingress.0.cidrIp': '100.0.0.0/16',
#     #  'egress.0.ipProtocol': 'tcp', 'ingress.0.desc': 'ingress', 'egress.0.desc': 'egress', 'egress.0.portRange': '',
#     #  'sgId': 'sg-cvnhntrc', 'ingress.0.ipProtocol': 'tcp', 'egress.0.action': 'ACCEPT',
#     #  'egress.0.cidrIp': '200.0.0.0/16', 'other': 'other'}
#
#
#     para = {u"ingress.0.portRange": 55,
#             u"egress.0.desc": u'xijia',
#             u"ingress.0.desc": u'yangrui',
#             u"ingress.0.action": u'ACCEPT',
#             u"ingress.0.ipProtocol": u'tcp',
#             u"egress.0.action": u'ACCEPT',
#             u"egress.0.cidrIp": u'11.0.0.0/16',
#             u"egress.0.portRange": '77',
#             u"ingress.0.cidrIp": u'10.0.0.0/16',
#             'sgId': u'sg-fxvbzc8a',
#             u"egress.0.ipProtocol": u'tcp'}
#
#     para = {u"ingress.0.portRange'": 55, u"egress.0.desc'": u'xijia', u"ingress.0.desc'": u'yangrui', u"ingress.0.action'": u'ACCEPT', u"ingress.0.ipProtocol'": u'tcp', u"egress.0.action'": u'ACCEPT', u"egress.0.cidrIp'": u'11.0.0.0/16', u"egress.0.portRange'": 77, u"ingress.0.cidrIp'": u'10.0.0.0/16', 'sgId': u'sg-fxvbzc8a', u"egress.0.ipProtocol'": u'tcp'}
#
#     print qcloud_client_dfw.generateUrl(action, para)
#
#     body = qcloud_client_dfw.call(action, para)
#     result = json.loads(body)
#
#     print result
#
#
# @with_qcloud_client('dfw')
# def modify_security_group(qcloud_client_dfw):
#
#     action = 'DescribeSecurityGroups'
#     parameters = {}
#     body = qcloud_client_dfw.call(action, parameters)
#     result = json.loads(body)
#
#     print result
#
#     param = {'instanceSet.0.sgIds.0': u'sg-cvnhntrc', 'instanceSet.0.instanceId': u'ins-2b8c8gq7'}
#     action = 'ModifySecurityGroupsOfInstance'
#     print qcloud_client_dfw.generateUrl(action, param)
#     body = qcloud_client_dfw.call(action, param)
#     result = json.loads(body)
#     print result
#
#
# def _create_group_rules():
#     """For each rule listed in the blueprint,
#     this will add the rule to the group with the given id.
#     :param group: The group object that you want to add rules to.
#     :raises NonRecoverableError: src_group_id OR ip_protocol,
#     from_port, to_port, and cidr_ip are not provided.
#     """
#
#     rules = [
#         {
#             'direction': 'ingress',
#             'ipProtocol': 'tcp',
#             'cidrIp': '12.0.0.0/16',
#             'action': 'ACCEPT',
#             'desc': 'ingress',
#             'portRange': '80'
#         },
#         {
#             'direction': 'egress',
#             'ipProtocol': 'tcp',
#             'cidrIp': '10.0.0.0/16',
#             'action': 'ACCEPT',
#             'desc': 'egress',
#             'portRange': ''
#         }
#     ]
#
#     if not rules:
#         return
#     rules_para = {'sgId': 'sg-cvnhntrc'}
#
#     ingress_rules = []
#     egress_rules = []
#     for rule in rules:
#         if rule.get('direction') == 'ingress':
#             del rule['direction']
#             ingress_rules.append(rule)
#         elif rule.get('direction') == 'egress':
#             del rule['direction']
#             egress_rules.append(rule)
#
#     if len(ingress_rules) + len(egress_rules) == 0:
#         print ('the direction param (direction: ingress/egress) is empty')
#     else:
#         for i in range(len(ingress_rules)):
#             for (k, v) in ingress_rules[i].items():
#                 rules_para['ingress.'+str(i)+'.'+k] = v
#
#         for i in range(len(egress_rules)):
#             for (k, v) in egress_rules[i].items():
#                 rules_para['egress.'+str(i)+'.'+k] = v
#
#     print rules_para
