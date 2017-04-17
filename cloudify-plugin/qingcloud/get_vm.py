#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/3/9'

from qingcloud_plugin.connection import with_qingcloud_client


@with_qingcloud_client
def describeinstances(qingcloud_client, **_):
    body = qingcloud_client.describe_instances()
    print body


@with_qingcloud_client
def describe_instance_status_from_id(qingcloud_client, instance_id, **_):
    result = qingcloud_client.describe_instances(instances=[instance_id])
    instance = result['instance_set'][0] if result['instance_set'] else None
    if instance:
        instance_status = instance['status']
        instance_transition_status = instance['transition_status']
    else:
        instance_status = None
        instance_transition_status = None
    return instance_status, instance_transition_status


@with_qingcloud_client
def describe_instance_from_id(instance_id, qingcloud_client):
    """Gets the instance ID of a QCLOUD Instance

    :param instance_id: The ID of an QCLOUD Instance
    :param ctx:  The Cloudify ctx context.
    :returns an ID of a an QCLOUD Instance or None.
    """
    result = qingcloud_client.describe_instances(instances=[instance_id])
    instance = result['instance_set'][0] if result['instance_set'] else None
    return instance

instance_id = 'i-jdlc79r8'
instance_object = describe_instance_from_id(instance_id)
print instance_object

attribute = instance_object.get('eip')
print attribute