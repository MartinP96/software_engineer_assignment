import time
import serial.tools.list_ports
import serial

class EncoderInterface:

    # Public
    serial_port_num: str
    interface_version: str

    # Private
    _serial_com: serial
    _biss_packet_len: int
    _mt_num_of_bits: int
    _st_num_of_bits: int

    # Constructor
    def __init__(self, biss_packet_len, mt_bit_len, st_bit_len):

        # Set biss packet parameters
        self._biss_packet_len = biss_packet_len
        self._mt_num_of_bits = mt_bit_len
        self._st_num_of_bits = st_bit_len

    # Public methods

    def connect_interface(self):

        # Scan for com avaiable com ports
        ports = serial.tools.list_ports.comports()
        discovered_ports = []
        for port, desc, hwid in sorted(ports):
            port_dict = {"port": port, "desc": desc, "hwid": hwid}
            discovered_ports.append(port_dict)
            version = -1
            try:
                self._serial_com = serial.Serial(port_dict["port"], write_timeout=0.5)

                # Test if encoder is connected
                version = self._write_command(b'v')
                if version == b'' or version == -1:
                    self._serial_com.close()
                else:
                    self.interface_version = str(version)
                    self.serial_port_num = port_dict["port"]
                    print(f"Connected to encoder: {self.interface_version} on Port: {self.serial_port_num}")
                    break

            except serial.SerialException:
                self._serial_com.close()

    def disconnect_interface(self):
        self._serial_com.close()

    def enable_encoder(self):
        self._write_command(b'N')

    def disable_encoder(self):
        self._write_command(b'f')

    def read_encoder_data(self):
        biss_data = self._read_biss_data()

        # Extract position bits MT + ST
        mt = self._extract_bits(biss_data, self._mt_num_of_bits, 49)
        mt = self._unsigned_to_signed_val(mt)
        st = self._extract_bits(biss_data, self._st_num_of_bits, 30)
        st_deg = st * (360 / (2 ** 19)) + (360 * mt)

        # Extract Error and Warning bits
        error = 0
        warning = 0
        error = self._extract_bits(biss_data, 1, 29)
        warning = self._extract_bits(biss_data, 1, 28)

        return mt, st_deg, error, warning

    # Private methods

    def _read_biss_data(self):
        self._serial_com.write(b'4')
        time.sleep(0.01)
        bytes_to_read = self._serial_com.inWaiting()
        biss_data = self._serial_com.read(bytes_to_read)
        biss_data_str = "0x" + str(biss_data)[2:18]
        return int(biss_data_str, 16)

    def _write_command(self, cmd):

        response = 0

        try:
            self._serial_com.write(cmd)
            time.sleep(0.01)
            bytes_to_read = self._serial_com.inWaiting()
            response = self._serial_com.read(bytes_to_read)
        except serial.SerialTimeoutException:
            response = -1
            pass

        return response

    def _extract_bits(self, in_value, num_of_bits, position):
        return ((1 << num_of_bits) - 1) & (in_value >> (position - 1))

    def _unsigned_to_signed_val(self, val_in):
        val_out = val_in
        if val_in > 65536 / 2:
            val_out = val_in - 65536
        return val_out