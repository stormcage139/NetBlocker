# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"NetworkBlocker")
        MainWindow.resize(1101, 608)
        MainWindow.setStyleSheet(u"QMainWindow { background-color: #1e1e1e; }\n"
"QTableWidget { \n"
"    background-color: #2b2b2b; \n"
"    color: #ffffff; \n"
"    border: 1px solid #3f3f3f;\n"
"    gridline-color: #3f3f3f;\n"
"}\n"
"QPushButton { \n"
"    background-color: #0078d4; \n"
"    color: white; \n"
"    border-radius: 4px; \n"
"    padding: 5px 15px; \n"
"}\n"
"QPushButton:hover { background-color: #2b88d8; }")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ProcessSearch = QLineEdit(self.centralwidget)
        self.ProcessSearch.setObjectName(u"ProcessSearch")

        self.gridLayout.addWidget(self.ProcessSearch, 0, 0, 1, 1)

        self.ToggleButton = QPushButton(self.centralwidget)
        self.ToggleButton.setObjectName(u"ToggleButton")

        self.gridLayout.addWidget(self.ToggleButton, 0, 1, 1, 1)

        self.ReloadButton = QPushButton(self.centralwidget)
        self.ReloadButton.setObjectName(u"ReloadButton")

        self.gridLayout.addWidget(self.ReloadButton, 0, 2, 1, 1)

        self.processTable = QTableWidget(self.centralwidget)
        if (self.processTable.columnCount() < 5):
            self.processTable.setColumnCount(5)
        self.processTable.setObjectName(u"processTable")
        self.processTable.setColumnCount(5)

        self.gridLayout.addWidget(self.processTable, 1, 0, 1, 3)

        self.StatusLabel = QLabel(self.centralwidget)
        self.StatusLabel.setObjectName(u"StatusLabel")
        self.StatusLabel.setStyleSheet(u"text-align: center;")

        self.gridLayout.addWidget(self.StatusLabel, 2, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ToggleButton.setText(QCoreApplication.translate("MainWindow", u"ToggleBlock", None))
        self.ReloadButton.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.StatusLabel.setText(QCoreApplication.translate("MainWindow", u"TEXT", None))
    # retranslateUi

