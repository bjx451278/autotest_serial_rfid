import struct
from command_analyze import CommandAnalyzer
import binascii
class FrameExtractor:
    def __init__(self):
        self.buffer = b''
        self.frames = []

    def unescape(self, data):
        """转义还原"""
        i = 0
        n = len(data)
        res = bytearray()
        while i < n:
            if data[i] == 0x99:
                if i + 1 >= n:
                    break
                if data[i + 1] == 0xA5:
                    res.append(0x5A)
                    i += 2
                    continue
                elif data[i + 1] == 0x66:
                    res.append(0x99)
                    i += 2
                    continue
                elif data[i + 1] == 0x95:
                    res.append(0x6A)
                    i += 2
                    continue
            res.append(data[i])
            i += 1
        return bytes(res)

    def caclc_check(self,data):
        """校验和计算
        @param：计算校验和的数据
        @return：CRC校验值
        """
        sum = 0
        for d in data:
            sum +=d
        return sum % 0xff

    def extract_frames(self, data):
        frames = []
        frame_start_found = False  # 新增标志变量，指示是否找到了帧头
        # 将当前数据缓冲区中的数据与新接收到的数据合并
        self.buffer +=data
        start = None  # 记录帧头的起始位置
        # 处理数据缓冲区中的数据，提取完整的数据帧
        while True:
            # 如果缓冲区中的数据不足一个完整的数据帧，则退出循环等待更多数据到达
            if len(self.buffer) < 6:
                break

            if not frame_start_found:
                # 查找帧头
                try:
                    start = self.buffer.index(b'\x5a\x55')
                    if start != None:
                        self.buffer = self.buffer[start:]
                        frame_start_found = True  # 找到帧头，设置标志变量为True
                        continue
                    else:
                        frame_start_found = True  # 找到帧头，设置标志变量为True
                except ValueError as e:
                    self.buffer = []
                    print(f'error:{e}')
                    break
            else:
                # 查找帧尾
                try:
                    end = self.buffer.index(b'\x6a\x69', start+2)
                except ValueError:
                    break  # 未找到帧尾，退出循环等待更多数据

                # 提取完整的数据帧
                try:
                    # 进行校验和计算判断
                    if self.caclc_check(self.buffer[start:end - 1]) != self.buffer[end - 1]:
                        # CRC校验不符，抛弃数据，重新寻找数据帧
                        self.buffer = self.buffer[start + 2:]
                        continue
                    #还原转义
                    data_frame = self.unescape(self.buffer[start+2:end-1])

                    #计算数据帧长度
                    length = struct.unpack('<H', data_frame[:2])[0]
                    #判断是否为完整的数据帧
                    if end - start == length + 2:
                        #添加完整的数据帧到列表中
                        frame = self.buffer[start:start+2] + data_frame +self.buffer[end-1:end+2]
                        frames.append(frame)
                        #重置标志变量
                        frame_start_found = False
                        #从缓冲区移出已提取到数据帧
                        self.buffer = self.buffer[end+2:]
                        break
                    else:
                        #不是完整的数据帧，需要重新查找帧头
                        frame_start_found = False
                        self.buffer = self.buffer[start+2:]
                except struct.error:
                    # 未找到帧尾，等待下一个数据
                    self.buffer = self.buffer[start:]
                    frame_start_found = False
                    pass  # 解析数据帧出错，继续查找下一个数据帧


        return frames

a = b'\x5a\x55\x06\x00\x0d\x03\x00\xc5\x6a\x69'
c = b'\x5a\x55\x07\x00\x0d\x11\x00\x01\xd5\x6a\x69'
frame = FrameExtractor()
# g = frame.caclc_check(c[0:8])
# print(hex(g))
b=frame.extract_frames(c)
q=b[0]
print(binascii.hexlify(q))
command = CommandAnalyzer()
command.analyze_frame(b[0])
frame_list = [b'ZU\x06\x00\r\x03\x00\xc5ji']
frame = frame_list[0]