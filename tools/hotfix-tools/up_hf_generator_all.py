# __CR__
# Copyright (c) 2008-2013 EMC Corporation
# All Rights Reserved
#
# This software contains the intellectual property of EMC Corporation
# or is licensed to EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of EMC.
# __CR__
# __Wayne.Zeng__

import os
import sys
import commands
from optparse import OptionParser
import configobj

HF_ELEMENTS = []

HFLOC_VERSION_ID = "000000"

def usage():
    usage_str = """
    Usage: %s --version All  --path /home/peter/20*-rpl2sles-upgrade
    where path is the check-in location for HF src files.
    use the --help to get the use method
    """ % (sys.argv[0])
    return usage_str

def gen_plpylib(src_tree, version):
    deploy_pylib = "/usr/local/maui/lib/site_packages/"
    src_pylib = os.path.join(src_tree, "src/platform/upgrade/rpl2sles/atmos")
    if os.path.exists(deploy_pylib):
        cmd = "rm -rf %s" % deploy_pylib
        status, output = commands.getstatusoutput(cmd)
        if status:
            print 'can not remove previous deploy_pylib dir: %s' % ouput
            return False

    os.makedirs(deploy_pylib)

    cmd = "cp -raf %s %s; find %s | grep svn | xargs rm -rf; find %s | grep pyc | xargs rm -rf" % (src_pylib, deploy_pylib, deploy_pylib, deploy_pylib)
    status, output = commands.getstatusoutput(cmd)
    if status:
        print 'cp and strip %s to %s failed: %s' % (src_pylib, deploy_pylib, output)
        return False

    cmd = "tar -cvf %s/plpylib.tar %s" % (HFLOC_VERSION_ID, deploy_pylib)
    status, output = commands.getstatusoutput(cmd)
    if status:
        print "can not make plpylib.tar: %s" % output
        return False
    
    return True

def gen_pre_upgrade_scripts(version):
    '''
    fetch pre-upgrade scripts from trunk/mgmt/upgrade/scripts/
    make pre-upgrade scripts tar ball
    '''
    if os.path.exists("./upgrade"):
        cmd = "rm -rf %s" % "./upgrade"
        status, output = commands.getstatusoutput(cmd)
        if status:
            print "remove ./upgrade failed: %s" % output

    cmd = "svn co https://tvg01.lss.emc.com/svn/maui/trunk/src/mgmt/upgrade/" 
    #cmd = "svn co https://cig-svn.isus.emc.com/svn/maui/dev/sumatra-upgrade-new/src/mgmt/upgrade/"
    status, output = commands.getstatusoutput(cmd)
    if status:
        print "check out upgrade scritps from trunk failed: %s" % output
        return False

    pre_upgrade_deploy = "/usr/local/maui/etc/mgmt/scripts/Sumatra/"
    if os.path.exists(pre_upgrade_deploy):
        cmd = "rm -rf %s" % pre_upgrade_deploy
        status, output = commands.getstatusoutput(cmd)
        if status:
            print "remove previous pre-upgrade deployment dir failed: %s" % output
            return False

    os.makedirs(pre_upgrade_deploy)

    cmd = "cp -raf ./upgrade/scripts/* %s" % pre_upgrade_deploy
    status, output = commands.getstatusoutput(cmd)
    if status:
        print "cp pre-upgrade scripts to deployment location failed: %s" % output
        return False
    
    cmd = "tar -cvf %s/pre_upgrade_scripts.tar %s" % (HFLOC_VERSION_ID, pre_upgrade_deploy)
    status, output = commands.getstatusoutput(cmd)
    if status:
        print "can not make pre_upgrade_scripts.tar: %s" % output
        return False

    return True

def cp_backup_list(version):
    cmd = "cp -raf ./upgrade/tools/backup_list.py %s" % HFLOC_VERSION_ID
    status, output = commands.getstatusoutput(cmd)
    if status:
        print "cp backup_list.py to deployment location failed: %s" % output
        return False

    return True

