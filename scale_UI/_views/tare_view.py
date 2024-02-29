from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TareWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tare Menu")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);") 

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setWeight(QFont.Bold)
        font.setPointSize(48)
        layout = QVBoxLayout(self)
        label = QLabel("Taring...")
        label.setFont(font)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
