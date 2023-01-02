"""
    File name: gui_components.py
    Date: 02.01.2023
    Desc: gui_main.py
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph

class ValueIndicator(QtWidgets.QLabel):
    """
    Custom class for creating value indicator in PyQt App

    Args:
        object_name(str) - name of gui object
        parent(QWidget) -  parent object of the Gui App
        dimensions(tuple) - dimensions of the Gui element: 0 - len, 1 - hight, 2 - x pos, 3 - y pos
        font_size(int) - font size in the indicator
        text_aligment(str) - aligment of the text in the value indicator

    Attributes:
        object_name(str) - name of the gui object
    """
    def __init__(self, object_name, parent, dimensions, font_size,
                 text_aligment=QtCore.Qt.AlignCenter):
        super().__init__(parent)
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
        """
        Set value of the indicator
        args: value
        return: /
        """
        self.setText(value)


class Label(QtWidgets.QLabel):
    """
    Custom class for creating label widget in PyQt App

    Args:
        object_name(str) - name of gui object
        parent(QWidget) -  parent object of the Gui App
        dimensions(tuple) - dimensions of the Gui element: 0 - len, 1 - hight, 2 - x pos, 3 - y pos
        font_size(int) - font size in the label
        label_text(str) - text of the label

    Attributes:
        object_name(str) - name of the gui object
    """
    def __init__(self, object_name, parent, dimensions, font_size, label_text):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.setFont(font)
        self.setObjectName(object_name)
        self.setText(label_text)

class Button(QtWidgets.QPushButton):
    """
    Custom class for creating button widget in PyQt App

    Args:
        object_name(str) - name of gui object
        parent(QWidget) -  parent object of the Gui App
        dimensions(tuple) - dimensions of the Gui element: 0 - len, 1 - hight, 2 - x pos, 3 - y pos
        text(str) - text of the button
        method - Method that is triggered when the button is pressed
        enabled(bool) - Button enabled when true
        visibility(bool) - Button visible when true
    """
    def __init__(self, object_name, parent, dimensions, text, method,
                 enabled=True, visibility=True):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        self.setObjectName(object_name)
        self.setText(text)
        self.clicked.connect(method)
        self.setEnabled(enabled)
        self.setVisible(visibility)


class LineGraph(pyqtgraph.PlotWidget):
    """
    Custom class for creating graph plot widget in PyQt App

    Args:
        parent(QWidget) -  parent object of the Gui App
        title(str) - title of the plot
        sampling_time(int) - sampling time of input plot data
        buffer_size(int) - size of the plot buffer
        xlabel(str) - x-axis label text
        ylabel(str) - y-axis label text
        dimensions(tuple) - dimensions of the Gui element: 0 - len, 1 - hight, 2 - x pos, 3 - y pos
        pen_color(tuple) - color of the plot (R,G,B)

    Attributes:
        sampling_time(int) - sampling time of the graph data
        buffer_size(int) - size of the data buffers (x and y buffers)
        x_data(list) - x axis (data point) buffer
        y_data(list) - y axis (data point) buffer
    """
    def __init__(self, parent, title="", sampling_time=1, buffer_size=100, xlabel="",
                 ylabel="", dimensions=(0, 0, 10, 10), pen_color=(255, 0, 0)):
        super().__init__(parent)

        self.sampling_time = sampling_time
        self.buffer_size = buffer_size
        self.x_data = [0]
        self.y_data = [0]

        self.setGeometry(dimensions[0], dimensions[1], dimensions[2], dimensions[3])
        self.setBackground('w')
        pen = pyqtgraph.mkPen(color=pen_color)
        self.data_line = self.plot(self.x_data, self.y_data, pen=pen)
        self.setTitle(title)
        styles = {'color': 'r', 'font-size': '20px'}
        self.setLabel('left', ylabel, **styles)
        self.setLabel('bottom', xlabel, **styles)
        self.showGrid(x=True, y=True)

    def update_graph(self, new_y_value):
        """
        Update the plot with new value
        args: new_y_value(int) - new value
        return: /
        """
        if len(self.x_data[1:]) >= self.buffer_size:
            # Remove the first y element.
            self.x_data = self.x_data[1:]
            # Add a new value 1 higher than the last.
            self.x_data.append(self.x_data[-1] + self.sampling_time)
            self.y_data = self.y_data[1:]  # Remove the first
            self.y_data.append(new_y_value)  # Add a new random value.
        else:
            # Add a new value 1 higher than the last
            self.x_data.append(self.x_data[-1] + self.sampling_time)
            self.y_data.append(new_y_value)
        self.data_line.setData(self.x_data, self.y_data)

    def clear_graph(self):
        self.data_line.clear()

class AlarmDisplay(QtWidgets.QTextBrowser):
    """
    Custom class for creating Alarm Display Widget

    Args:
        object_name(str) - name of gui object
        parent(QWidget) -  parent object of the Gui App
        dimensions(tuple) - dimensions of the Gui element: 0 - len, 1 - hight, 2 - x pos, 3 - y pos
    """
    def __init__(self, object_name, parent, dimensions):
        super().__init__(parent)
        # Alarm Display
        self.setGeometry(QtCore.QRect(dimensions[0], dimensions[1], dimensions[2], dimensions[3]))
        self.setObjectName(object_name)
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
