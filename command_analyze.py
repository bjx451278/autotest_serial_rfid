class CommandAnalyzer:
    def __init__(self):
        self.frame = None
        self.port = None
        self.command_type = None
        self.payload = None
        self.checksum = None

    def analyze_frame(self,data):
        self.frame=data

        # 解析帧长度
        frame_length = int.from_bytes(self.frame[2:4], byteorder='little')
        # 解析端口号
        self.port = self.frame[4]
        # 解析指令类型
        self.command_type = int.from_bytes(self.frame[5:7], byteorder='little')
        # 解析帧载荷，根据帧长度判断
        if frame_length > 6:
            self.payload = self.frame[7:frame_length+1]
        # 解析校验和
        self.checksum = self.frame[frame_length +1]

        # 根据不同的指令类型进行不同的操作
        if self.command_type == 0x0000:
            self.handle_command_0000()
        elif self.command_type == 0x0001:
            self.handle_command_0001()
        elif self.command_type == 0x0002:
            self.handle_command_0002()
        elif self.command_type == 0x0003:
            self.handle_command_0003()
        elif self.command_type == 0x0011:
            self.handle_command_0011()
        # 可以继续添加其他指令类型的处理函数

    def handle_command_0011(self):
        # 中止操作
        # 处理指令类型为0x0011的指令
        if self.payload:
            print(f'中止操作成功：{self.payload}')
        else:
            print(f'中止操作失败')

    def handle_command_0000(self):
        #Command_Begin指令
        # 处理指令类型为0x0000的指令
        pass

    def handle_command_0001(self):
        # 处理指令类型为0x00的指令
        # Command_End指令
        pass

    def handle_command_0002(self):
        pass

    def handle_command_0004(self):
        pass

    def handle_command_0003(self):
        pass

