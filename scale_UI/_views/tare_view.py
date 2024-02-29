from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class TareWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tare Menu")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);") 

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        label = QLabel("Taring...")
        layout.addWidget(label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
