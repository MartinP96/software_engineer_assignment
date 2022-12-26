import time
import serial.tools.list_ports
import serial

class SerialInterface:

    # Public variables
    serial_port_num: str

    # Private variables
    _serial_com: serial
    _respone_delay_time: float

    # Constructor
    def __init__(self, response_delay_time):
        self._respone_delay_time = response_delay_time

    def scan_ports(self):
        ports = serial.tools.list_ports.comports()
        discovered_ports = []
        for port, desc, hwid in sorted(ports):
            port_dict = {"port": port, "desc": desc, "hwid": hwid}
            discovered_ports.append(port_dict)
        return discovered_ports

    def connect_port(self, port):
        try:
            self._serial_com = serial.Serial(port, write_timeout=0.5)
            response = 1
        except serial.SerialException:
            response = -1
        return response

    def disconnect_port(self):
        self._serial_com.close()

    def write_command(self, cmd):
        try:
            self._serial_com.write(cmd)
            time.sleep(self._respone_delay_time)
            bytes_to_read = self._serial_com.inWaiting()
            response = self._serial_com.read(bytes_to_read)
        except serial.SerialTimeoutException:
            response = -1
            pass
        return response
