import sys
import pandas as pd
import serial.tools.list_ports

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDialog, QRadioButton, QMessageBox, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize, QEventLoop
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime
from time import sleep


MOCK_PORT = '/dev/ttyUSB0'

class MockSerial:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.weight = 0
        print(f"MockSerial initialized on port {port} with baudrate {baudrate}")

    def isOpen(self):
        return True

    def write(self, command):
        print(f"MockSerial write: {command}")

        if command == b't':
            self.weight = 0
        else:
            try:
                float(command.decode('utf-8'))
                calibrate_complete = "c"
                return calibrate_complete.encode('utf-8')
                
            except ValueError:
                pass

    def readline(self):
        mock_weight = f"{self.weight}\n"
        self.weight += 9.5
        sleep(3)
        return mock_weight.encode('utf-8')

    def close(self):
        print("MockSerial port closed")


class SerialReaderThread(QThread):
    new_data = pyqtSignal(str)
    tare_signal = pyqtSignal()
    calibrate_signal = pyqtSignal()
    zeroed_out_signal = pyqtSignal()
    calibrate_capture_signal = pyqtSignal()
    calibrated_weight_scale_value_signal = pyqtSignal(float)
    change_port_signal = pyqtSignal(str)
    calibration_complete_signal = pyqtSignal()

    def __init__(self, serial_port_name):
        super().__init__()
        self.ser = None
        self.waiting_for_calibration = False
        self.connect_to_serial_port(serial_port_name)

    def connect_to_serial_port(self, port_name):

        if (port_name != MOCK_PORT):
            self.ser = serial.Serial(port_name, baudrate=57600)
        else:
            # default mock port
            self.ser = MockSerial(MOCK_PORT, 57600)

    def terminate(self):
        super().terminate()
        self.wait()  

        if self.ser and self.ser.isOpen():
            self.ser.close()
        
    def run(self):
        while True:
            data = self.ser.readline().decode('utf-8').strip()

            if self.waiting_for_calibration and data == 'c':
                self.calibration_complete_signal.emit()
                self.waiting_for_calibration = False
            else:
                self.new_data.emit(data)
    def tare_scale(self):
        if self.ser and self.ser.isOpen():
            self.ser.write(b't')

    def calibrate_scale(self):
        if self.ser and self.ser.isOpen():
            self.ser.write(b'c')
            self.waiting_for_calibration = True

    def zeroed_scale(self):
        if self.ser and self.ser.isOpen():
            self.ser.write(b'z')

    def capture_calibrated_weight_scale(self):
        if self.ser and self.ser.isOpen():
            self.ser.write(b'w')

    def calibrated_weight_scale_value(self, weight):
        if self.ser and self.ser.isOpen():
            weight_bytes = str(weight).encode('utf-8')
            weight_bytes += b'\n'
            self.ser.write(weight_bytes)


            


class ConfigurationMenu(QDialog):
    def __init__(self, selected_serial_port, serial_thread, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration Menu")
        self.resize(400, 300)

        self.selected_serial_port = selected_serial_port
        self.serial_thread = serial_thread

        self.ports_layout = QVBoxLayout(self)
        self.populate_ports()

    def populate_ports(self):
        ports = self.get_available_serial_ports()

        for port in ports:
            button = QRadioButton(port, self)
            button.setChecked(port == self.selected_serial_port)
            button.toggled.connect(lambda checked, port=port: self.on_radio_button_toggled(checked, port))
            self.ports_layout.addWidget(button)

        self.ports_layout.addStretch()

    def on_radio_button_toggled(self, checked, port):
        if checked:
            self.selected_serial_port = port
            self.serial_thread.change_port_signal.emit(self.selected_serial_port) 

    def get_available_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        port_list.append(MOCK_PORT)
        return port_list

class CaptureWindow(QDialog):
    def __init__(self, captured_weight, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Weight Capture Information")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);") 

        layout = QVBoxLayout(self)
        label = QLabel(f"Captured Weight: {captured_weight} lb")
        layout.addWidget(label)

        row2 = QHBoxLayout()
        zoneLabel = QLabel("Zone")
        row2.addWidget(zoneLabel)

        self.text_box = QLineEdit()
        row2.addWidget(self.text_box)

        layout.addLayout(row2)

        confirm_button = QPushButton("Confirm")
        confirm_button.setStyleSheet("QPushButton {background-color: rgb(54, 115, 210); color: white; border: 2px solid black; border-radius: 10px; }")
        confirm_button.clicked.connect(self.confirm_and_close)
        layout.addWidget(confirm_button)

        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)


    def confirm_and_close(self):
        self.accept()


