# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shortcut.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(282, 250)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setStyleSheet("QFrame{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0.511, stop:0 rgba(66, 167, 245, 255), stop:1 rgba(149, 113, 227, 255));\n"
"    border-radius : 5px;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(10, 190, 133, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox.setFont(font)
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setCheckable(True)
        self.checkBox.setObjectName("checkBox")
        self.treeWidget = QtWidgets.QTreeWidget(self.frame)
        self.treeWidget.setGeometry(QtCore.QRect(0, 10, 260, 190))
        self.treeWidget.setStyleSheet("QTreeWidget{\n"
"    border-radius : 5px;\n"
"}")
        self.treeWidget.setAllColumnsShowFocus(False)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget.headerItem().setBackground(0, QtGui.QColor(192, 167, 255))
        self.treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.treeWidget.headerItem().setBackground(1, QtGui.QColor(192, 167, 255))
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        item_0.setFont(0, font)
        font = QtGui.QFont()
        font.setPointSize(13)
        item_0.setFont(1, font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.CrossPattern)
        item_0.setForeground(1, brush)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        item_0.setFont(0, font)
        font = QtGui.QFont()
        font.setPointSize(13)
        item_0.setFont(1, font)
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(170, 200, 75, 26))
        self.pushButton.setStyleSheet("QPushButton{\n"
"    background-color: rgb(225, 225, 225);\n"
"    border-radius : 3px;\n"
"    border: 2px solid #5fa2fa;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(225, 225, 225);\n"
"    border-radius : 3px;\n"
"    border: 3px solid #0d76ff;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Shortcut"))
        self.checkBox.setText(_translate("Dialog", "دیگر نشان نده"))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "شورتکات"))
        self.treeWidget.headerItem().setText(1, _translate("Dialog", "توضیحات"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Dialog", "TAB"))
        self.treeWidget.topLevelItem(0).setText(1, _translate("Dialog", "Next line"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Dialog", "CTRL+R"))
        self.treeWidget.topLevelItem(1).setText(1, _translate("Dialog", "RUN"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("Dialog", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
