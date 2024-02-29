from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit

class KnownWeightWindow(QDialog):
    def __init__(self, serial_thread, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);")
        self.serial_thread = serial_thread

        self.initUI()

    def initUI(self):
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
        try:
            known_weight = float(self.weightEntry.text())
            if known_weight == 0:
                self.serial_thread.calibration_abort_signal.emit()
            else:
                self.serial_thread.calibrated_weight_scale_value_signal.emit(known_weight)
        except ValueError:
            self.serial_thread.calibration_abort_signal.emit()
        
        self.accept()
    
    def closeEvent(self, event):
        self.serial_thread.calibration_abort_signal.emit()
        super().closeEvent(event)

