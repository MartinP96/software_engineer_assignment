"""
    File name: gui_main.py
    Date: 02.01.2023
    Desc: gui_main.py
"""

import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from software_engineer_assignment.encoder_interface import EncoderInterface
from software_engineer_assignment.gui_components import ValueIndicator, Label, Button, LineGraph, AlarmDisplay
from software_engineer_assignment.gui_alarm_module import Alarm, AlarmLogger


class EncoderControlTask(QObject):
    """
    EncoderControlTask class for creating seperate python thread for collection data
    from the encoder

    Args: /

    Attributes:
        encoder_connection_signal(pyqtSignal [int]) - signal for sending connection status
        to the main thread
        encoder_info_signal(pyqtSignal [dict]) - signal for sending connection information
        to the main thread
        encoder_data_signal(pyqtSignal [tuple]) - signal for sending measurement data
        to the main thread
        encoder_stop_reading(pyqtSignal [int]) - signal for sending stop signal
        to the main thread
        interface(EncoderInterface) - object for encoder interface
        poller(QTimer) - PyQt timer for pooling measreuement while loop
    """
    encoder_connection_signal = pyqtSignal(int)
    encoder_info_signal = pyqtSignal(dict)
    encoder_data_signal = pyqtSignal(tuple)
    encoder_stop_reading = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.interface = EncoderInterface(64, 16, 19)
        self.poller = QTimer(self)
        self.poller.timeout.connect(self.read_data)

    def enable_encoder(self, val):
        """
        Enable encoder data collection (hardcoded sampling time of 0.1 s) - #possible improvement#
        args: /
        return: /
        """
        self.poller.start(100)

    def disable_encoder(self):
        """
        Disable encoder data collection
        args: /
        return: /
        """
        self.poller.stop()

    def connect_encoder(self, val):
        """
        Connects to the encoder on com port
        args: /
        return: /
        """
        response = self.interface.connect_interface()
        self.encoder_info_signal.emit(response)

    def disconnect_encoder(self, val):
        """
        Disconnect from the encoder
        args: /
        return: /
        """
        self.interface.disconnect_interface()

    def read_data(self):
        """
        Read encoder data
        args: /
        return: /
        """
        data = self.interface.read_encoder_data()
        self.encoder_data_signal.emit(data)


