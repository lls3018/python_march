#! /usr/bin/env python
# coding=utf-8

import os
import compileall
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='the cloudchef plugin dir path')

    parser.add_argument('-p', '--path',
                        action='store',
                        help='the plugin path | (aliyun, aws, vsphere, openstack, docker)')

    args = parser.parse_args()
    return args


def clean_all_py(plugin_path):
    dir = plugin_path
    for root, dirs, filename in os.walk(dir):
        for file in filename:
            path_filename = os.path.join(root, file)
            if path_filename.endswith('.py'):
                os.remove(path_filename)


if __name__ == "__main__":
    args = get_args()
    if args.path:
        print "start gen the pyc only  plugin"
        plugin_path = args.path
        compileall.compile_dir(plugin_path)
        clean_all_py(plugin_path)
    else:
        print "Need the args"