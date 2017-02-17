#!/usr/bin/env python
# encoding: utf-8
import sys
import commands
import os
import compileall
import argparse


def usage():
    usage_str = """
    python %s --help : to get help info
    """ % (sys.argv[0])
    return usage_str


def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for cloudchef tool')

    parser.add_argument('-u', '--upload',
                        action='store',
                        help='upload the plugin | '
                             '(aliyun, docker, vsphere, openstack, or other plugin name)')
    parser.add_argument('-d', '--dev', action='store_true', default=False)

    args = parser.parse_args()
    return args


def upload_plugin(plugin_name):

    ret, out = commands.getstatusoutput("cfy plugins list | grep %s" % plugin_name)
    if ret == 0:
        plugin_id = out.split('|')[1].strip()
        print "the {} plugin  id is {} ".format(plugin_name, plugin_id)
        delete_cmd = "cfy plugins delete -f -p " + plugin_id
        ret, out = commands.getstatusoutput(delete_cmd)
        print out

    upload_cmd = "cfy plugins upload -p *%s*.wgn" % plugin_name
    ret, out = commands.getstatusoutput(upload_cmd)
    print out
    print '---------------------------------------'


def clean_all_py(plugin_path):
    dir = plugin_path
    for root, dirs, filename in os.walk(dir):
        for file in filename:
            path_filename = os.path.join(root, file)
            if path_filename.endswith('.py') and file != "setup.py":
                os.remove(path_filename)

def main():
    """
    Let this thing fly
    """
    print usage()
    args = get_args()
    if args.upload:
        plugins = str(args.upload).split(',')
        for plugin in plugins:
            print "start upload the %s plugin" % args.upload
            upload_plugin(plugin.strip())
    if not args.dev:
        plugin_path = "/opt/mgmtworker/env/plugins/"
        compileall.compile_dir(plugin_path)
        clean_all_py(plugin_path)

if __name__ == "__main__":
    main()
