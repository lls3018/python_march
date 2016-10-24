import util.Env
import util.Connection
import urllib
import time
import os

from PyQt4 import QtGui, QtCore

authorID = "wenqiz@cn.ibm.com"
TIMEOUT_UPGRADE_DOWNLOAD = 3600
UPGRADE_DOWNLOAD_DONE_STATE = "Download is Over. Ready to begin system upgrade"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Code_Upgrade(QtCore.QThread):
    def __init__(self,host_ip="",host_username="",host_password="",
                 xiv_name="",xiv_ip="",xiv_tar_path="",xiv_tar_name="",copy_flag=False,upgrade_flag=False):
        QtCore.QThread.__init__(self)

        # host
        self.host_ip = host_ip
        self.host_username = host_username
        self.host_password = host_password
        # xiv
        self.xiv_name = xiv_name
        self.xiv_ip = xiv_ip
        self.xiv_tar_path = xiv_tar_path
        self.xiv_tar_name = xiv_tar_name

        self.SSH = util.Connection.Connection(host=self.xiv_ip,
                                         username="root",
                                        private_key=util.Env.id_rsa)
        self.copy_flag = copy_flag
        self.upgrade_flag = upgrade_flag

    def __del__(self):
        self.exiting = True
        self.wait()
        if self.SSH is not None:
            self.SSH.close()

    def run(self):
        if self.copy_flag is True:
            self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),    "(1) ***** Start setup Env to XIV *****")
            if self.envSetup():
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(2) ***** Start upload the upgrade tar ball from Host to XIV *****")
                if self.copyTarFileToSystem(self.host_ip,self.host_username,self.host_password,self.xiv_tar_path+"/"+self.xiv_tar_name):
                    self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"------------Copy Done---------------")
                else:
                    self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(2.1)-----Faild: upload the upgrade tar ball from Host to XIV---------")
            else:
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(1.1)-----Failed: setup Env to XIV-------")

        if self.upgrade_flag is True:
            self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(3)***** Start upgrade XIV *****")
            if self.perform_package_append():
                if self.waitUntilUpgradeStatus(UPGRADE_DOWNLOAD_DONE_STATE):
                    self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(4)-----Download is Over. Ready to begin system upgrade---------")
                    self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(5)-----Begin to run system upgrade---------")
                    if self.upgrade_system():
                        self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(5.1)-----Upgrade command  is run success,please wait ---------")
                    else:
                        self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(5.2)-----Failed: run upgrade command---------")

    def envSetup(self):
        '''
        **@Description: Setup the env for upgrade:**

         Remove previous version files**
         Verify sufficient free capacity on file-system**

        - @return: code: 0:failed;1:successful

        '''

        #cmd="xcli.py local_storage_clear -u xiv_development -p x1vD3v"
        #self.SSH.execute(cmd)
        #time.sleep(10)

        self.SSH.execute("cd /local/scratch/ ; rm ixss* -rf")
        self.SSH.execute("cd /local/scratch/ ; rm upgrade* -rf")
        time.sleep(10)
        self.SSH.execute("cd /local/ ; mkdir upgrade_packages")
        self.SSH.execute("cd /local/upgrade_packages/ ; rm upgrade* -rf")
        self.SSH.execute("ln -s /local/upgrade_packages /local/scratch/upgrade_packages")
        return 1


    def copyTarFileToSystem(self,source_hostname,source_username,source_pwd, filePath, destPath="/local/upgrade_packages/upgrade.tar.gz"):
        '''
        **@Description: Copy the target tarball to xiv system.**

        - @param1: source_hostname: [String] The host that you wanna download the tarball of the target build
        - @param2: source_username: [String] The user allowed to access the source host
        - @param3: source_pwd: [String] The pwd for the source_user
        - @param4: sourceFile: [String] The path on the source host to download the package
        - @param5: destPath: [String] The dest_path you wanna save the package on the xiv
        - @return: code: 0: failed. 1:successful
        '''

        #Check if the sourceFile exists.
        self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"[DEBUG] file: %s " % filePath)
        print("[DEBUG] file: %s " % filePath)

        print "[DEBUG]get into copyTarFileToSystem..."
        print "==== Download Build Package for Source Host, BY SCP ..."

        scp_cmd= '''expect -d -c "
             set timeout 1800;
             spawn scp -r %s@%s:%s %s;
             expect {
             \"*yes/no*\" {set timeout 1; send \"yes\\\\r\"};
             \"*password*\" {send \"%s\\\\r\"};}
             expect eof" 2>&1; echo return=$? ''' % (source_username,source_hostname,filePath, destPath, source_pwd)

        print "[DEBUG] scp_cmd:"+scp_cmd
        print "---------------------------------------"
        ret=self.SSH.execute(scp_cmd)
        len = ret.__len__()
        if ret[-1].strip() != "return=0":
            print ("scp_cmd %s executed failed." % scp_cmd)
            for line in ret:
                print line
            return 0

        return 1

    def getPackageSizeAndName(self,package_name_with_path="/local/upgrade_packages/upgrade.tar.gz"):
        '''
        **@Description: To get the package size and name, which will be used in cmd 'perform_package_append'**

        - @param1: [String] package_name_with_path: The package name with path
        - @return: code: 0: failed; package_size: successful

        '''

        print("==== Get Package Size=======")
        ret_size = self.SSH.execute("ls -l /local/upgrade_packages/upgrade.tar.gz | awk '{ print $5 }'")
        package_size = ret_size[0]
        print("==== Get Package Name=======")
        ret_name = self.xiv_tar_name.split('-')
        package_name = '-'.join(ret_name[2:-4])

        self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),package_size + " " + package_name)

        if (package_size,package_name) is not (0,0):
            return (int(package_size),package_name)
        else:
            return (0,0)

    def perform_package_append(self,lastFragment="yes"):
        '''
        **@Description: To perform the package_append. Which will Distributing the package to other  modules**

        - @param1: [String] offset: The size of the package
        - @param2: [String] to_version: The target version you wanna upgrade the code to.
        - @param3: [String] lastFragment: DEFAULT is "yes"
        - @return: code: 0: failed; 1: successful

        '''

        upgrade_state_info=self.upgrade_get_status()
        cur_upgrade_state=upgrade_state_info["upgrade_state"].lower().strip()
        upgrade_state=UPGRADE_DOWNLOAD_DONE_STATE.lower().strip()

        if cur_upgrade_state == upgrade_state:
            return 1

        (offset,to_version) = self.getPackageSizeAndName()
        if (offset,to_version) is not (0,0):
            self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"=====  Perform Package append =====")
            print("=====  Perform Package append  =====")
            cmd='xcli.py -u xiv_development -p x1vD3v upgrade_package_append fragment= offset=%s last_fragment=%s version=%s; echo return=$?' % \
                (offset,lastFragment,to_version)
            ret=self.SSH.execute(cmd)
            result = (ret[-1]).strip()
            if result != "return=0":
                print ("cmd %s executed failed." % cmd)
                print ret
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),ret[5])
                return 0
            else:
                return 1

    def upgrade_system(self,upgrade_type="hot"):
        '''
        **@Description: Execute the upgrade process after the package downloading is over**

        - @param1: [String] upgrade_type: DEFAULT is "hot"

        - @return: code: 0: failed; 1: successful

        '''
        print("==== Run Upgrade_System ...")
        cmd='xcli.py upgrade_system upgrade_type=%s; echo return=$?' % upgrade_type

        ret=self.SSH.execute(cmd)
        len2 = ret.__len__()
        result = (ret[-1]).strip()
        if result != "return=0":
            print ("cmd %s executed failed." % cmd)
            for line in ret:
                print line
            return 0

        return 1

    def upgrade_get_status(self):
        '''
        **@Description: Abort the download process of upgrade.**

        - @return: [Dict]: status dict dump from 'upgrade_get_status'

        '''
        print("==== Get Upgrade Status...")
        cmd='xcli.py upgrade_get_status -z 2>&1; echo return=$?'
        state_info_dict={}
        ret=self.SSH.execute(cmd)
        len2 = ret.__len__()
        result = (ret[-1]).strip()
        if result != "return=0":
            print ("cmd %s executed failed." % cmd)
            print ret
            return 0
        else:
            for line in ret[0:len2]:
                pair=line.split()
                len=pair.__len__()
                if len >= 2:
                    value_str = ""
                    for i in range(1, len):
                        value_str += pair[i]+" "
                    value = value_str
                else:
                    value = ""

                state_info_dict[pair[0]]=value
            print "state_info_dict:"+str(state_info_dict)

        return state_info_dict


    def waitUntilUpgradeStatus(self,upgrade_state):
        '''
        **@Description: Loop to wait until the 'upgrade_state' to be the same with target upgrade_status.**

        ** About with 0 if any error happens or timeout(TIMEOUT_UPGRADE_DOWNLOAD).**

        - @param1: [String] upgrade_state: The target upgrade_state.
        - @return: code: 0: failed. 1:successful

        '''
        print("==== Wait Until : %s" % upgrade_state)
        upgrade_state_info=self.upgrade_get_status()
        if not upgrade_state_info:
            return 0
        cur_upgrade_state=upgrade_state_info["upgrade_state"].lower().strip()
        upgrade_state=upgrade_state.lower().strip()

        time_a=time.time()
        time_b=time_a
        cost_time=time_b-time_a

        print("[DEBUG] cur_upgrade_state:####%s####" % cur_upgrade_state)
        print("[DEBUG]     upgrade_state:####%s####" % upgrade_state)

        while cur_upgrade_state != upgrade_state and cost_time<TIMEOUT_UPGRADE_DOWNLOAD:
            time.sleep(20)
            upgrade_state_info=self.upgrade_get_status()
            print ("upgrade_state_info: %s " % str(upgrade_state_info))

            if not upgrade_state_info :
                return 0
            cur_upgrade_state=upgrade_state_info["upgrade_state"].lower().strip(" ")

            print("[DEBUG] cur_upgrade_state:####%s####" % cur_upgrade_state)
            print("[DEBUG]     upgrade_state:####%s####" % upgrade_state)

            #Check if get failure info in upgrade_state, get event and print it to the console
            if cur_upgrade_state == "upgrade failed. see failure reason":
                print "[EROOR] Upgrade Failed. See failure reason from evnet."
                return 0

            time_b=time.time()
            cost_time=time_b-time_a
            print "[DEBUG] cost_time: %s" % str(cost_time)

        if cur_upgrade_state != upgrade_state:
            print "Timeout!!"
            return 0

        return 1
