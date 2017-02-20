#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/2/20'

from ecs import instance
instance.get_state('i-wz9514uorf5a4rioasn2')
#instance.stop(instance_id='i-wz9514uorf5a4rioasn2')
instance.terminate(instance_id='i-wz9514uorf5a4rioasn2')