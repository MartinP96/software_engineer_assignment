"""
    File name: encoder_interface.py
    Date: 26.12.2022
    Desc: Encoder interface
"""

from serial_interface import SerialInterface

class EncoderInterface:
    """
    EncoderInterface class used for communication and control of encoder

    Args:
        biss_packet_len(int): Number of bits in biss packet
        mt_bit_len(int): Number of bits for multiturn position in biss packet
        st_bit_len(int): Number of bits for singleturn position in biss packet

    Attributes:
        serial_port_num(str): Number of connected serial port
        interface_version(str): Version of encoder interface module
        _biss_packet_len(int): Number of bits in biss packet
        _mt_num_of_bits(int): Number of bits for multiturn position in biss packet
        _st_num_of_bits(int): Number of bits for singleturn position in biss packet
        _serial_interface(int): Serial interface class for serial com
    """

    # Constructor
    def __init__(self, biss_packet_len, mt_bit_len, st_bit_len):

        self._serial_interface = SerialInterface(0.01)

        self.serial_port_num = ""
        self.interface_version = ""

        # Set biss packet parameters
        self._biss_packet_len = biss_packet_len
        self._mt_num_of_bits = mt_bit_len
        self._st_num_of_bits = st_bit_len

    def disconnect_interface(self):
        """
        Disconnect encoder interface from com port
        args: /
        return: /
        """
        self._serial_interface.disconnect_port()

    def enable_encoder(self):
        """
        Enable encoder power
        args: /
        return: /
        """
        self._serial_interface.write_command(b'N')

    def disable_encoder(self):
        """
        Disable encoder power
        args: /
        return: /
        """
        self._serial_interface.write_command(b'f')

    # Public methods
    def connect_interface(self):
        """
        Scan all com ports and connects to encoder interface module; if present.
        args: /
        return: /
        """

        discovered_ports = self._serial_interface.scan_ports()
        response = {}
        # Test all ports if encoder connected
        for com_port in discovered_ports:
            connection_status = self._serial_interface.connect_port(com_port['port'])
            response = {"com_port":"", "version": "", "status": "not_connected"}
            if connection_status == 1:
                # Test if encoder is connected
                version = self._serial_interface.write_command(b'v')
                if version == b'' or version == -1:
                    self._serial_interface.disconnect_port()
                else:
                    self.interface_version = str(version).replace("b'", "").replace(chr(92), "").replace("r'", "")
                    self.serial_port_num = com_port['port']
                    print(f"Connected to encoder: {self.interface_version} on Port: {self.serial_port_num}")
                    response["com_port"] = com_port['port']
                    response["version"] = self.interface_version
                    response["status"] = "connected"
                    break
        return response

    def read_encoder_data(self):
        """
        Read encoder position and status data (MT, ST, error, warning)
        args: /
        return: MT, ST, error, warning
        """

        biss_data = self._read_biss_data()

        if biss_data != -1:
            mt_bit_offset = self._biss_packet_len - self._mt_num_of_bits + 1
            st_bit_offset = mt_bit_offset - self._st_num_of_bits
            error_bit_offset = st_bit_offset - 1
            warning_bit_offset = st_bit_offset - 2

            # Extract position bits MT + ST
            mt = self._extract_bits(biss_data, self._mt_num_of_bits, mt_bit_offset)
            mt = self._unsigned_to_signed_val(mt)
            st = self._extract_bits(biss_data, self._st_num_of_bits, st_bit_offset)
            st_deg = st * (360 / (2 ** self._st_num_of_bits)) + (360 * mt)

            # Extract Error and Warning bits
            error = self._extract_bits(biss_data, 1, error_bit_offset)
            warning = self._extract_bits(biss_data, 1, warning_bit_offset)

            return mt, st_deg, error, warning
        else:
            return -1

    def _read_biss_data(self):
        """
        Read encoder biss position and status data
        args: /
        return: biss data packet
        """
        response = self._serial_interface.write_command(b'4')
        biss_data = -1
        if response != -1:
            biss_data = "0x" + str(response).replace("b'", "").replace(chr(92), "").replace("r'", "")
            biss_data = int(biss_data, 16)
        return biss_data

    def _extract_bits(self, in_value, num_of_bits, position):
        """
        Extract given number of bits and given position from input value
        args:
            in_value(int): input value
            num_of_bits(int): number of bits to be extracted
            position(int): position of where to extract bits
        return: extracted bits
        """
        return ((1 << num_of_bits) - 1) & (in_value >> (position - 1))

    def _unsigned_to_signed_val(self, val_in):
        """
        Convert unsigned value to signed value - not the best solution, but it works for now.
        args:
            val_in(int): input value

        return: signed value
        """
        val_out = val_in
        if val_in > 65536 / 2:
            val_out = val_in - 65536
        return val_out