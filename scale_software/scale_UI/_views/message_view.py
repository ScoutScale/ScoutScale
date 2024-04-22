from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit

class MessageWindow(QDialog):
    def __init__(self, style_guide, message_key, parent=None):
        super().__init__(parent)
        self.style_guide = style_guide
        self.message_key = message_key
        self.init_UI()
    
    def init_UI(self):

        message_style = self.style_guide.get("message view", {}).get("dialog", {})
        window_style = self.style_guide.get("message view", {}).get("window", {})
        ok_button_style = self.style_guide.get("message view", {}).get("buttons", {}).get("ok", {})
        
        self.setWindowTitle(window_style.get("title", {}))
        
        self.setStyleSheet(f"background-color: {window_style.get('color', {})};")
        
        font = QFont(message_style.get("font", {}), message_style.get("text size", {}))
        layout = QVBoxLayout(self)

        message = QTextEdit(message_style.get("labels", {}).get(self.message_key, {}))
        message.setReadOnly(True)
        message.setFont(font)
        message.setStyleSheet(f"""
                                color: {message_style.get('text color', {})}; 
                                background-color: {window_style.get('color', {})}; 
                                border: none;""")
        message.setFixedWidth(message_style.get('width', {}))
        message.setFixedHeight(message_style.get('height', {}))
        layout.addWidget(message)

        confirm_button = QPushButton(ok_button_style["label"])
        confirm_button.setStyleSheet(
            f"background-color: {ok_button_style['color']};"
            f"color: {ok_button_style['text color']};"
            f"font: {ok_button_style['font']};"
            f"border: {ok_button_style['border']};"
            f"border-radius: {ok_button_style['border radius']};"
        )
        confirm_button.clicked.connect(self.accept)
        layout.addWidget(confirm_button)
    
        self.setLayout(layout)

        if not window_style.get("auto size", {}):
            self.resize(window_style.get("width", {}), window_style.get("height", {}))

