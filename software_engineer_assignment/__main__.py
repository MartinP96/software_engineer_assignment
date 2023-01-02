'''
    File name: main.py
    Version: v0.1
    Date: 23.12.2022
    Desc: Main python script file for software engineer assignment
'''

import time
from software_engineer_assignment.encoder_interface import EncoderInterface
from software_engineer_assignment.gui_main import UiMainWindow

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


def app():
    gui_app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow(main_window)
    main_window.show()
    sys.exit(gui_app.exec_())


if __name__ == '__main__':
    app()

