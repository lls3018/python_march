import commands,os

if __name__=="__main__":
    os.chdir("/home/cloudchef/cfy")
    ret,out = commands.getstatusoutput("cfy plugins list | grep cloudchef-vsphere-plugin")
    print ret, out
    cloud_chef_id = out.split('|')[1].strip()
    print cloud_chef_id

    delete_cmd = "cfy plugins delete -p " + cloud_chef_id
    ret, out = commands.getstatusoutput(delete_cmd)
    print out

    upload_cmd = "cfy plugins upload -p cloudchef_vsphere_plugin-1.3-py27-none-linux_x86_64-centos-Core.wgn"
    ret, out = commands.getstatusoutput(upload_cmd)
    print out