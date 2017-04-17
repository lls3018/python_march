#!/usr/bin/env python
# encoding: utf-8
import argparse
from common.util import Connection
import os
import commands
import datetime


def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for cloudchef tool')

    parser.add_argument('-p', '--plugin',
                        action='store',
                        help='upload the plugin')

    args = parser.parse_args()
    return args


def gen_plugin(plugin_name):

    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d-%H:%M:%S')

    base_path = "$HOME/CloudChef-WorkSpace/"
    tar_path = base_path + "cloudchef-{}-plugin.tar.gz".format(plugin_name)
    tar_cmd = "cd {base_path}/codebase/smartcmp-orchestrator ; tar -zcvf " \
                  "{base_path}/cloudchef-{plugin_name}-plugin.tar.gz cloudchef-{plugin_name}-plugin/"\
                  .format(base_path=base_path, plugin_name=plugin_name)
    print tar_path
    print tar_cmd
    if os.path.exists(tar_path):
        print os.remove(tar_path)
    commands.getstatusoutput(tar_cmd)

    ssh = Connection.Connection(host="192.168.84.19", username="root", password="Passw0rd")

    gen_dir = plugin_name + '-' + str(now)
    gen_dir_cmd = "cd /var/cc/plugins ; mkdir {0}".format(gen_dir)
    print "1. make the dir"
    print ssh.execute(gen_dir_cmd)

    scp_cmd = "scp {} root@192.168.84.19:/var/cc/plugins/{}".format(tar_path, gen_dir)
    print "2. scp the tar.gz to the dir"
    print commands.getstatusoutput(scp_cmd)
    # gen the wgn plugin
    gen_cmd = "cd /var/cc/plugins/{0} ; wagon create ./*.tar.gz".format(gen_dir)
    print "3. create the wagon"
    print ssh.execute(gen_cmd)

    scp_file = "cd /var/cc/plugins ; cp scp_plugin_to_server.sh %s" % (gen_dir)
    print "4. cp the .sh to dir"
    print ssh.execute(scp_file)

    if os.path.exists(tar_path):
        os.remove(tar_path)


def main():
    """
    Let this thing fly
    """

    plugin_name = raw_input("Input the plugin name: ")

    gen_plugin(plugin_name)


if __name__ == "__main__":
    main()