#!/usr/bin/env python
# encoding: utf-8

import argparse
import shutil
import commands
import os
import sys

__author__ = "zengwenqi"
__date__ = "2016-8-28"


def usage():
    usage_str = """
    %s after deploy the clouchef,need to run the script
    """ % (sys.argv[0])
    return usage_str


def get_args():
    parser = argparse.ArgumentParser(usage=usage())
    parser.add_argument("-m", "--mgmtworkservice",
                        action="store_true",
                        help="update the mgmtwork service")
    parser.add_argument("-r", "--restservice",
                        action="store_true",
                        help="update the rest service")
    parser.add_argument("-y", "--yamlfile",
                        action="store_true",
                        help="update the yaml file")
    args = parser.parse_args()
    return args


def update_mgmtwork_service():
    print "update mgmtwork service"
    shutil.copy("./mgmtwork-service/workflows.py",
                "/opt/mgmtworker/env/lib/python2.7/site-packages/cloudify/plugins")
    status, output = commands.getstatusoutput("service cloudify-mgmtworker stop")
    print status, output
    status, output = commands.getstatusoutput("service cloudify-mgmtworker start")
    print status, output
    return True


def update_rest_service():
    print "update rest service"
    shutil.copy("./rest-service/files.py",
                "/opt/manager/env/lib/python2.7/site-packages/manager_rest")
    shutil.copy("./rest-service/resources.py",
                "/opt/manager/env/lib/python2.7/site-packages/manager_rest")
    shutil.copy("./rest-service/resources_v2.py",
                "/opt/manager/env/lib/python2.7/site-packages/manager_rest")
    status, output = commands.getstatusoutput("service cloudify-restservice stop")
    print status, output
    status, output = commands.getstatusoutput("service cloudify-restservice start")
    print status, output
    return True


def update_yaml_file():
    print "update yaml file"
    if os.path.exists('/opt/manager/resources/spec'):
        shutil.rmtree('/opt/manager/resources/spec')
    shutil.copytree("./spec/", "/opt/manager/resources/spec")
    return True


def main():
    """
    Let this thing fly
    """
    args = get_args()
    if args.mgmtworkservice:
        update_mgmtwork_service()
    elif args.restservice:
        update_rest_service()
    elif args.mgmtworkservice:
        update_yaml_file()
    else:
        print "do the post update..."
        update_mgmtwork_service()
        update_rest_service()
        update_yaml_file()


if __name__ == "__main__":
    main()