def cp_hf_elements(src_tree):
    for element in HF_ELEMENTS:
        element = os.path.join(src_tree, element)
        cmd = 'cp -raf %s %s' % (element, HFLOC_VERSION_ID)
        status, output = commands.getstatusoutput(cmd)
        if status:
            print 'cp hf element %s into %s failed: %s' % (element, HFLOC_VERSION_ID, output)
            return False
    
#    cmd = "cp -raf ./misc/* %s" % HFLOC_VERSION_ID
#    status, output = commands.getstatusoutput(cmd)
#    if status:
#        print "cp misc elements failed: %s" % output
#        return False
    
    return True

def gen_hf(version):
    if not os.path.exists("./doc"):
        os.mkdir("./doc")
    cmd = "PYTHONPATH=./pylib python hotfixgen -i hotfix-%s.cfg --eng=./pylib/ --data=./%s --doc=./doc" % ( (HFLOC_VERSION_ID,) * 2)
    status, output = commands.getstatusoutput(cmd)
    if status:
        print "generate HF hotfix-%s.tgz failed: %s" % (HFLOC_VERSION_ID, output)
        return False

    return True
   
def read_hotfix_cfg(cfg_file):
    try:
        cfg = configobj.ConfigObj(cfg_file,encoding='UTF8')
    except Exception,e:
        print "cfg_file is wrong"
        print e
        return False
   
    elements_path = []
    hf_elements = 'file_build_path'
    if cfg.has_key(hf_elements):
        elements_path = cfg[hf_elements].strip().split('\n')
    else:
        return False

    global HFLOC_VERSION_ID
    if cfg.has_key('id'):
        HFLOC_VERSION_ID = str(cfg['id'])
    else:
        return False

    for element_path in elements_path:
        element_path = element_path.strip().split()
        if len(element_path)==2 and element_path[0]=="Buildpath":
            HF_ELEMENTS.append(element_path[1])
    return True

    
    
if __name__ == "__main__":
    parser = OptionParser(usage = usage())

    parser.add_option("-p", "--path", action="store", dest="src_tree", help="Root path of local HF branch, svn co the branch in advance")

    parser.add_option("-c", "--cfg", action="store", dest="config", help="Target config where the HF will be applied")

    parser.add_option("-s", "--svn", action="store", dest="svn", help="svn path where the HF will be applied")
    
    (options, args) = parser.parse_args(sys.argv)

#    if not options.svn 
#        print "svn is need: %s" % usage()
#        sys.exit(1)
           
    if not options.config:
        print "the config file is needed"
        sys.exit(1)

    if not options.src_tree:
        print "the src_tree is needed"
        sys.exit(1)
    
    if not read_hotfix_cfg(options.config):
        print "get the hotfix config is wrong"

    if os.path.exists(HFLOC_VERSION_ID):
        cmd = 'rm -rf %s' % HFLOC_VERSION_ID
        status, output = commands.getstatusoutput(cmd)
        if status:
            print 'can not remove previous element dir %s: %s' % (HFLOC_VERSION_ID, output)
            sys.exit(1)
    
    os.mkdir(HFLOC_VERSION_ID)
    
#    if not gen_plpylib(options.src_tree, options.version):
#        print "generate plpylib.tar failed"
#        sys.exit(1)
    
#    if not gen_pre_upgrade_scripts(options.version):
#        print "generate pre_upgrade_scripts.tar failed"
#        sys.exit(1)

#    if not cp_backup_list(options.version):
#        print "cp backup_list.py failed"
#        sys.exit(1)

    if not cp_hf_elements(options.src_tree):
        print "cp hf elements failed"
        sys.exit(1)
    
#    if not gen_hf(options.version):
#        print "gen_hf failed"
#        sys.exit(1)
    print "Success!!!"
