from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

class TareWindow(QDialog):
    def __init__(self, style_guide, parent=None):
        super().__init__(parent)

        tare_view_style = style_guide.get("tare view", {})
        self.window_title, self.window_color, self.window_width, self.window_height = (
            tare_view_style.get("window", {}).get(key) for key in ("title", "color", "width", "height")
        )
        message_style = tare_view_style.get("dialog", {})
        self.label_font = message_style.get("font")
        self.text_size = message_style.get("text size")
        self.text_color = message_style.get("text color")
        self.message = message_style.get("text")

    
        self.init_UI()
    
    def init_UI(self):
        self.setWindowTitle(self.window_title)
        self.setStyleSheet(f"background-color: {self.window_color};") 
        font = QFont(self.label_font, self.text_size)
        font.setWeight(QFont.Bold)
        layout = QVBoxLayout(self)
        label = QLabel(self.message)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"color: {self.text_color};")
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(self.window_width, self.window_height)

    def closeEvent(self, event):
        event.ignore()
