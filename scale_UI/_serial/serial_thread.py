from PyQt5.QtCore import QThread, pyqtSignal
from threading import Event
import serial

from _serial.mock_serial import MockSerial

class SerialReaderThread(QThread):

    new_data = pyqtSignal(str)
    tare_signal = pyqtSignal()
    tare_in_progress_signal = pyqtSignal()
    tare_complete_signal = pyqtSignal()
    calibrate_signal = pyqtSignal()
    zeroed_out_signal = pyqtSignal()
    zeroed_out_tare_complete_signal = pyqtSignal()
    calibrate_capture_signal = pyqtSignal()
    calibrated_weight_scale_value_signal = pyqtSignal(float)
    calibration_complete_signal = pyqtSignal()
    calibration_abort_signal = pyqtSignal()
    confirm_calibration_abort_signal = pyqtSignal()
    change_port_signal = pyqtSignal(str)

    def __init__(self, config_parameters, serial_port_name):
        super().__init__()

        self.serial_port = None
        self.serial_port_name = serial_port_name

        self.mock_port1_name = config_parameters["mock ports"][0]
        self.mock_port2_name = config_parameters["mock ports"][1]
        self.baudrate = config_parameters["baudrate"]

        self.waiting_for_calibration = False
        self.taring_in_progress = False
        self.weighting_in_progress = False
        self.aborting_calibration = False

        self.connect_to_serial_port(serial_port_name)

    def connect_to_serial_port(self, port_name):
        self.serial_port_name = port_name

        # currently set up to work with both real and mock ports
        if (port_name !=  self.mock_port1_name and port_name != self.mock_port2_name):
            self.serial_port = serial.Serial(port_name, baudrate=self.baudrate)
        elif (port_name == self.mock_port2_name):
            self.serial_port = MockSerial(self.mock_port2_name, self.baudrate)
        else:
            self.serial_port = MockSerial(self.mock_port1_name, self.baudrate)

    def terminate(self):
        super().terminate()
        self.wait()  

        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()
        
    def run(self):
        while True:
            data = self.serial_port.readline().decode('utf-8').strip()

            if self.waiting_for_calibration and data == 'c':
                self.calibration_complete_signal.emit()
                self.waiting_for_calibration = False
            elif self.weighting_in_progress and data == "w":
                self.weighting_in_progress = False
                self.weighting_event.set()
            elif self.taring_in_progress and data == 't':
                self.taring_in_progress = False
                self.tare_complete_signal.emit()

                if self.waiting_for_calibration == True:
                    self.zeroed_out_tare_complete_signal.emit()
                
            elif self.aborting_calibration and data == 'x':
                self.aborting_calibration = False
                self.confirm_calibration_abort_signal.emit()
            else:
                self.new_data.emit(data)
        
    def tare_scale(self):
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.write(b't')
            self.taring_in_progress = True
            self.tare_in_progress_signal.emit()

    def calibrate_scale(self):
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.write(b'c')
            self.waiting_for_calibration = True

    def zeroed_scale(self):
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.write(b'z')
            self.taring_in_progress = True
            self.tare_in_progress_signal.emit()

    def capture_calibrated_weight_scale(self):
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.write(b'w')
            self.weighting_in_progress = True
            self.weighting_event = Event()  # Create the event

    def calibrated_weight_scale_value(self, weight):
        if self.serial_port and self.serial_port.isOpen():
            weight_bytes = str(weight).encode('utf-8')
            weight_bytes += b'\n'
            self.weighting_event.wait()
            self.serial_port.write(weight_bytes)
    
    def send_calibration_abort_signal(self):
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.write(b'x')
            self.waiting_for_calibration = False
            self.weighting_in_progress = False
            self.aborting_calibration = True
