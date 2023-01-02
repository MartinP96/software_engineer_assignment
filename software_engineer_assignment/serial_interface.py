"""
    File name: serial_interface.py
    Date: 26.12.2022
    Desc: Interface for serial communication
"""

import time
import serial.tools.list_ports
import serial

class SerialInterface:
    """
    SerialInterface class for serial communication via virtual com port.

    Args:
        response_delay_time(float): delay time [in seconds] when between writing and
        reading data from serial port

    Attributes:
        serial_port_num(str): number of connected serial port
        _serial_com (serial): serial com object
        _respone_delay_time (float): delay time [in seconds] when between writing
        and reading data from serial port
    """
    # Constructor
    def __init__(self, response_delay_time):
        self._respone_delay_time = response_delay_time
        self.serial_port_num = ""
        self._serial_com = None

    def scan_ports(self):
        """
        Scan for all used com ports
        args: /
        return: list of all found com ports
        """
        ports = serial.tools.list_ports.comports()
        discovered_ports = []
        for port, desc, hwid in sorted(ports):
            port_dict = {"port": port, "desc": desc, "hwid": hwid}
            discovered_ports.append(port_dict)
        return discovered_ports

    def connect_port(self, port):
        """
        Connect to input port
        args: Port to connect
        return: response - 1 connected, -1 not connected (error)
        """
        try:
            self._serial_com = serial.Serial(port, write_timeout=0.5)
            response = 1
        except serial.SerialException:
            response = -1
        return response

    def disconnect_port(self):
        """
        Close connected port
        args: /
        return: /
        """
        self._serial_com.close()

    def write_command(self, cmd):
        """
        Write comman to serial port
        args: cmd
        return: response: 1 ok, -1 failed
        """
        try:
            self._serial_com.write(cmd)
            time.sleep(self._respone_delay_time)
            bytes_to_read = self._serial_com.inWaiting()
            response = self._serial_com.read(bytes_to_read)
        except (serial.SerialTimeoutException, serial.SerialException):
            response = -1
        return response
