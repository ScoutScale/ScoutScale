from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ScoutScale Information Hub")
        self.resize(400, 300)
        self.setStyleSheet("color: black; background-color: rgb(254,248,234);") 

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        label = QLabel("Welcome to ScoutScale\n\n\nThis window is under development")
        layout.addWidget(label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
