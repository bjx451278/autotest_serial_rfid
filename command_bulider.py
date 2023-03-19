class CommandBuilder:
    def __init__(self):
        self.header = b'\x5a\x55'
        self.footer = b'\x6a\x69'
        self.port = b'\x0d'

    def build_oem_read_command(self,register_address,register_value):
        """

        :param register_address: 寄存器地址2byte
        :param register_value: 寄存器值4byte
        :return: OEM寄存器读取指令
        """

    def build_oem_write_command(self, register_address, register_value):
        """
        Host发送获取OEM寄存器写入指令
        HOST_PACKET_TYPE_OEM_WRITE_COMMAND
        :param register_address: 寄存器地址2byte
        :param register_value:寄存器值4byte
        :return:OEM寄存器写入指令
        """
        oem_write_command = b'\x50\x54'
        # construct payload
        payload = register_address.to_bytes(2, byteorder='little')
        payload += register_value.to_bytes(4, byteorder='little')

        oem_write_command_len = b'\x00\x0c'

        # construct full command
        command = self.header
        command += oem_write_command_len[::-1]
        command += self.port
        command += oem_write_command[::-1] # command type little
        command += payload
        # calculate checksum
        checksum = self._calculate_checksum(command)
        command += checksum.to_bytes(1, byteorder='little')
        command += self.footer

        return command

    def build_abort_command(self):
        """
        操作中止：HOST_PACKET_TYPE_ABORT_COMMAND
        :return:操作中止指令
        """
        # construct payload
        payload = b''
        abort_len = b'\x00\x06'


        abort_command = b'\x00\x03'

        # construct full command
        command = self.header
        command += abort_len[::-1]
        command += self.port
        command += abort_command[::-1]  # command type little
        command += payload
        # calculate checksum
        checksum = self._calculate_checksum(command)

        command += checksum.to_bytes(1, byteorder='little')
        command += self.footer

        return command

    def _calculate_checksum(self, payload):
        checksum = 0
        for byte in payload:
            checksum += byte
        print(checksum % 0xff)
        return checksum % 0xff


build = CommandBuilder()
# print(build.build_abort_command().hex())
print(build.build_oem_write_command(505,1).hex())

