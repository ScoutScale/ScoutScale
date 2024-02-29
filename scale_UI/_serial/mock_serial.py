from time import sleep

class MockSerial:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.weight = 0
        self.taring = False
        self.weighing = False
        print(f"MockSerial initialized on port {port} with baudrate {baudrate}")

    def isOpen(self):
        return True

    def write(self, command):
        print(f"MockSerial write: {command}")

        if command in [b't', b'z']:
            self.weight = 0
            self.taring = True
        elif command == b'w':
            self.weighing = True

    def readline(self):
        sleep(3)

        if self.taring:
            send_value = "t"
            self.taring = False
        elif self.weighing:
            send_value = "w"
            self.weighing = False
        else:
            send_value = f"{self.weight}\n"
            self.weight += 6.5
            
        return send_value.encode('utf-8')

    def close(self):
        print("MockSerial port closed")
