from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

class ConfirmWindow(QDialog):
    def __init__(self, style_guide, message_key, parent=None):
        super().__init__(parent)
        self.style_guide = style_guide["confirm action view"]
        self.message = style_guide["confirm action view"]["dialog"]["labels"][message_key]
        self.init_UI()
    
    def init_UI(self):
        window_style = self.style_guide["window"]
        dialog_style = self.style_guide["dialog"]
        confirm_button_style = self.style_guide["buttons"]["confirm"]
        cancel_button_style = self.style_guide["buttons"]["cancel"]

        self.setWindowTitle(window_style["title"])
        self.setStyleSheet(f"background-color: {window_style['color']};")

        font = QFont(dialog_style["font"], dialog_style["text size"])

        layout = QVBoxLayout(self)

        message = QTextEdit(self.message)
        message.setFont(font)
        message.setReadOnly(True)
        message.setStyleSheet(f"""
                                color: {dialog_style['text color']}; 
                                background-color: {window_style['color']}; 
                                border: none;""")
        message.setFixedWidth(dialog_style["width"])
        message.setFixedHeight(dialog_style["height"])
        layout.addWidget(message)

        row2 = QHBoxLayout()

        cancel_button = QPushButton(cancel_button_style["label"])
        cancel_button.setStyleSheet(
            f"background-color: {cancel_button_style['color']};"
            f"color: {cancel_button_style['text color']};"
            f"font: {cancel_button_style['font']};"
            f"border: {cancel_button_style['border']};"
            f"border-radius: {cancel_button_style['border radius']};"
        )
        cancel_button.clicked.connect(self.cancel)
        row2.addWidget(cancel_button)

        confirm_button = QPushButton(confirm_button_style["label"])
        confirm_button.setStyleSheet(
            f"background-color: {confirm_button_style['color']};"
            f"color: {confirm_button_style['text color']};"
            f"font: {confirm_button_style['font']};"
            f"border: {confirm_button_style['border']};"
            f"border-radius: {confirm_button_style['border radius']};"
        )
        confirm_button.clicked.connect(self.confirm)
        row2.addWidget(confirm_button)

        layout.addLayout(row2)
        self.setLayout(layout)

        if not window_style["auto size"]:
            self.resize(window_style["width"], window_style["height"])

    def confirm(self):
        self.accept()
        
    def cancel(self):
        self.reject()

    def closeEvent(self, event):
        self.reject()
