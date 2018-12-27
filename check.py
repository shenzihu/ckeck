# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys, json,re
from device import *
from common import *

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


class Check(QtGui.QWidget):
    def __init__(self):
        super(Check, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(600, 500)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.textGroupBox = QtGui.QGroupBox("Please Input the VBS")
        self.textGroupBox.setObjectName(_fromUtf8("groupBoxText"))
        self.textTextEdit = QtGui.QPlainTextEdit()
        self.textTextEdit.setObjectName(_fromUtf8("textTextEdit"))
        self.textTextEdit.appendPlainText(_fromUtf8(
"""格式为（check时,请将此行删去）: 
{
    "steps":["cmd1","cmd2"],
    "result":"cmd"
}
        """))
        self.ipLabel = QLabel(_fromUtf8("IP Adress:"))
        self.ipInput = QLineEdit()
        ip = "127.0.0.1"
        if getIP() is not None:
            ip = getIP()
        self.ipInput.setText(_fromUtf8(ip))
        self.ipGridLayout = QGridLayout()
        self.ipGridLayout.addWidget(self.ipLabel,0,0,1,1,Qt.AlignLeft)
        self.ipGridLayout.addWidget(self.ipInput, 0,1,1,8,Qt.AlignLeft)

        self.groupBoxTextVerLayout = QVBoxLayout()
        self.groupBoxTextVerLayout.addLayout(self.ipGridLayout)
        self.groupBoxTextVerLayout.addWidget(self.textTextEdit)

        self.textGroupBox.setLayout(self.groupBoxTextVerLayout)

        self.checkBox = QPushButton("Check")
        self.checkBox.setFixedWidth(80)
        self.checkBoxLayout = QHBoxLayout()
        self.checkBoxLayout.addWidget(self.checkBox, 0, Qt.AlignRight)
        self.checkBox.clicked.connect(self.check)

        self.groupBox = QtGui.QGroupBox("Console")
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.consoleTextEdit = QtGui.QPlainTextEdit()
        self.consoleTextEdit.setObjectName(_fromUtf8("consoleTextEdit"))
        self.consoleTextEdit.setReadOnly(True)
        self.groupBoxVerLayout = QVBoxLayout()
        self.groupBoxVerLayout.addWidget(self.consoleTextEdit)
        self.groupBox.setLayout(self.groupBoxVerLayout)

        self.verticalLayout.addWidget(self.textGroupBox)
        self.verticalLayout.addLayout(self.checkBoxLayout)
        self.verticalLayout.addWidget(self.groupBox)

        Form.setLayout(self.verticalLayout)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.consoleTextEdit.appendPlainText(_fromUtf8("---------------- Start check your input ---------------"))
#         self.consoleTextEdit.appendPlainText(_fromUtf8("""
# The demo likes that:
# {
#     "steps":["cmd1","cmd2"],
#     "result":"cmd"
# }
#         """))

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Check", None))

    def log(self, msg):
        logStr = '[%s]: %s' % (now(), msg)
        self.consoleTextEdit.appendPlainText(_fromUtf8(logStr))

    def check(self):
        self.log("*********正在初始化设备*********")
        if(not self.initDevice()):
            self.log("*********初始化设备失败*********")
            return
        self.log("*********初始化设备成功*********")
        plainText = unicode(self.textTextEdit.toPlainText())
        try:
            jsonObj = json.loads(plainText)
        except ValueError ,e:
            self.log("json 格式错误")
            print e.message
        if(not self.checkInput(jsonObj)):
            self.log("json 格式内容错误")
        steps = jsonObj["steps"]
        for step in steps:
            self.device.write_string(step, 1)
            self.log("executing the cmd %s " % step)
        time.sleep(2)
        self.log("sleep %s s" % 2)
        result = jsonObj["result"]
        if(result):
            re = self.device.read_string()
            self.log("executing the resultCmd %s " % result)
            self.log("Result:%s" % re)

    def initDevice(self):
        ip = self.ipInput.text()
        pattern = re.compile(ur'(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}')
        if(pattern.match(ip) == None):
            self.log("请输入正确的ip地址")
            return False
        setIP(ip)
        self.device = Device(ip)
        self.device.connect()
        return True

    def checkInput(self, jsonObj):
        try:
            jsonObj["steps"]
            jsonObj["result"]
        except KeyError,err:
           self.log("数据格式错误")
           return  False
        return True

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Check()
    win.show()
    app.exec_()
