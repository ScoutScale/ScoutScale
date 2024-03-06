from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TareWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_UI()
    
    def init_UI(self):
        self.setWindowTitle("Tare View")
        self.setStyleSheet("color: white; background-color: rgb(46,46,46);") 
        font = QFont("Arial", 20)
        font.setWeight(QFont.Bold)
        layout = QVBoxLayout(self)
        label = QLabel("Taring...")
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.setSpacing(20)
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(200, 50)