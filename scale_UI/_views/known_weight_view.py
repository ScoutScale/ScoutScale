from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

class KnownWeightWindow(QDialog):

    calibration_abort_change_dialog_signal = pyqtSignal()

    def __init__(self, known_weight_window_style_guide, units, serial_thread, parent=None):
        super().__init__(parent)

        self.window_title, self.window_color, self.window_width, self.window_height, self.auto_size = (
            known_weight_window_style_guide.get("window", {}).get(key) for key in ("title", "color", "width", "height", "auto size")
        )

        self.dialog_text, self.dialog_font, self.dialog_text_size, self.dialog_text_color = (
            known_weight_window_style_guide.get("dialog", {}).get(key) for key in ("text", "font", "text size", "text color")
        )

        confirm_button_style = known_weight_window_style_guide.get("buttons", {}).get("confirm", {})
        self.confirm_button_label = confirm_button_style.get("label")
        self.confirm_button_color = confirm_button_style.get("color")
        self.confirm_button_font = confirm_button_style.get("font")
        self.confirm_button_text_color = confirm_button_style.get("text color")
        self.confirm_button_text_size = confirm_button_style.get("text size")
        self.confirm_button_border = confirm_button_style.get("border")
        self.confirm_button_border_radius = confirm_button_style.get("border radius")

        self.serial_thread = serial_thread

        self.units = units

        self.init_UI()

    def init_UI(self):

        self.setWindowTitle(self.window_title)
        self.setStyleSheet(f"background-color: {self.window_color};")
        layout = QVBoxLayout(self)

        label_font = QFont(self.dialog_font, self.dialog_text_size)
        label = QLabel(self.dialog_text+ f" ({self.units}):")
        label.setFont(label_font)
        label.setStyleSheet(f"color: {self.dialog_text_color}") 
        layout.addWidget(label)

        self.weightEntry = QLineEdit()
        layout.addWidget(self.weightEntry)

        confirm_button = QPushButton(self.confirm_button_label)
        confirm_button.setFont(QFont(self.confirm_button_font, self.confirm_button_text_size))
        confirm_button.setStyleSheet(f"""QPushButton {{
                                      background-color: {self.confirm_button_color};
                                      color: {self.confirm_button_text_color}; 
                                      border: {self.confirm_button_border}; 
                                      border-radius: {self.confirm_button_border_radius}; }}""")
        confirm_button.clicked.connect(self.on_confirm)
        
        layout.addWidget(confirm_button)

        self.setLayout(layout)

        if not self.auto_size:
            self.resize(self.window_width, self.window_height)

    def on_confirm(self):
        
        try:
            known_weight = float(self.weightEntry.text())
            if known_weight == 0:
                self.calibration_abort_change_dialog_signal.emit()
                self.serial_thread.calibration_abort_signal.emit()
            else:
                self.serial_thread.calibrated_weight_scale_value_signal.emit(known_weight)
        except ValueError:
            self.calibration_abort_change_dialog_signal.emit()
            self.serial_thread.calibration_abort_signal.emit()
            

        self.accept()
        
    def closeEvent(self, event):
        self.calibration_abort_change_dialog_signal.emit()
        self.serial_thread.calibration_abort_signal.emit()
        super().closeEvent(event)

