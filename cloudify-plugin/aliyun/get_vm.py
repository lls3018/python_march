#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/2/20'

from ecs import instance
instance_id = 'i-wz9e2s7zkkhw080ldav8'

instance.get_state(instance_id)
instance.stop(instance_id=instance_id)
instance.terminate(instance_id=instance_id)