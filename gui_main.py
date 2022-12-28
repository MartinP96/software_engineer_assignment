import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from encoder_interface import EncoderInterface
import pyqtgraph as pg

from gui_components import ValueIndicator, Label, Button, LineGraph

class EncoderControlTask(QObject):

    encoder_connection_signal = pyqtSignal(int)
    encoder_info_signal = pyqtSignal(dict)
    encoder_data_signal = pyqtSignal(tuple)

    encoder_stop_reading = pyqtSignal(int)

    def __init__(self, test):
        super(EncoderControlTask, self).__init__()

        self.interface = EncoderInterface(64, 16, 19)
        self.test = test

        self.poller = QTimer(self)
        self.poller.timeout.connect(self.read_data)

    def enable_encoder(self, val):
        self.poller.start(100)

    def disable_encoder(self):
        self.poller.stop()

    def connect_encoder(self, val):
        response = self.interface.connect_interface()
        if response != -1:
            self.encoder_info_signal.emit(response)
        else:
            self.encoder_info_signal.emit(-1)

    def disconnect_encoder(self, val):
        self.interface.disconnect_interface()

    def read_data(self):
        data = self.interface.read_encoder_data()
        self.encoder_data_signal.emit(data)

class UiMainWindow(QObject):

    encoder_connect_signal = pyqtSignal(int)
    encoder_disconnect_signal = pyqtSignal(int)
    encoder_enable_signal = pyqtSignal(int)
    encoder_disable_signal = pyqtSignal(int)

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
        self.enable_encoder_button = Button("enable_button", self.centralwidget, (20, 60, 131, 28), "ENABLE ENCODER", self.enable_encoder, True, False)
        self.disable_encoder_button = Button("disable_button", self.centralwidget, (160, 60, 131, 28), "DISABLE ENCODER", self.disable_encoder, False, False)
        self.connect_button = Button("connect_button", self.centralwidget, (20, 20, 131, 28), "CONNECT", self.connect_to_encoder, True)
        self.disconnect_button = Button("disconnect_button", self.centralwidget, (160, 20, 131, 28), "DISCONNECT", self.disconnect_encoder, False)

        # Graph object
        self.position_plot = LineGraph(main_window, "Position", 0.1, 1000, "Time [s]", "Position [°]", (20, 120, 700, 450))

        # Main window
        main_window.setCentralWidget(self.centralwidget)
        main_window.setWindowTitle("Encoder Interface")

        # Start thread tasks
        self.run_encoder_task()

    # Methods
    def run_encoder_task(self):

        self.thread = QThread()
        self.worker = EncoderControlTask("This is a test!")
        self.worker.moveToThread(self.thread)

        # Slots and Signals
        self.encoder_connect_signal.connect(self.worker.connect_encoder)
        self.encoder_disconnect_signal.connect(self.worker.disconnect_encoder)
        self.encoder_enable_signal.connect(self.worker.enable_encoder)
        self.encoder_disable_signal.connect(self.worker.disable_encoder)

        self.worker.encoder_info_signal.connect(self.display_encoder_connection_status)
        self.worker.encoder_data_signal.connect(self.display_encoder_data)
        self.thread.start()

    def connect_to_encoder(self):
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.encoder_connect_signal.emit(1)

    def disconnect_encoder(self):
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.encoder_disconnect_signal.emit(1)
        self.com_port_indicator.set_indicator_value("")
        self.device_indicator.set_indicator_value("")
        self.enable_encoder_button.setVisible(False)
        self.disable_encoder_button.setVisible(False)

    def enable_encoder(self):
        self.enable_encoder_button.setEnabled(False)
        self.disable_encoder_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.encoder_enable_signal.emit(1)

    def disable_encoder(self):
        self.enable_encoder_button.setEnabled(True)
        self.disable_encoder_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.mt_pos_indicator.set_indicator_value("")
        self.st_pos_indicator.set_indicator_value("")
        self.encoder_disable_signal.emit(1)
        self.position_plot.clear_graph()

    def display_encoder_connection_status(self, data):
        if data["status"] == "connected":
            self.com_port_indicator.set_indicator_value(data["com_port"])
            self.device_indicator.set_indicator_value(data["version"])
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.enable_encoder_button.setVisible(True)
            self.disable_encoder_button.setVisible(True)
        else:
            self.com_port_indicator.set_indicator_value("")
            self.device_indicator.set_indicator_value("")
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)

    def display_encoder_data(self, data):
        self.mt_pos_indicator.set_indicator_value(str(data[0]))
        pos_str = f"{str(round(data[1], 4))}°"
        self.st_pos_indicator.set_indicator_value(pos_str)
        self.position_plot.update_graph(data[1])

