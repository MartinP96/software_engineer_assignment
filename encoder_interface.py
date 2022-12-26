from serial_interface import SerialInterface

class EncoderInterface:

    # Public attributes
    serial_port_num: str
    interface_version: str

    # Private attributes
    _biss_packet_len: int
    _mt_num_of_bits: int
    _st_num_of_bits: int
    _serial_interface: SerialInterface

    # Constructor
    def __init__(self, biss_packet_len, mt_bit_len, st_bit_len):

        self._serial_interface = SerialInterface(0.01)

        # Set biss packet parameters
        self._biss_packet_len = biss_packet_len
        self._mt_num_of_bits = mt_bit_len
        self._st_num_of_bits = st_bit_len

    def disconnect_interface(self):
        self._serial_interface.disconnect_port()

    def enable_encoder(self):
        self._serial_interface.write_command(b'N')

    def disable_encoder(self):
        self._serial_interface.write_command(b'f')

    # Public methods
    def connect_interface(self):

        discovered_ports = self._serial_interface.scan_ports()

        # Test all ports if encoder connected
        for com_port in discovered_ports:
            response = self._serial_interface.connect_port(com_port['port'])

            if response == 1:
                # Test if encoder is connected
                version = self._serial_interface.write_command(b'v')
                if version == b'' or version == -1:
                    self._serial_interface.disconnect_port()
                else:
                    self.interface_version = str(version)
                    self.serial_port_num = com_port['port']
                    print(f"Connected to encoder: {self.interface_version} on Port: {self.serial_port_num}")

    def read_encoder_data(self):
        biss_data = self._read_biss_data()

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

    # Private methods

    def _read_biss_data(self):
        response = self._serial_interface.write_command(b'4')
        biss_data = "0x" + str(response)[2:18]
        return int(biss_data, 16)

    def _extract_bits(self, in_value, num_of_bits, position):
        return ((1 << num_of_bits) - 1) & (in_value >> (position - 1))

    def _unsigned_to_signed_val(self, val_in):
        val_out = val_in
        if val_in > 65536 / 2:
            val_out = val_in - 65536
        return val_out