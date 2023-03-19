import struct


class RFIDFrame:
    def __init__(self, command_type, payload=b''):
        self.command_type = command_type
        self.payload = payload

    def to_bytes(self):
        port = 0x0D
        payload_len = len(self.payload)
        frame_len = 9 + payload_len  # 9 bytes for header, footer, and checksum

        # Pack fields into bytes
        header = struct.pack('<HHB', 0x555A, frame_len, port)
        payload = self.payload.replace(b'\x5A', b'\x99\xA5').replace(b'\x99', b'\x99\x66').replace(b'\x6A', b'\x99\x95')
        payload = struct.pack(f'<H{payload_len}s', self.command_type, payload)
        checksum = sum(header + payload) % 256
        footer = struct.pack('<H', 0x696A)

        # Combine fields into final byte string
        frame_bytes = header + payload + bytes([checksum]) + footer
        return frame_bytes

    @staticmethod
    def from_bytes(frame_bytes):
        if len(frame_bytes) < 11:
            raise ValueError('Frame is too short')
        if frame_bytes[:2] != b'\x55\x5A':
            raise ValueError('Frame header is invalid')
        if frame_bytes[-2:] != b'\x69\x6A':
            raise ValueError('Frame footer is invalid')

        # Calculate and verify checksum
        checksum = sum(frame_bytes[:-3]) % 256
        if checksum != frame_bytes[-3]:
            raise ValueError('Frame checksum is invalid')

        # Unpack fields from bytes
        _, frame_len, port = struct.unpack('<HHB', frame_bytes[:5])
        if frame_len != len(frame_bytes) - 3:
            raise ValueError('Frame length is invalid')
        command_type, = struct.unpack('<H', frame_bytes[5:7])
        payload = frame_bytes[7:-3]
        payload = payload.replace(b'\x99\xA5', b'\x5A').replace(b'\x99\x66', b'\x99').replace(b'\x99\x95', b'\x6A')

        # Create and return RFIDFrame object
        return RFIDFrame(command_type, payload)