class CalibrateWindow(QDialog):
    def __init__(self, serial_thread, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scale Calibration")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);")

        self.serial_thread = serial_thread

        self.layout = QVBoxLayout(self)

        self.dialogLabel = QLabel("Please remove all weight from the table and press the Zero button.")
        self.layout.addWidget(self.dialogLabel)

        row2 = QHBoxLayout()

        self.zeroButton = QPushButton("Zero")
        self.zeroButton.clicked.connect(self.on_zero_button_clicked)
        row2.addWidget(self.zeroButton)

        self.calibrateButton = QPushButton("Calibrate")
        self.calibrateButton.clicked.connect(self.on_calibrate_button_clicked)
        row2.addWidget(self.calibrateButton)

        self.layout.addLayout(row2)

        self.setLayout(self.layout)

    def on_zero_button_clicked(self):
        
        self.dialogLabel.setText("Place a known weight on the table and press the Calibrate button.")
        self.serial_thread.zeroed_out_signal.emit() 

    def on_calibrate_button_clicked(self):
        self.serial_thread.calibrate_capture_signal.emit()
        known_weight_dialog = KnownWeightDialog(self.serial_thread)
        if known_weight_dialog.exec_() == QDialog.Accepted:
            self.dialogLabel.setText("Calibrating...")
            event_loop = QEventLoop()
            self.serial_thread.calibration_complete_signal.connect(event_loop.quit)
            self.dialogLabel.setText("Calibration Complete. You can now close this window")

            
            


class KnownWeightDialog(QDialog):
    def __init__(self, serial_thread, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);")

        self.serial_thread = serial_thread

        layout = QVBoxLayout(self)

        label = QLabel("Enter the known weight (lb):")
        layout.addWidget(label)

        self.weightEntry = QLineEdit()
        layout.addWidget(self.weightEntry)

        confirmButton = QPushButton("Confirm")
        confirmButton.clicked.connect(self.on_confirm)
        layout.addWidget(confirmButton)

        self.setLayout(layout)

    def on_confirm(self):
        known_weight = float(self.weightEntry.text())
        self.serial_thread.calibrated_weight_scale_value_signal.emit(known_weight)
        self.accept()


class ScaleInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scale Interface")
        self.initUI()
        self.weight = 0
        self.selected_serial_port = MOCK_PORT

        self.csv_file = "scale_data.csv"
        pd.DataFrame(columns=['Capture Date', 'Weight', 'Zone']).to_csv(self.csv_file, index=False)

        self.serial_thread = SerialReaderThread(self.selected_serial_port)
        self.serial_thread.new_data.connect(self.update_weight)
        self.serial_thread.tare_signal.connect(self.serial_thread.tare_scale)
        self.serial_thread.calibrate_signal.connect(self.serial_thread.calibrate_scale)
        self.serial_thread.zeroed_out_signal.connect(self.serial_thread.zeroed_scale)
        self.serial_thread.calibrate_capture_signal.connect(self.serial_thread.capture_calibrated_weight_scale)
        self.serial_thread.calibrated_weight_scale_value_signal.connect(self.serial_thread.calibrated_weight_scale_value)
        self.serial_thread.change_port_signal.connect(self.serial_thread.connect_to_serial_port)


        self.serial_thread.start()

    def closeEvent(self, event):
        self.terminate()
        super().closeEvent(event)

    def terminate(self):
        self.serial_thread.terminate()
        super().close()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet("background-color: rgb(254,248,234);")  
        layout = QVBoxLayout()

        font = QFont()
        font.setWeight(QFont.Bold)
        font.setPointSize(48)

        row1 = QHBoxLayout()

        self.imageButton = QPushButton()
        self.imageButton.setIcon(QIcon("logo.jpg"))
        self.imageButton.setIconSize(QSize(75, 75))
        self.imageButton.setFixedSize(75, 75)

        self.imageButton.clicked.connect(self.show_information_page)
        row1.addWidget(self.imageButton)

        scoutScaleFont = QFont("Gill Sans", 56)
        scoutScaleFont.setWeight(QFont.Bold)

        title = QLabel("ScoutScale")
        title.setFont(scoutScaleFont)
        title.setStyleSheet("color: black;") 
        row1.addWidget(title)

        row1.addStretch()

        hamburger_button = QPushButton("☰")
        hamburger_button.setFont(font)
        hamburger_button.setStyleSheet("color: black;") 
        hamburger_button.setFlat(True)
        hamburger_button.clicked.connect(self.show_configuration_menu)
        row1.addWidget(hamburger_button)

        layout.addLayout(row1)

        self.weightDisplay = QLabel("Current Weight: ")
        self.weightDisplay.setFont(font)
        self.weightDisplay.setStyleSheet("color: black;") 
        layout.addWidget(self.weightDisplay, alignment=Qt.AlignCenter)

        captureButton = QPushButton("Capture Output")
        captureButton.setFont(font)
        captureButton.setStyleSheet("QPushButton { background-color: rgb(180, 120, 80); color: black; border: 2px solid black; border-radius: 10px; }")
        captureButton.clicked.connect(self.capture_scale_output)
        layout.addWidget(captureButton)

        tareButton = QPushButton("Tare Scale")
        tareButton.setFont(font)
        tareButton.setStyleSheet("QPushButton { background-color: rgb(180, 120, 80); color: black; border: 2px solid black; border-radius: 10px; }")
        tareButton.clicked.connect(self.tare_scale)
        layout.addWidget(tareButton)


        calibrateButton = QPushButton("Calibrate Scale")
        calibrateButton.setFont(font)
        calibrateButton.setStyleSheet("QPushButton { background-color: rgb(180, 120, 80); color: black; border: 2px solid black; border-radius: 10px; }")
        calibrateButton.clicked.connect(self.calibrate_scale)
        layout.addWidget(calibrateButton)

        self.centralWidget.setLayout(layout)

    def show_configuration_menu(self):
        dialog = ConfigurationMenu(self.selected_serial_port, self.serial_thread, self)
        dialog.exec_()

    def show_information_page(self):
        msg = QMessageBox()
        msg.setWindowTitle("Logo Clicked")
        msg.setText("The logo was clicked!")
        msg.exec_()

    def tare_scale(self):
        self.serial_thread.tare_signal.emit()

    def calibrate_scale(self):
        self.serial_thread.calibrate_signal.emit() 
        calibrate_window = CalibrateWindow(self.serial_thread)
        calibrate_window.exec_()      

    def capture_scale_output(self):

        tempWeight = self.weight
        capture_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        capture_window = CaptureWindow(tempWeight)
        if capture_window.exec_() == QDialog.Accepted:
            zone = capture_window.text_box.text()

            pd.DataFrame([[capture_date, tempWeight, zone]], columns=['Capture Date', 'Weight', 'Zone']).to_csv(self.csv_file, mode='a', header=False, index=False)
            self.send_to_backend(tempWeight, capture_date, zone) 

    def update_weight(self, weight):
        self.weight = weight
        self.update_weight_display()

    def update_weight_display(self):
        self.weightDisplay.setText(f"Current Weight: {self.weight} lb")

    def send_to_backend(self, weight, capture_date, zone):
        # Mock function to send data to backend
        print(f"Sending to backend: Weight: {weight}, Date: {capture_date}, Zone: {zone}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ScaleInterface()
    mainWin.resize(900, 400)
    mainWin.show()
    sys.exit(app.exec_())
