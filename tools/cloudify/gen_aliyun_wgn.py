from common.util import Connection
import os
import commands
import datetime
import shutil

if __name__=="__main__":

    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d-%H:%M:%S')

    tar_path = "$HOME/CloudChef-WorkSpace/cloudchef-aliyun-plugin.tar.gz"
    if os.path.exists(tar_path):
        os.remove(tar_path)

    ssh = Connection.Connection(host="192.168.84.19", username="root", password="Passw0rd")

    tar_cmd = "cd $HOME/CloudChef-WorkSpace/codebase/yacmp-orchestrator ; tar -zcvf " \
              "$HOME/CloudChef-WorkSpace/cloudchef-aliyun-plugin.tar.gz cloudchef-aliyun-plugin/"
    commands.getstatusoutput(tar_cmd)

    scp_cmd = "scp %s root@192.168.84.19:/var/cc/plugins" % (tar_path)
    commands.getstatusoutput(scp_cmd)

    if os.path.exists(tar_path):
        os.remove(tar_path)

    # gen the wgn plugin
    #gen_cmd = "cd /var/cc/plugins ; wagon create -s ./cloudchef-vsphere-plugin.tar.gz  -r  --validate"
    gen_cmd = "cd /var/cc/plugins ; wagon create -s ./cloudchef-aliyun-plugin.tar.gz"
    ret = ssh.execute(gen_cmd)

    current_dir = str(now) + '-aliyun'
    backup_cloudchef = "cd /var/cc/plugins ; mkdir %s ; mv cloudchef* %s" % (current_dir, current_dir)
    ret = ssh.execute(backup_cloudchef)

    scp_file = "cd /var/cc/plugins ; cp scp_aliyun_to_server.sh %s" % (current_dir)
    ret = ssh.execute(scp_file)
    print ret

    gen_version = "cd /var/cc/plugins ; echo %s >> aliyun-version.txt" % (now)
    ret = ssh.execute(gen_version)