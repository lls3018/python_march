import paramiko
import os
import util.Env
import util.Connection

# New SSHClient
from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Check_Host(QtCore.QThread):
    def __init__(self,host_ip,user,passwd,cmd):
        QtCore.QThread.__init__(self)
        self.host_ip = host_ip;
        self.user = user
        self.passwd = passwd
        self.cmd = cmd

        self.exiting = False
        self.isWait=False
        self.data={}
    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        (ret,ret_content) = self.check_host(self.host_ip,self.user,self.passwd,self.cmd)
        if int(ret) == 1:
            #self.console.setText("host connect succefully")
            self.emit(QtCore.SIGNAL(_fromUtf8('output(QString)')),ret_content)
        else:
            self.emit(QtCore.SIGNAL('output(QString)'),"Authentication failed")

    def check_host(self,host_ip,user,passwd,cmd):
        try:
            if passwd:
                 ssh = util.Connection.Connection(host=host_ip,
                                         username=user,
                                        password=passwd)
            else:
                ssh = util.Connection.Connection(host=host_ip,
                                         username=user,
                                        private_key=util.Env.id_rsa)
            ret = ssh.execute(cmd)
            ret_content = ''.join(ret)
            return (1,ret_content)

        except Exception, e:
            print '%s,\tError\t'%(host_ip)
            print e
            return (0,e)