#!/usr/bin/env python
# encoding: utf-8
import argparse
import commands


def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for cloudchef tool')

    parser.add_argument('-g', '--generate',
                        action='store',
                        help='generate the plugin | (aliyun, docker, vsphere, openstack)')

    args = parser.parse_args()
    return args


def generate_plugin(plugin):
    plugin_tar_name = None
    plugin_wgn_name = None
    if plugin == 'aliyun':
        plugin_tar_name = 'cloudchef-aliyun-plugin'
        plugin_wgn_name = 'cloudchef_aliyun_plugin-1.4.1-py27-none-linux_x86_64-centos-Core.wgn'
    elif plugin == 'docker':
        plugin_tar_name = 'cloudify-docker-plugin'
        plugin_wgn_name = 'cloudify_docker_plugin-1.3.2-py27-none-linux_x86_64-centos-Core.wgn'
    elif plugin == 'vsphere':
        plugin_tar_name = 'cloudchef-vsphere-plugin'
        plugin_wgn_name = 'cloudchef_vsphere_plugin-2.0-py27-none-linux_x86_64-centos-Core.wgn'
    elif plugin == 'openstack':
        plugin_tar_name = 'cloudify-openstack-plugin'
        plugin_wgn_name = 'cloudify_openstack_plugin-1.4-py27-none-linux_x86_64-centos-Core.wgn'

    ret, out = commands.getstatusoutput("cfy plugins list | grep %s" % plugin_tar_name)
    if ret == 0:
        plugin_id = out.split('|')[1].strip()
        print "the plugins id is:" + plugin_id
        delete_cmd = "cfy plugins delete -f -p " + plugin_id
        ret, out = commands.getstatusoutput(delete_cmd)
        print out

    upload_cmd = "cfy plugins upload -p %s" % plugin_wgn_name
    ret, out = commands.getstatusoutput(upload_cmd)
    print out


def main():
    """
    Let this thing fly
    """
    args = get_args()
    all_plugin = ('aliyun', 'docker', 'vsphere', 'openstack')
    if args.generate and (args.generate in all_plugin):
        print "start generate the %s plugin" % args.generate


# start this thing
if __name__ == "__main__":
    main()


