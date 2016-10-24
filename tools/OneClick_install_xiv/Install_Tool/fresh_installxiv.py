import util.Env
import util.Connection
import urllib
import time
import os

from PyQt4 import QtGui, QtCore
authorID = "wenqiz@cn.ibm.com"

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


class Fresh_Install(QtCore.QThread):
    def __init__(self,host_ip="",host_username="",host_password="",
                 xiv_name="",xiv_ip="",xiv_tar_path="",xiv_tar_name="",copy_conf_flag=False,copy_flag=False,install_flag=False,):

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
        self.copy_conf_flag = copy_conf_flag
        self.copy_flag = copy_flag
        self.install_flag = install_flag

    def __del__(self):
        self.exiting = True
        self.wait()
        if self.SSH is not None:
            self.SSH.close()

    def run(self):
        if self.copy_conf_flag is True:
            self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),    "(1)***** Start get the xiv conf  to XIV *****")
            if self.upload_conf(self.xiv_name):
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')), "(1.1)-----Success get the xiv conf  to XIV-------")
                conf_file = './config.xml'
                if os.path.exists(conf_file):
                    os.remove(conf_file)
                else:
                    pass
                    #print 'no such file:%s' % conf_file
            else:
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')), "(1.1)-----Failed get the xiv conf  to XIV-------")
        if self.copy_flag is True:
            self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(2)***** Start upload the tar ball from Host to XIV *****")
            if self.copyTarFileToSystem(self.host_ip,self.host_username,self.host_password,self.xiv_tar_path+"/"+self.xiv_tar_name):
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(3)***** Start extract the XIV tar ball *****")
                if self.extractXIVTarFile(self.xiv_tar_name):
                    self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"----------Copy Done---------")
                else:
                    self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(3)-----Failed: extract the XIV tar ball---------")
            else:
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(2)-----Failed: upload the tar ball from Host to XIV-------")
        if self.install_flag is True:
            self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(4)***** Start install XIV *****")
            if self.freshInstall():
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(4.1)----Install Done---------")
            else:
                self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),"(4.1)----Install Failed---------")



    def  upload_conf(self,xiv_name):
        '''
         From the sysconf to check the system owner
        '''
        url = "https://sysconf.xiv.ibm.com/systems10/" +xiv_name+"/config.xml"
        urllib.urlretrieve(url, "config.xml")

        local_conf_file='config.xml'
        xiv_conf_file = '/local/scratch/config.xml'
        self.SSH.put(local_conf_file, xiv_conf_file)
        return 1

    def copyTarFileToSystem(self,source_hostname,source_username,source_pwd, filePath, destPath="/local/scratch"):
        '''
        **@Description: Copy the target tarball to xiv system.**

        - @param1: source_hostname: [String] The host that you wanna download the tarball of the target build
        - @param2: source_username: [String] The user allowed to access the source host
        - @param3: source_pwd: [String] The pwd for the source_user
        - @param4: sourceFile: [String] The path on the source host to download the package
        - @param5: destPath: [String] The dest_path you wanna save the package on the xiv
        - @return: code: 0: failed. 1:successful
        '''

        #self.SSH.execute("xcli.py local_storage_clear -u xiv_development -p x1vD3v")
        self.SSH.execute("cd /local/scratch/ ; rm ixss* -rf")
        time.sleep(10)

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

    def extractXIVTarFile(self, fileName, destPath="/local/scratch"):
        '''
        **@Description: Extract the XIV tarball**

        - @param1: fileName: [String] The tar file you wanna extract
        - @param2: filePath: [String] The path of the tar file
        - @return: code: 0: failed. 1:successful
        '''
        print ("=== Extract XIV Tar File...")
        scp_cmd='cd %s; tar -zxvf %s 2>&1; echo return=$?' %(destPath, fileName)
        ret=self.SSH.execute(scp_cmd)
        time.sleep(15)
        if ret[-1].strip() != "return=0":
            print ("scp_cmd %s executed failed." % scp_cmd)
            for line in ret:
                print line
            return 0

        delete_cmd='cd %s; rm %s' %(destPath, fileName)
        ret=self.SSH.execute(delete_cmd)
        return 1


    def freshInstall(self, installPackage="/local/scratch/ixss-*", config_path="/local/scratch/config.xml",
                     upgrade_firmware=False,allow_firmware_downgrade=False):
        '''
        **@Description: To Install the system from the target extracted build package**

        - @param1: installPackage: [String] The target extracted dir for the build package.
        - @param2: upgrade_firmware: [Boolean] If upgrade the firmware during the install process. DEFAULT:  False.
        - @param3: allow_firmware_downgrade: [Boolean] If the firmware_downgrade allowed. DEFAULT:  True.

        - @return: code: 0: failed; 1: successful
        '''

        print("==== Fresh Install the system ...")
        #Export the (a won't fix bug in 11.4)

        scp_cmd0='cd %s;export LD_LIBRARY_PATH="$PWD/root_image/root_image/usr/lib64/";./install.py --install --use-internal-ips --customize-config=xiv' % installPackage
        if upgrade_firmware:
            scp_cmd0 += " --upgrade-firmware"
        if allow_firmware_downgrade:
            scp_cmd0 += " --allow-firmware-downgrade"

        scp_cmd="%s %s ; echo return=$?" % (scp_cmd0,config_path)
        print scp_cmd

        ret=self.SSH.execute(scp_cmd)
        if ret[-1].strip() != "return=0":
            print ("scp_cmd %s executed failed." % scp_cmd)
            for line in ret:
                print line
            return 0
        return 1
