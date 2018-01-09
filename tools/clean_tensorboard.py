#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: WayneZeng 
@contact: zwqjoy@163.com 
@site: http://www.cnblogs.com/WayneZeng/ 
@file: clean_tensorboard.py.py 
@time: 2018/1/9 11:38 
""" 

import commands
import logging

# 创建一个logger
logger = logging.getLogger('tensorboardlogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('tensorboard.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('[%(asctime)s][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

# 记录一条日志
logger.info("Start clean tensorboard")

status, output = commands.getstatusoutput(
    "kubectl get deployments --all-namespaces | grep tensorboard | awk '{print $1,$2,$7}'")

if status == 0:
    tensorboard_list = output.split("\n")
    for tensorboard in tensorboard_list:
        tensorboard_namespace = tensorboard.split()[0]
        tensorboard_name = tensorboard.split()[1]
        tensorboard_live = tensorboard.split()[2]
        if tensorboard_live.endswith("d"):
            tensorboard_day = int(tensorboard_live[:-1])
            if tensorboard_day > 14:
                delete_cmd = "kubectl delete deployment {0} --namespace={1}".\
                    format(tensorboard_name, tensorboard_namespace)
                status, output = commands.getstatusoutput(delete_cmd)
                logger.info(output)
    logger.info("Success clean tensorboard")
else:
    logger.error("Fail clean tensorboard")