from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import QEventLoop
from PyQt5.QtGui import QFont

from _views.known_weight_view import KnownWeightWindow

class CalibrateWindow(QDialog):
    def __init__(self, config_parameters, units, serial_thread, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calibrate View")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);")

        self.serial_thread = serial_thread

        self.units = units

        self.number_of_data_points = config_parameters["calibrate data points"]

        self.scale_zeroed = False

        # calls calibration_abort_confirm function when the confirm_calibration_abort_signal is emitted by serial_thread
        self.serial_thread.confirm_calibration_abort_signal.connect(self.calibration_abort_confirm)

         # calls zeroingComplete function when the zeroed_out_tare_complete_signal is emitted by serial_thread
        self.serial_thread.zeroed_out_tare_complete_signal.connect(self.zeroingComplete)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        label_font = QFont()
        label_font.setPointSize(20)

        button_font = QFont()
        button_font.setPointSize(16)

        self.dialogLabel = QLabel("Please remove all weight from the table and press the ZERO button.")
        self.dialogLabel.setFont(label_font)
        layout.addWidget(self.dialogLabel)

        buttonLayout = QHBoxLayout()

        self.zeroButton = QPushButton("Zero")
        self.zeroButton.setFont(button_font)
        self.zeroButton.setStyleSheet("QPushButton {background-color: rgb(54, 115, 210); color: white; border: 2px solid black; border-radius: 10px; }")
        self.zeroButton.clicked.connect(self.on_zero_button_clicked)
        buttonLayout.addWidget(self.zeroButton)

        self.calibrateButton = QPushButton("Calibrate")
        self.calibrateButton.setFont(button_font) 
        self.calibrateButton.setStyleSheet("QPushButton {background-color: rgb(46,46,46); color: white; border: 2px solid black; border-radius: 10px; }")
        self.calibrateButton.clicked.connect(self.on_calibrate_button_clicked)
        buttonLayout.addWidget(self.calibrateButton)

        layout.addLayout(buttonLayout)

    def on_zero_button_clicked(self):
        self.serial_thread.zeroed_out_signal.emit()

    def zeroingComplete(self):
        self.scale_zeroed = True
        self.dialogLabel.setText("Place a known weight on the table and press the CALIBRATE button.")
        self.calibrateButton.setStyleSheet("QPushButton {background-color: rgb(54, 115, 210); blue: white; border: 2px solid black; border-radius: 10px; }")

    def on_calibrate_button_clicked(self):
        if (self.scale_zeroed):
            self.serial_thread.calibrate_capture_signal.emit()
            known_weight_dialog = KnownWeightWindow(self.units, self.serial_thread)
            if known_weight_dialog.exec_() == QDialog.Accepted:
                self.dialogLabel.setText("Calibrating...")
                event_loop = QEventLoop()
                self.serial_thread.calibration_complete_signal.connect(event_loop.quit)
                self.number_of_data_points -= 1
                if (self.number_of_data_points == 1):
                    self.dialogLabel.setText("Calibration Complete. You can now close this window")
                else:
                    self.dialogLabel.setText("Place a different known weight on the table and press the CALIBRATE button.")


    def calibration_abort_confirm(self):
        self.dialogLabel.setText("Calibration Aborted. You can now close this window")

    def closeEvent(self, event):
        self.serial_thread.calibration_abort_signal.emit()
        super().closeEvent(event)
