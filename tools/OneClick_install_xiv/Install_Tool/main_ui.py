__author__ = 'Wayne-PC'

from PyQt4 import QtCore, QtGui
from install_tool import Ui_MainWindow
import sys

class Ui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(1000, 520)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())