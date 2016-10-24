# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J:\XIV_AUTO\mytest\install_tool\Gui_.ui'
#
# Created: Thu Apr 02 11:20:41 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from check_host import Check_Host
import time
import ConfigParser
from fresh_installxiv import Fresh_Install
from code_upgradexiv import Code_Upgrade

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

class Ui_MainWindow(object):
    def __init__(self,parent=None):
        pass

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1008, 525)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.test = QtGui.QPushButton(self.centralwidget)
        self.test.setGeometry(QtCore.QRect(270, 80, 75, 23))
        self.test.setObjectName(_fromUtf8("test"))
        self.clear = QtGui.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(270, 120, 75, 23))
        self.clear.setObjectName(_fromUtf8("clear"))
        self.host_text = QtGui.QLineEdit(self.centralwidget)
        self.host_text.setGeometry(QtCore.QRect(130, 40, 111, 20))
        self.host_text.setObjectName(_fromUtf8("host_text"))
        self.username_text = QtGui.QLineEdit(self.centralwidget)
        self.username_text.setGeometry(QtCore.QRect(130, 80, 113, 20))
        self.username_text.setObjectName(_fromUtf8("username_text"))
        self.password_text = QtGui.QLineEdit(self.centralwidget)
        self.password_text.setGeometry(QtCore.QRect(130, 120, 113, 20))
        self.password_text.setObjectName(_fromUtf8("password_text"))
        self.password_text.setEchoMode(QtGui.QLineEdit.Password)
        self.host = QtGui.QLabel(self.centralwidget)
        self.host.setGeometry(QtCore.QRect(90, 40, 31, 16))
        self.host.setObjectName(_fromUtf8("host"))
        self.username = QtGui.QLabel(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(70, 80, 54, 12))
        self.username.setObjectName(_fromUtf8("username"))
        self.password = QtGui.QLabel(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(70, 120, 54, 12))
        self.password.setObjectName(_fromUtf8("password"))
        self.console = QtGui.QTextBrowser(self.centralwidget)
        self.console.setGeometry(QtCore.QRect(20, 210, 431, 241))
        self.console.setObjectName(_fromUtf8("console"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(270, 40, 71, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.xiv_ip_text = QtGui.QLineEdit(self.centralwidget)
        self.xiv_ip_text.setGeometry(QtCore.QRect(760, 40, 141, 20))
        self.xiv_ip_text.setText(_fromUtf8(""))
        self.xiv_ip_text.setObjectName(_fromUtf8("xiv_ip_text"))
        self.xiv_ip = QtGui.QLabel(self.centralwidget)
        self.xiv_ip.setGeometry(QtCore.QRect(690, 40, 54, 12))
        self.xiv_ip.setObjectName(_fromUtf8("xiv_ip"))
        self.xiv_name_text = QtGui.QLineEdit(self.centralwidget)
        self.xiv_name_text.setGeometry(QtCore.QRect(540, 40, 121, 20))
        self.xiv_name_text.setText(_fromUtf8(""))
        self.xiv_name_text.setObjectName(_fromUtf8("xiv_name_text"))
        self.xiv_name = QtGui.QLabel(self.centralwidget)
        self.xiv_name.setGeometry(QtCore.QRect(480, 40, 51, 20))
        self.xiv_name.setObjectName(_fromUtf8("xiv_name"))
        self.xiv_tar_name = QtGui.QLabel(self.centralwidget)
        self.xiv_tar_name.setGeometry(QtCore.QRect(463, 80, 71, 20))
        self.xiv_tar_name.setObjectName(_fromUtf8("xiv_tar_name"))
        self.xiv_tar_name_text = QtGui.QLineEdit(self.centralwidget)
        self.xiv_tar_name_text.setGeometry(QtCore.QRect(540, 80, 371, 20))
        self.xiv_tar_name_text.setText(_fromUtf8(""))
        self.xiv_tar_name_text.setObjectName(_fromUtf8("xiv_tar_name_text"))
        self.xiv_tar_path = QtGui.QLabel(self.centralwidget)
        self.xiv_tar_path.setGeometry(QtCore.QRect(460, 120, 71, 20))
        self.xiv_tar_path.setObjectName(_fromUtf8("xiv_tar_path"))
        self.xiv_tar_path_text = QtGui.QLineEdit(self.centralwidget)
        self.xiv_tar_path_text.setGeometry(QtCore.QRect(540, 120, 371, 20))
        self.xiv_tar_path_text.setText(_fromUtf8(""))
        self.xiv_tar_path_text.setObjectName(_fromUtf8("xiv_tar_path_text"))
        self.console_2 = QtGui.QTextBrowser(self.centralwidget)
        self.console_2.setGeometry(QtCore.QRect(490, 210, 491, 241))
        self.console_2.setObjectName(_fromUtf8("console_2"))
        self.copytarball = QtGui.QPushButton(self.centralwidget)
        self.copytarball.setGeometry(QtCore.QRect(520, 150, 81, 23))
        self.copytarball.setObjectName(_fromUtf8("copytarball"))
        self.oneclear = QtGui.QPushButton(self.centralwidget)
        self.oneclear.setGeometry(QtCore.QRect(770, 180, 75, 23))
        self.oneclear.setObjectName(_fromUtf8("oneclear"))
        self.clickinstall = QtGui.QPushButton(self.centralwidget)
        self.clickinstall.setGeometry(QtCore.QRect(610, 150, 91, 23))
        self.clickinstall.setObjectName(_fromUtf8("clickinstall"))
        self.oneclickinstall = QtGui.QPushButton(self.centralwidget)
        self.oneclickinstall.setGeometry(QtCore.QRect(520, 470, 201, 23))
        self.oneclickinstall.setObjectName(_fromUtf8("oneclickinstall"))
        self.host_cmd_text = QtGui.QLineEdit(self.centralwidget)
        self.host_cmd_text.setGeometry(QtCore.QRect(90, 170, 361, 20))
        self.host_cmd_text.setObjectName(_fromUtf8("host_cmd_text"))
        self.host_cmd = QtGui.QLabel(self.centralwidget)
        self.host_cmd.setGeometry(QtCore.QRect(20, 170, 51, 20))
        self.host_cmd.setObjectName(_fromUtf8("host_cmd"))
        self.copyupgradeball = QtGui.QPushButton(self.centralwidget)
        self.copyupgradeball.setGeometry(QtCore.QRect(710, 150, 101, 23))
        self.copyupgradeball.setObjectName(_fromUtf8("copyupgradeball"))

        self.getconf = QtGui.QPushButton(self.centralwidget)
        self.getconf.setGeometry(QtCore.QRect(520, 180, 75, 23))
        self.getconf.setObjectName(_fromUtf8("getconf"))

        self.example = QtGui.QPushButton(self.centralwidget)
        self.example.setGeometry(QtCore.QRect(610, 180, 75, 23))
        self.example.setObjectName(_fromUtf8("example"))
        self.clickupgrade = QtGui.QPushButton(self.centralwidget)
        self.clickupgrade.setGeometry(QtCore.QRect(820, 150, 91, 23))
        self.clickupgrade.setObjectName(_fromUtf8("clickupgrade"))
        self.oneclickupgrade = QtGui.QPushButton(self.centralwidget)
        self.oneclickupgrade.setGeometry(QtCore.QRect(760, 470, 201, 23))
        self.oneclickupgrade.setObjectName(_fromUtf8("oneclickupgrade"))
        self.oneclickupgrade.setDisabled(True)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.test, QtCore.SIGNAL(_fromUtf8("clicked()")),self.test_check_host)

        QtCore.QObject.connect(self.clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clear_text)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL(_fromUtf8("activated(QString)")),self.default_host)

        QtCore.QObject.connect(self.copytarball, QtCore.SIGNAL(_fromUtf8("clicked()")), self.copy_tar_ball)
        QtCore.QObject.connect(self.clickinstall, QtCore.SIGNAL(_fromUtf8("clicked()")), self.click_install)

        QtCore.QObject.connect(self.copyupgradeball, QtCore.SIGNAL(_fromUtf8("clicked()")), self.copy_upgrade_ball)
        QtCore.QObject.connect(self.clickupgrade, QtCore.SIGNAL(_fromUtf8("clicked()")), self.click_upgrade)

        QtCore.QObject.connect(self.oneclear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.one_clear)
        QtCore.QObject.connect(self.getconf, QtCore.SIGNAL(_fromUtf8("clicked()")), self.get_conf)
        QtCore.QObject.connect(self.example, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_default)

        QtCore.QObject.connect(self.oneclickinstall, QtCore.SIGNAL(_fromUtf8("clicked()")), self.one_click_install)
        QtCore.QObject.connect(self.oneclickupgrade, QtCore.SIGNAL(_fromUtf8("clicked()")), self.one_clickup_grade)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Fresh Install XIV Tool---Wayne", None))
        self.test.setText(_translate("MainWindow", "Test", None))
        self.clear.setText(_translate("MainWindow", "Clear", None))
        self.host.setText(_translate("MainWindow", "Host", None))
        self.username.setText(_translate("MainWindow", "Username", None))
        self.password.setText(_translate("MainWindow", "Password", None))
        self.comboBox.setItemText(0, _translate("MainWindow", " -----", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "China", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "Israel", None))
        self.xiv_ip.setText(_translate("MainWindow", "XIV_ip", None))
        self.xiv_name.setText(_translate("MainWindow", "XIV_name", None))
        self.xiv_tar_name.setText(_translate("MainWindow", "XIV_tar_name", None))
        self.xiv_tar_path.setText(_translate("MainWindow", "XIV_tar_path", None))
        self.copytarball.setText(_translate("MainWindow", "CopyTarBall", None))
        self.oneclear.setText(_translate("MainWindow", "OneClear", None))
        self.clickinstall.setText(_translate("MainWindow", "ClickInstall", None))
        self.oneclickinstall.setText(_translate("MainWindow", "OneClickInstall", None))
        self.host_cmd.setText(_translate("MainWindow", "Host_cmd", None))
        self.copyupgradeball.setText(_translate("MainWindow", "CopyUpgradeBall", None))
        self.clickupgrade.setText(_translate("MainWindow", "ClickUpgrade", None))
        self.oneclickupgrade.setText(_translate("MainWindow", "OneClickUpgrade", None))
        self.example.setText(_translate("MainWindow", "Example", None))
        self.getconf.setText(_translate("MainWindow", "GetConf", None))

    #-------------------
    def copy_upgrade_ball(self):
        if self.check_xiv_text() == 0 or self.check_host_text() == 0:
            error_msg = time.strftime('%H:%M:%S') +":  Failed to conncet Host or XIV "
            self.console_2.append(error_msg)
            print error_msg
            return 0
        else:
            local_xiv_name =  str(QtCore.QString(self.xiv_name_text.text())).strip()
            local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()
            local_xiv_tar_path =  str(QtCore.QString(self.xiv_tar_path_text.text())).strip()
            local_xiv_tar_name =  str(QtCore.QString(self.xiv_tar_name_text.text())).strip()

            host_ip = str(QtCore.QString(self.host_text.text())).strip()
            host_username = str(QtCore.QString(self.username_text.text())).strip()
            host_password = str(QtCore.QString(self.password_text.text())).strip()

            self.thread_copy_upgrade_tar_ball = Code_Upgrade(host_ip,host_username,host_password,local_xiv_name,local_xiv_ip,local_xiv_tar_path,local_xiv_tar_name,copy_flag=True)
            QtCore.QObject.connect(self.thread_copy_upgrade_tar_ball, QtCore.SIGNAL(_fromUtf8('output(QString)')),self.xiv_result)
            self.thread_copy_upgrade_tar_ball.start()
            return 1

    def click_upgrade(self):
        local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()
        local_xiv_tar_name =  str(QtCore.QString(self.xiv_tar_name_text.text())).strip()
        if local_xiv_ip == "":
            self.console_2.setText("The XIV ip is blank")
            return 0
        else:
            self.thread_click_upgrade = Code_Upgrade(xiv_ip=local_xiv_ip,xiv_tar_name=local_xiv_tar_name,upgrade_flag=True)
            QtCore.QObject.connect(self.thread_click_upgrade, QtCore.SIGNAL(_fromUtf8('output(QString)')),self.xiv_result)
            self.thread_click_upgrade.start()
            return 1


    def one_clickup_grade(self):
        return 1
   #------------------

   #----host--------------------------------

    def check_host_text(self):
        host_ip = str(QtCore.QString(self.host_text.text())).strip()
        host_username = str(QtCore.QString(self.username_text.text())).strip()
        host_password = str(QtCore.QString(self.password_text.text())).strip()

        if  host_ip=="" or host_username=="":
             return 0
        return 1

    def clear_text(self):
        self.host_text.clear()
        self.username_text.clear()
        self.password_text.clear()
        self.console.clear()
        return 1

    def default_host(self):
        if int(self.comboBox.currentIndex()) == 0:
            self.host_text.setText("")
            self.username_text.setText("")
            self.password_text.setText("")
        if int(self.comboBox.currentIndex()) == 1:
            self.host_text.setText("9.115.249.158")
            self.username_text.setText("root")
            self.password_text.setText("CSTLfvt")
            self.host_cmd_text.setText("ls -d /local/system_build_from_GSA/*")
        if int(self.comboBox.currentIndex()) == 2:
            self.host_text.setText("9.151.158.96")
            self.username_text.setText("wenqiz")
            self.password_text.setText("")
            self.host_cmd_text.setText("ls -d /a/system_build/leia/11.6*")

    def test_check_host(self):
        self.console.clear()
        host_ip = str(QtCore.QString(self.host_text.text()))
        host_username = str(QtCore.QString(self.username_text.text()))
        host_password = str(QtCore.QString(self.password_text.text()))
        host_cmd = str(QtCore.QString(self.host_cmd_text.text()))

        self.thread1 = Check_Host(host_ip,host_username,host_password,host_cmd)
        QtCore.QObject.connect(self.thread1, QtCore.SIGNAL(_fromUtf8('output(QString)')),self.host_result)
        self.thread1.start()
        return 1

    def host_result(self,msg):
        self.console.setText(msg)
        return  1
    #-----xiv----------------------------------

    def set_default(self):
        self.xiv_ip_text.setText("9.151.152.95")
        self.xiv_name_text.setText("Gen3P1-28")
        self.xiv_tar_name_text.setText("ixss-gen3-11.6.0-2015.05.18-155109-git-b4cffccfba3f.tar.gz")
        self.xiv_tar_path_text.setText("/a/system_build/leia/11.6.0")

    def check_xiv_text(self):
         local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()
         local_xiv_name =  str(QtCore.QString(self.xiv_name_text.text())).strip()
         local_xiv_tar_name =  str(QtCore.QString(self.xiv_tar_name_text.text())).strip()
         local_xiv_tar_path =  str(QtCore.QString(self.xiv_tar_path_text.text())).strip()

         if  local_xiv_ip=="" or local_xiv_name=="" or local_xiv_tar_name=="" or local_xiv_tar_path=="":
             return 0
         return 1

    def get_conf(self):
        local_xiv_name =  str(QtCore.QString(self.xiv_name_text.text())).strip()
        local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()
        self.thread_copy_conf = Fresh_Install(xiv_name=local_xiv_name,xiv_ip=local_xiv_ip,copy_conf_flag=True)
        QtCore.QObject.connect(self.thread_copy_conf, QtCore.SIGNAL(_fromUtf8('output(QString)')),self.xiv_result)
        self.thread_copy_conf.start()
        return 1

    def copy_tar_ball(self):
        if self.check_xiv_text() == 0 or self.check_host_text() == 0:
            error_msg = time.strftime('%H:%M:%S') +":  Failed to conncet Host or XIV "
            self.console_2.append(error_msg)
            print error_msg
            return 0
        else:
            local_xiv_name =  str(QtCore.QString(self.xiv_name_text.text())).strip()
            local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()
            local_xiv_tar_path =  str(QtCore.QString(self.xiv_tar_path_text.text())).strip()
            local_xiv_tar_name =  str(QtCore.QString(self.xiv_tar_name_text.text())).strip()

            host_ip = str(QtCore.QString(self.host_text.text())).strip()
            host_username = str(QtCore.QString(self.username_text.text())).strip()
            host_password = str(QtCore.QString(self.password_text.text())).strip()

            self.thread_copy_tar_ball = Fresh_Install(host_ip,host_username,host_password,local_xiv_name,local_xiv_ip,local_xiv_tar_path,local_xiv_tar_name,copy_flag=True)
            QtCore.QObject.connect(self.thread_copy_tar_ball, QtCore.SIGNAL(_fromUtf8('output(QString)')),self.xiv_result)
            self.thread_copy_tar_ball.start()
            return 1

    def click_install(self):
        local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()
        if local_xiv_ip == "":
            self.console_2.setText("The XIV ip is blank")
            return 0
        else:
            self.thread_click_install = Fresh_Install(xiv_ip=local_xiv_ip,install_flag=True)
            QtCore.QObject.connect(self.thread_click_install, QtCore.SIGNAL(_fromUtf8('output(QString)')),self.xiv_result)
            self.thread_click_install.start()
            return 1

    def one_click_install(self):
        self.console_2.clear()
        if self.check_xiv_text() == 0 or self.check_host_text() == 0:
            error_msg = time.strftime('%H:%M:%S') +":  Failed to conncet Host or XIV "
            self.console_2.append(error_msg)
            print error_msg
            return 0
        else:
            local_xiv_name =  str(QtCore.QString(self.xiv_name_text.text())).strip()
            local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()
            local_xiv_tar_path =  str(QtCore.QString(self.xiv_tar_path_text.text())).strip()
            local_xiv_tar_name =  str(QtCore.QString(self.xiv_tar_name_text.text())).strip()

            host_ip = str(QtCore.QString(self.host_text.text())).strip()
            host_username = str(QtCore.QString(self.username_text.text())).strip()
            host_password = str(QtCore.QString(self.password_text.text())).strip()

            local_xiv_ip =  str(QtCore.QString(self.xiv_ip_text.text())).strip()

            if local_xiv_ip == "":
                self.console_2.setText("The XIV ip is blank")
                return 0
            else:
                self.thread_copy_tar_ball_install = Fresh_Install(host_ip,host_username,host_password,local_xiv_name,local_xiv_ip,local_xiv_tar_path,local_xiv_tar_name,copy_conf_flag=True,copy_flag=True,install_flag=True)
                QtCore.QObject.connect(self.thread_copy_tar_ball_install, QtCore.SIGNAL(_fromUtf8('output(QString)')),self.xiv_result)
                self.thread_copy_tar_ball_install.start()


    def xiv_result(self,msg):
        self.console_2.append(msg)
        return 1

    def one_clear(self):
        self.xiv_ip_text.setText("")
        self.xiv_name_text.setText("")
        self.xiv_tar_name_text.setText("")
        self.xiv_tar_path_text.setText("")
    #-----------check host------------------
    #----------------------------------------
