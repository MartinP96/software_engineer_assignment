import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from encoder_interface import EncoderInterface

# Widget Classes

class ValueIndicator:

    # Constructor
    def __init__(self, object_name, parent, dimensions, font_size, text_aligment=QtCore.Qt.AlignCenter):
        self.object_name = object_name
        self.indicator = QtWidgets.QLabel(parent)
        self.indicator.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.indicator.setFont(font)
        self.indicator.setAutoFillBackground(False)
        self.indicator.setStyleSheet(
            "border-top: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(64, 64, 64, 255));\n"
            "border-left: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(64, 64, 64, 255));\n"
            "border-right: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "border-bottom: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "background-color: rgb(226, 226, 226);")
        self.indicator.setAlignment(text_aligment)
        self.indicator.setObjectName(object_name)
        self.indicator.setText("0")

    # Methods
    def set_indicator_value(self, value):
        self.indicator.setText(value)

class Label:
    # Constructor
    def __init__(self, object_name, parent, dimensions, font_size, label_text):
        self.object_name = object_name
        self.label = QtWidgets.QLabel(parent)
        self.label.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.label.setFont(font)
        self.label.setObjectName(object_name)
        self.label.setText(label_text)

class Label_2(QtWidgets.QLabel):
    def __init__(self, object_name, parent, dimensions, font_size, label_text):
        super(Label_2, self).__init__(parent)
        self.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        self.setObjectName(object_name)
        self.setText(label_text)

class Button(QtWidgets.QPushButton):
    # Constructor
    def __init__(self, object_name, parent, dimensions, text, method, enabled=True, visibility=True):
        super(Button, self).__init__(parent)
        self.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        self.setObjectName(object_name)
        self.setText(text)
        self.clicked.connect(method)
        self.setEnabled(enabled)
        self.setVisible(visibility)

class UiMainWindow(QObject):

    encoder_connect_signal = pyqtSignal(int)
    encoder_disconnect_signal = pyqtSignal(int)
    encoder_enable_signal = pyqtSignal(int)

    # Constructor
    def __init__(self, main_window):
        super(UiMainWindow, self).__init__()
        main_window.setObjectName("main_window")
        main_window.setFixedSize(935, 698)
        main_window.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # Value Indicator Objects
        self.mt_pos_label = Label("mt_pos_label", self.centralwidget, (30, 600, 231, 31), 14, "Multi Turn Position:")
        self.mt_pos_indicator = ValueIndicator("mt_pos_indicator", self.centralwidget, (30, 640, 231, 41), 14)
        self.st_pos_label = Label("st_pos_label", self.centralwidget, (280, 600, 231, 31), 14, "Single Turn Position:")
        self.st_pos_indicator = ValueIndicator("st_pos_indicator", self.centralwidget, (280, 640, 231, 41), 14)
        self.com_port_label = Label("com_port_label", self.centralwidget, (390, 10, 101, 31), 12, "COM Port:")
        self.com_port_indicator = ValueIndicator("com_port_indicator", self.centralwidget, (490, 10, 91, 31), 12)
        self.device_label = Label("device_label", self.centralwidget, (590, 10, 71, 31), 12, "Device:")
        self.device_indicator = ValueIndicator("device_indicator", self.centralwidget, (660, 10, 121, 31), 9)

        # Button objects
        self.enable_encoder_button = Button("enable_button", self.centralwidget, (20, 60, 131, 28), "ENABLE ENCODER", self.test_print_msg, True, False)
        self.disable_encoder_button = Button("disable_button", self.centralwidget, (160, 60, 131, 28), "DISABLE ENCODER", self.test_print_msg, False, False)
        self.connect_button = Button("connect_button", self.centralwidget, (20, 20, 131, 28), "CONNECT", self.test_print_msg, True)
        self.disconnect_button = Button("disconnect_button", self.centralwidget, (160, 20, 131, 28), "DISCONNECT", self.test_print_msg, False)

        # Main window
        main_window.setCentralWidget(self.centralwidget)
        main_window.setWindowTitle("Encoder Interface")

    def test_print_msg(self):
        print("Button clicked!")
