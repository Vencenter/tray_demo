# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets as  QtGui
from PyQt5 import QtCore
import os


class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'定时关机')
        self.resize(300, 150)

        self.leName = QtGui.QLineEdit(self)
        self.leName.setPlaceholderText(u'预计关机时间时长设定(min)')

        self.pbLogin = QtGui.QPushButton(u'确定', self)
        self.pbCancel = QtGui.QPushButton(u'取消', self)

        self.horizontalGroupBox = QtGui.QGroupBox("login")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.leName)
        self.horizontalGroupBox.setLayout(layout)

        self.pbLogin.clicked.connect(self.login)
        self.pbCancel.clicked.connect(self.recancel)

        layout1 = QtGui.QVBoxLayout()
        layout1.addWidget(self.horizontalGroupBox)

        # 放一个间隔对象美化布局
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout1.addItem(spacerItem)

        # 按钮布局
        buttonLayout = QtGui.QHBoxLayout()
        # 左侧放一个间隔
        spancerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        buttonLayout.addItem(spancerItem2)
        buttonLayout.addWidget(self.pbLogin)
        buttonLayout.addWidget(self.pbCancel)

        layout1.addLayout(buttonLayout)

        self.setLayout(layout1)

    def login(self):
        gettime= int(self.leName.text())*60
        if gettime!="":
            com="shutdown -s -t "+str(gettime)
            os.system(com)
        else:
            pass
    def recancel(self):
        com="shutdown /a"
        os.system(com)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec_())
