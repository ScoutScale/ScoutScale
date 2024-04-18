from time import sleep

class MockSerial:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.taring = False
        self.weighing = False
        self.calibrate_abort = False
        print(f"MockSerial initialized on port {port} with baudrate {baudrate}")

    def isOpen(self):
        return True

    def write(self, command):
        print(f"MockSerial write: {command}")

        if command in [b't', b'z']:
            self.taring = True
        elif command == b'w':
            self.weighing = True
        elif command == b'x':
            self.calibrate_abort = True

    def readline(self):
        sleep(5)

        if self.taring:
            send_value = "t"
            self.taring = False
        elif self.weighing:
            send_value = "w"
            self.weighing = False
        elif self.calibrate_abort:
            send_value = "x"
            self.calibrate_abort = False
        else:
            send_value = f"m:m:m:m"
        return send_value.encode('utf-8')

    def close(self):
        print("MockSerial port closed")