class UiMainWindow(QObject):
    """
    Main class for creating User Interface of the application - runs in main thread of the Qt App.

    Args: /

    Attributes:
        encoder_connect_signal(pyqtSignal [int]) - signal for sending connect cmd
        to the encoder thread
        encoder_disconnect_signal(pyqtSignal [int]) - signal for sending disconnect cmd
        to the encoder thread
        encoder_enable_signal(pyqtSignal [int]) - signal for sending enable cmd
        to encoder thread
        encoder_disable_signal(pyqtSignal [int]) - signal for sending disable cmd
        to encoder thread
        centralwidget(QWidget) - main widget of UI
        mt_pos_label(Label) - MT position label for the indicator
        mt_pos_indicator(ValueIndicator) - MT position indicator
        st_pos_label(Label) - ST position label for the indicator
        st_pos_indicator(ValueIndicator) - ST position indicator
        com_port_label(Label) - Com port indicator label
        com_port_indicator(ValueIndicator) - Com port indicator
        device_label(Label) - Device indicator label
        device_indicator(ValueIndicator) - Device indicator
        enable_encoder_button(Button) - Encoder enable button
        disable_encoder_button(Button) - Enable encoder button
        connect_button(Button) - Encoder connect button
        disconnect_button(Button) - Encoder disconnect button
        position_plot(LineGraph) - Measurements graph
        alarm_display(AlarmDisplay) - Display for encoder alarms
        alarm_logger(AlarmLogger) - Alarm logger object for logging alarms
        in to txt file
        alarm_error(Alarm) - Encoder Error alarm
        alarm_warning(Alarm) - Encoder Warning alarm
    """

    encoder_connect_signal = pyqtSignal(int)
    encoder_disconnect_signal = pyqtSignal(int)
    encoder_enable_signal = pyqtSignal(int)
    encoder_disable_signal = pyqtSignal(int)

    # Constructor
    def __init__(self, main_window):
        super().__init__()
        main_window.setObjectName("main_window")
        main_window.setFixedSize(935, 698)
        main_window.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # Value Indicator Objects
        self.mt_pos_label = Label("mt_pos_label", self.centralwidget,
                                  (30, 600, 231, 31), 14,
                                  "Multi Turn Position:")

        self.mt_pos_indicator = ValueIndicator("mt_pos_indicator", self.centralwidget,
                                               (30, 640, 231, 41), 14)

        self.st_pos_label = Label("st_pos_label", self.centralwidget,
                                  (280, 600, 231, 31), 14,
                                  "Single Turn Position:")

        self.st_pos_indicator = ValueIndicator("st_pos_indicator", self.centralwidget,
                                               (280, 640, 231, 41), 14)

        self.com_port_label = Label("com_port_label", self.centralwidget,
                                    (390, 10, 101, 31), 12,
                                    "COM Port:")

        self.com_port_indicator = ValueIndicator("com_port_indicator", self.centralwidget,
                                                 (490, 10, 91, 31), 12)

        self.device_label = Label("device_label", self.centralwidget,
                                  (590, 10, 71, 31), 12,
                                  "Device:")

        self.device_indicator = ValueIndicator("device_indicator", self.centralwidget,
                                               (660, 10, 121, 31), 9)

        # Button objects
        self.enable_encoder_button = Button("enable_button", self.centralwidget,
                                            (20, 60, 131, 28), "ENABLE ENCODER",
                                            self.enable_encoder, True, False)

        self.disable_encoder_button = Button("disable_button", self.centralwidget,
                                             (160, 60, 131, 28), "DISABLE ENCODER",
                                             self.disable_encoder, False, False)

        self.connect_button = Button("connect_button", self.centralwidget,
                                     (20, 20, 131, 28), "CONNECT",
                                     self.connect_to_encoder, True)

        self.disconnect_button = Button("disconnect_button", self.centralwidget,
                                        (160, 20, 131, 28), "DISCONNECT",
                                        self.disconnect_encoder, False)

        # Graph object
        self.position_plot = LineGraph(main_window, "Position", 0.1, 1000,
                                       "Time [s]", "Position [°]", (20, 115-20, 680, 480))

        # Alarm Display
        self.alarm_display = AlarmDisplay("alarm_display", self.centralwidget,
                                          (720, 145-20, 191, 405))

        # Alarms
        self.alarm_logger = AlarmLogger("alarm_log.txt")
        self.alarm_error = Alarm(alarm_name="Encoder Error", inverted=True,
                                 trigger_mode="rising")

        self.alarm_warning = Alarm(alarm_name="Encoder Warning", inverted=True,
                                   trigger_mode="rising")

        # Main window
        main_window.setCentralWidget(self.centralwidget)
        main_window.setWindowTitle("Encoder Interface")

        # Start thread tasks
        self.run_encoder_task()

    # Methods
    def run_encoder_task(self):
        """
        Starts encoder data collection thread
        args: /
        return: /
        """
        self.thread = QThread()
        self.worker = EncoderControlTask()
        self.worker.moveToThread(self.thread)

        # Slots and Signals
        self.encoder_connect_signal.connect(self.worker.connect_encoder)
        self.encoder_disconnect_signal.connect(self.worker.disconnect_encoder)
        self.encoder_enable_signal.connect(self.worker.enable_encoder)
        self.encoder_disable_signal.connect(self.worker.disable_encoder)
        self.worker.encoder_info_signal.connect(self.display_encoder_connection_status)
        self.worker.encoder_data_signal.connect(self.get_encoder_data)
        self.thread.start()

    def connect_to_encoder(self):
        """
        Method for connecting to the encoder
        args: /
        return: /
        """
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.encoder_connect_signal.emit(1)

    def disconnect_encoder(self):
        """
        Method for disconnecting from the encoder
        args: /
        return: /
        """
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.encoder_disconnect_signal.emit(1)
        self.com_port_indicator.set_indicator_value("")
        self.device_indicator.set_indicator_value("")
        self.enable_encoder_button.setVisible(False)
        self.disable_encoder_button.setVisible(False)

    def enable_encoder(self):
        """
        Method for enabling the encoder
        args: /
        return: /
        """
        self.enable_encoder_button.setEnabled(False)
        self.disable_encoder_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.encoder_enable_signal.emit(1)

    def disable_encoder(self):
        """
        Method for disabling the encoder
        args: /
        return: /
        """
        self.enable_encoder_button.setEnabled(True)
        self.disable_encoder_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.mt_pos_indicator.set_indicator_value("")
        self.st_pos_indicator.set_indicator_value("")
        self.encoder_disable_signal.emit(1)

    def display_encoder_connection_status(self, data):
        """
        Method for receiving and displaying encoder connection status
        args: data(dict) - received data from the encoder thread
        return: /
        """
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

    def get_encoder_data(self, data):
        """
         Method for receiving measurement data from encoder thread
         args: data(dict) - received data from the encoder thread
         return: /
         """
        error = self.alarm_error.monitor_alarm(data[2])
        warning = self.alarm_warning.monitor_alarm(data[3])

        self.mt_pos_indicator.set_indicator_value(str(data[0]))
        pos_str = f"{str(round(data[1], 4))}°"
        self.st_pos_indicator.set_indicator_value(pos_str)
        self.position_plot.update_graph(data[1])

        self.alarm_logger.log_alarm(self.alarm_error)
        self.alarm_logger.log_alarm(self.alarm_warning)

        # Error
        if error == 1:
            self.alarm_display.append(f"Error\n{datetime.datetime.now()}\n")

        # Warning
        if warning == 1:
            self.alarm_display.append(f"Warning\n{datetime.datetime.now()}\n")
