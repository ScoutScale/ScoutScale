from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class CaptureWindow(QDialog):
    def __init__(self, captured_weight, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Weight Capture Information")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);") 

        self.initUI(captured_weight)

    def initUI(self, captured_weight):
        layout = QVBoxLayout(self)
        label = QLabel(f"Captured Weight: {captured_weight} lb")
        layout.addWidget(label)

        buttonLayout = QHBoxLayout()
        zoneLabel = QLabel("Zone")
        buttonLayout.addWidget(zoneLabel)

        self.text_box = QLineEdit()
        buttonLayout.addWidget(self.text_box)

        layout.addLayout(buttonLayout)

        confirm_button = QPushButton("Confirm")
        confirm_button.setStyleSheet("QPushButton {background-color: rgb(54, 115, 210); color: white; border: 2px solid black; border-radius: 10px; }")
        confirm_button.clicked.connect(self.confirm_and_close)
        layout.addWidget(confirm_button)

        layout.setAlignment(Qt.AlignCenter)

    def confirm_and_close(self):
        self.accept()
