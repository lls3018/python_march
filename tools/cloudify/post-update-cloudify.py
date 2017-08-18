#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
import commands

def update_rest_service():
    shutil.copy("./rest-service/files.py",
                "/opt/manager/env/lib/python2.7/site-packages/manager_rest")
    shutil.copy("./rest-service/resources.py",
                "/opt/manager/env/lib/python2.7/site-packages/manager_rest")
    shutil.copy("./rest-service/resources_v2.py",
                "/opt/manager/env/lib/python2.7/site-packages/manager_rest")
    shutil.copy("./rest-service/blueprints_manager.py",
                "/opt/manager/env/lib/python2.7/site-packages/manager_rest")
    status, output = commands.getstatusoutput("service cloudchef-restservice stop")
    print status, output
    status, output = commands.getstatusoutput("service cloudchef-restservice start")
    print status, output
    return


def update_mgmtworker_service():
    shutil.copy("./mgmtworker-service/__init__.py",
                "/opt/mgmtworker/env/lib/python2.7/site-packages/cloudify_agent/installer")
    status, output = commands.getstatusoutput("service cloudchef-mgmtworker stop")
    print status, output
    status, output = commands.getstatusoutput("service cloudchef-mgmtworker start")
    print status, output
    return

if __name__ == '__main__':
    update_mgmtworker_service()
    update_rest_service()