import sys
import pandas as pd

from yaml import safe_load
from datetime import datetime
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                             QDialog)

from _views.configuration_view import ConfigurationWindow
from _views.capture_view import CaptureWindow
from _views.calibrate_view import CalibrateWindow
from _views.tare_view import TareWindow
from _views.info_view import InfoWindow
from _serial.serial_thread import SerialReaderThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scale Interface")
        self.weight = 0

        with open("_config/config.yaml", 'r') as file:
            self.config_parameters = safe_load(file)

        self.init_UI()

        # defaults to MOCK_PORT at the moment
        self.selected_serial_port = self.config_parameters["mock ports"][0]

        self.units = self.config_parameters["default units"]

        # initialize csv file
        self.csv_file = self.config_parameters["data folder"] + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
        pd.DataFrame(columns=["Capture Date", f"Weight({self.units})", "Zone"]).to_csv(self.csv_file, index=False)

        # serial thread initialization
        self.serial_thread = SerialReaderThread(self.config_parameters, self.selected_serial_port)
        self.connect_signals()
        self.serial_thread.start()

    def connect_signals(self):
        # calls update_weight function when new_data signal is emitted by serial_thread
        self.serial_thread.new_data.connect(self.update_weight)

        # calls serial_thread's tare_scale fuction when the tare signal is emitted
        self.serial_thread.tare_signal.connect(self.serial_thread.tare_scale)

        # calls show_tare_menu function when tare_in_progress_signal is emitted by serial_thread
        self.serial_thread.tare_in_progress_signal.connect(self.show_tare_menu)

        # calls close_tare_menu function when the tare_complete_signal is emitted by serial_thread
        self.serial_thread.tare_complete_signal.connect(self.close_tare_menu)

        # calls serial_thread's calibrate_scale scale fuction when the calibrate_signal signal is emitted
        self.serial_thread.calibrate_signal.connect(self.serial_thread.calibrate_scale)

        # calls serial_thread's zeroed_scale fuction when the zeroed_out_signal is emitted
        self.serial_thread.zeroed_out_signal.connect(self.serial_thread.zeroed_scale)

        # calls serial_thread's capture_calibrated_weight_scale fuction when the calibrate_capture_signal is emitted
        self.serial_thread.calibrate_capture_signal.connect(self.serial_thread.capture_calibrated_weight_scale)

        # calls serial_thread's calibrated_weight_scale_value fuction when the calibrated_weight_scale_value_signal is emitted
        self.serial_thread.calibrated_weight_scale_value_signal.connect(self.serial_thread.calibrated_weight_scale_value)

        # calls serial_thread's send_calibration_abort_signal fuction when the calibration_abort_signal is emitted
        self.serial_thread.calibration_abort_signal.connect(self.serial_thread.send_calibration_abort_signal)

        # calls serial_thread's connect_to_serial_port fuction when the change_port_signal is emitted
        self.serial_thread.change_port_signal.connect(self.serial_thread.connect_to_serial_port)

    def closeEvent(self, event):
        self.terminate()
        super().closeEvent(event)

    def terminate(self):
        QCoreApplication.quit()
        self.serial_thread.terminate()
        super().close()
    
    def init_UI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet("background-color: rgb(254,248,234);")  
        layout = QVBoxLayout()

        font = QFont()
        font.setWeight(QFont.Bold)
        font.setPointSize(48)

        row1 = QHBoxLayout()

        self.imageButton = QPushButton()
        self.imageButton.setIcon(QIcon(self.config_parameters["ScoutScale logo"]))
        self.imageButton.setIconSize(QSize(75, 75))
        self.imageButton.setFixedSize(75, 75)

        self.imageButton.clicked.connect(self.show_information_page)
        row1.addWidget(self.imageButton)

        scout_scale_font = QFont("Gill Sans", 56)
        scout_scale_font.setWeight(QFont.Bold)

        title = QLabel("ScoutScale")
        title.setFont(scout_scale_font)
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
        config_window = ConfigurationWindow(self.config_parameters, self.units, self.serial_thread, self)
        config_window.change_units_signal.connect(self.update_units)
        config_window.exec_()

    def show_information_page(self):
        self.InfoWindow = InfoWindow(self.config_parameters)
        self.InfoWindow.exec_()

    def tare_scale(self):
        self.serial_thread.tare_signal.emit()
    
    def show_tare_menu(self):
        self.tare_menu = TareWindow()
        self.tare_menu.exec_()
    
    def close_tare_menu(self):
        self.tare_menu.accept()

    def calibrate_scale(self):
        self.serial_thread.calibrate_signal.emit() 
        calibrate_window = CalibrateWindow(self.config_parameters, self.units, self.serial_thread)
        calibrate_window.exec_()      

    def capture_scale_output(self):

        tempWeight = self.weight
        capture_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        capture_window = CaptureWindow(tempWeight, self.units)
        if capture_window.exec_() == QDialog.Accepted:
            zone = capture_window.text_box.text()
            
            if zone != "" and tempWeight != 0:
                pd.DataFrame([[capture_date, tempWeight, zone]], columns=['Capture Date', 'Weight', 'Zone']).to_csv(self.csv_file, mode='a', header=False, index=False)
                self.send_to_backend(tempWeight, capture_date, zone) 

    def update_weight(self, weight):
        self.weight = weight
        self.update_weight_display()

    def update_units(self, units):
        self.units = units
        pd.DataFrame([["Capture Date", f"Weight({self.units})", "Zone"]], columns=['Capture Date', 'Weight', 'Zone']).to_csv(self.csv_file, mode='a', header=False, index=False)

    def update_weight_display(self):
        self.weightDisplay.setText(f"Current Weight: {self.weight} {self.units}")

    def send_to_backend(self, weight, capture_date, zone):
        #There is a timeout error. Look at Test.py
        pass

        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.resize(900, 400)
    mainWin.show()
    sys.exit(app.exec_())
