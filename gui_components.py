from PyQt5 import QtCore, QtGui, QtWidgets

class ValueIndicator(QtWidgets.QLabel):

    # Constructor
    def __init__(self, object_name, parent, dimensions, font_size, text_aligment=QtCore.Qt.AlignCenter):
        super(ValueIndicator, self).__init__(parent)
        self.object_name = object_name
        self.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        self.setAutoFillBackground(False)
        self.setStyleSheet(
            "border-top: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(64, 64, 64, 255));\n"
            "border-left: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(64, 64, 64, 255));\n"
            "border-right: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "border-bottom: 2px solid qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
            "stop:0 rgba(192, 192, 192, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "background-color: rgb(226, 226, 226);")
        self.setAlignment(text_aligment)
        self.setObjectName(object_name)
        self.setText("")

    # Methods
    def set_indicator_value(self, value):
        self.setText(value)

class Label(QtWidgets.QLabel):
    def __init__(self, object_name, parent, dimensions, font_size, label_text):
        super(Label, self).__init__(parent)
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