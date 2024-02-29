from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import QEventLoop

from _serial.serial_thread import SerialReaderThread
from _views.known_weight_view import KnownWeightWindow

class CalibrateWindow(QDialog):
    def __init__(self, serial_thread, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scale Calibration")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);")

        self.serial_thread = serial_thread

        # calls calibration_abort_confirm function when the confirm_calibration_abort_signal is emitted by serial_thread
        self.serial_thread.confirm_calibration_abort_signal.connect(self.calibration_abort_confirm)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.dialogLabel = QLabel("Please remove all weight from the table and press the Zero button.")
        layout.addWidget(self.dialogLabel)

        buttonLayout = QHBoxLayout()

        self.zeroButton = QPushButton("Zero")
        self.zeroButton.clicked.connect(self.on_zero_button_clicked)
        buttonLayout.addWidget(self.zeroButton)

        self.calibrateButton = QPushButton("Calibrate")
        self.calibrateButton.clicked.connect(self.on_calibrate_button_clicked)
        buttonLayout.addWidget(self.calibrateButton)

        layout.addLayout(buttonLayout)

    def on_zero_button_clicked(self):
        self.dialogLabel.setText("Place a known weight on the table and press the Calibrate button.")
        self.serial_thread.zeroed_out_signal.emit() 

    def on_calibrate_button_clicked(self):
        self.serial_thread.calibrate_capture_signal.emit()
        known_weight_dialog = KnownWeightWindow(self.serial_thread)
        if known_weight_dialog.exec_() == QDialog.Accepted:
            self.dialogLabel.setText("Calibrating...")
            event_loop = QEventLoop()
            self.serial_thread.calibration_complete_signal.connect(event_loop.quit)
            self.dialogLabel.setText("Calibration Complete. You can now close this window")

    def calibration_abort_confirm(self):
        self.dialogLabel.setText("Calibration Aborted. You can now close this window")

    def closeEvent(self, event):
        self.serial_thread.calibration_abort_signal.emit()
        super().closeEvent(event)
