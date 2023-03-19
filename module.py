import serial
import struct

class RFIDReader:
    def __init__(self, port, baud_rate):

        self.HEADER = 0x5a55
        self.FOOTER = 0x6a69
        self.g_port = 0x0d
        self.ser = serial.Serial(port, baud_rate)

    def pack_frame(self, cmd_type, payload):
        payload = self._escape_frame(payload)
        frame_len = len(payload) + 5  # 5 bytes for header, length and checksum
        frame = struct.pack('<2H B 2s %ds B 2s' % len(payload),
                            self.HEADER, frame_len, self.g_port, cmd_type, payload, 0, self.FOOTER)
        checksum = self._calc_checksum(frame[:-2])
        frame = frame[:-2] + struct.pack('B', checksum) + frame[-2:]
        return frame

    def _escape_frame(self, payload):
        escaped = bytearray()
        for byte in payload:
            if byte == 0x5a:
                escaped.extend(b'\x99\xa5')
            elif byte == 0x99:
                escaped.extend(b'\x99\x66')
            elif byte == 0x6a:
                escaped.extend(b'\x99\x95')
            else:
                escaped.append(byte)
        return escaped

    def _unescape_frame(self, payload):
        unescaped = bytearray()
        i = 0
        while i < len(payload):
            if payload[i] == 0x99:
                if payload[i+1] == 0xa5:
                    unescaped.append(0x5a)
                elif payload[i+1] == 0x66:
                    unescaped.append(0x99)
                elif payload[i+1] == 0x95:
                    unescaped.append(0x6a)
                else:
                    raise ValueError("Invalid escape sequence")
                i += 2
            else:
                unescaped.append(payload[i])
                i += 1
        return unescaped


    def _calc_checksum(self, data):
        checksum = sum(data)
        return checksum & 0xff

    def read_rfid(self):
        # cmd_type = b'\x00\x00'  # command type for reading RFID
        # frame = self.pack_frame(cmd_type, b'')
        # self.ser.write(frame)

        header = self.ser.read(4)
        if header != b'\x55\x5a':
            raise ValueError("Invalid frame header")

        frame_len = struct.unpack('<H', self.ser.read(2))[0]
        payload = self.ser.read(frame_len - 5)

        checksum = struct.unpack('B', self.ser.read())[0]
        expected_checksum = self._calc_checksum(header + struct.pack('<H', frame_len) + payload)
        if checksum != expected_checksum:
            raise ValueError("Checksum mismatch")

        unescaped_payload = self._unescape_frame(payload[:-2])
        rfid = unescaped_payload.decode('utf-8')

        footer = self.ser.read(2)
        if footer != b'\x6a\x69':
            raise ValueError("Invalid frame footer")

        return rfid

    def close(self):
        self.ser.close()

# process_data方法可以用来处理从串口读取的原始数据。该方法需要在串口接收到数据后被调用。在该方法中，你需要解析读取到的原始数据并处理每个数据帧。
#
# 以下是一个可能的实现，仅供参考：
#
# python
# Copy code
def process_data(self):
    buffer = self.ser.read(self.ser.in_waiting)
    frames = self.extract_frames(buffer)
    for frame in frames:
        try:
            payload = self.handle_frame(frame)
            # do something with the payload
        except ValueError as e:
            print("Error handling frame:", e)

def extract_frames(self, buffer):
    frames = []
    i = 0
    while i < len(buffer):
        if buffer[i:i+2] == b'\x5a\x55':
            # found a potential frame header
            if i+4 >= len(buffer):
                # not enough data for a complete frame
                break
            frame_len = struct.unpack('<H', buffer[i+2:i+4])[0]
            if i+frame_len >= len(buffer):
                # not enough data for a complete frame
                break
            frames.append(buffer[i:i+frame_len])
            i += frame_len
        else:
            i += 1
    return frames

def handle_frame(self, frame):
    if frame[-2:] != b'\x6a\x69':
        raise ValueError("Invalid frame footer")
    frame = frame[:-2]
    checksum = struct.unpack('B', frame[-1:])[0]
    expected_checksum = self._calc_checksum(frame[:-1])
    if checksum != expected_checksum:
        raise ValueError("Checksum mismatch")
    unescaped_payload = self._unescape_frame(frame[4:-1])
    return unescaped_payload.decode('utf-8')
# 该实现从串口读取缓冲区中提取帧，并依次处理每个帧。首先，它使用extract_frames方法将缓冲区中的字节流分割成一个个帧。然后，对于每个帧，它使用handle_frame方法解析帧头、帧长度、帧载荷、校验和和帧尾，并返回解析后的载荷。最后，在process_data方法中，你可以使用handle_frame返回的载荷执行相应的操作。如果在解析过程中发生错误，handle_frame会引发ValueError异常，这个异常会被捕获并打印到控制台上。
#
# 请注意，这只是一个简单的实现示例，你需要根据实际情况进行修改。特别是，你需要添加针对不同命令类型的逻辑。