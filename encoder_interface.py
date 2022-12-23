import time
import serial.tools.list_ports
import serial

class EncoderInterface:

    # Public
    serial_port_num: str
    interface_version: str

    # Private
    _serial_com: serial

    # Constructor
    def __init__(self, com_port):
        self.serial_port_num = com_port
        self._serial_com = serial.Serial(com_port)

    # Public methods

    def disconnect_interface(self):
        self._serial_com.close()

    def enable_encoder(self):
        self._serial_com.write(b'N')

    def disable_encoder(self):
        self._serial_com.write(b'f')

    def read_encoder_data(self):
        biss_data = self._read_biss_data()

        # Extract position bits MT + ST
        mt = self._extract_bits(biss_data, 16, 49)  # TODO: Quick Solution, needs to be tested
        if mt > 65536 / 2:
            mt = mt - 65536

        st = extract_bits(biss_data, 19, 30)
        st_deg = st * (360 / (2 ** 19)) + (360 * mt)

        # TODO: Extract error and warning status

        return mt, st_deg

    # Private methods

    def _read_biss_data(self):
        self._serial_com.write(b'4')
        time.sleep(0.01)
        bytes_to_read = self._serial_com.inWaiting()
        biss_data = self._serial_com.read(bytes_to_read)
        biss_data_str = "0x" + str(biss_data)[2:18]
        return int(biss_data_str, 16)

    def _write_command(self):
        pass

    def _extract_bits(self, in_value, num_of_bits, position):
        return ((1 << num_of_bits) - 1) & (in_value >> (position - 1))

def extract_bits(in_value, num_of_bits, position):
    return ((1 << num_of_bits) - 1) & (in_value >> (position - 1))