#!/usr/bin/env python
# encoding: utf-8
import sys
import argparse
import commands


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

    args = parser.parse_args()
    return args


def upload_plugin(plugin_name):

    ret, out = commands.getstatusoutput("cfy plugins list | grep %s" % plugin_name)
    if ret == 0:
        plugin_id = out.split('|')[1].strip()
        print "the plugins id is:" + plugin_id
        delete_cmd = "cfy plugins delete -f -p " + plugin_id
        ret, out = commands.getstatusoutput(delete_cmd)
        print out

    upload_cmd = "cfy plugins upload -p *%s*.wgn" % plugin_name
    ret, out = commands.getstatusoutput(upload_cmd)
    print out


def main():
    """
    Let this thing fly
    """
    args = get_args()
    if args.upload:
        print "start upload the %s plugin" % args.upload
        upload_plugin(args.upload)
    else:
        print usage()

# start this thing
if __name__ == "__main__":
    main()