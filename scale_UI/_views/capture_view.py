from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CaptureWindow(QDialog):
    def __init__(self, style_guide, captured_weight, units, debug_mode_is_active: bool, desktop_rect, known_weight, parent=None):
        super().__init__(parent)

        self.debug_mode_is_active = debug_mode_is_active
        self.desktop_rect = desktop_rect
        self.known_weight = known_weight

        capture_view_style = style_guide.get("capture view", {})
        window_style = capture_view_style.get("window", {})
        dialog_styles = capture_view_style.get("dialogs", {})
        button_styles = capture_view_style.get("buttons", {})
     
        self.capture_window_title = window_style.get("title")
        self.capture_window_color = window_style.get("color")
        self.capture_window_width = window_style.get("width")
        self.capture_window_height = window_style.get("height")
        self.capture_window_auto_size = window_style.get("auto size")

        self.weight_dialog_text = dialog_styles.get("weight", {}).get("text")
        self.weight_dialog_font = dialog_styles.get("weight", {}).get("font")
        self.weight_dialog_text_color = dialog_styles.get("weight", {}).get("text color")
        self.weight_dialog_text_size = dialog_styles.get("weight", {}).get("text size")

        self.expected_weight_dialog_text = dialog_styles.get("expected weight", {}).get("text")
        self.expected_weight_dialog_font = dialog_styles.get("expected weight", {}).get("font")
        self.expected_weight_dialog_text_color = dialog_styles.get("expected weight", {}).get("text color")
        self.expected_weight_dialog_text_size = dialog_styles.get("expected weight", {}).get("text size")

        self.zone_dialog_text = dialog_styles.get("zone", {}).get("text")
        self.zone_dialog_font = dialog_styles.get("zone", {}).get("font")
        self.zone_dialog_text_color = dialog_styles.get("zone", {}).get("text color")
        self.zone_dialog_text_size = dialog_styles.get("zone", {}).get("text size")

        self.confirm_button_label = button_styles.get("confirm", {}).get("label")
        self.confirm_button_color = button_styles.get("confirm", {}).get("color")
        self.confirm_button_font = button_styles.get("confirm", {}).get("font")
        self.confirm_button_text_color = button_styles.get("confirm", {}).get("text color")
        self.confirm_button_text_size = button_styles.get("confirm", {}).get("text size")
        self.confirm_button_border = button_styles.get("confirm", {}).get("border")
        self.confirm_button_border_radius = button_styles.get("confirm", {}).get("border radius")

        self.units = units

        self.init_UI(captured_weight)

        self.move(desktop_rect.center().x(), desktop_rect.top())

    def init_UI(self, captured_weight):

        self.setWindowTitle(self.capture_window_title)
        self.setStyleSheet(f"background-color: {self.capture_window_color};")

        layout = QVBoxLayout(self)
        label = QLabel(self.weight_dialog_text + f" {captured_weight} {self.units}")
        label.setFont(QFont(self.weight_dialog_font, self.weight_dialog_text_size))
        label.setStyleSheet(f"color: {self.weight_dialog_text_color};")
        layout.addWidget(label)

        expected_weight_label = QLabel(self.expected_weight_dialog_text + f" {captured_weight + self.known_weight} {self.units}")
        expected_weight_label.setFont(QFont(self.expected_weight_dialog_font, self.expected_weight_dialog_text_size))
        expected_weight_label.setStyleSheet(f"color: {self.expected_weight_dialog_text_color};")
        if self.debug_mode_is_active:
            layout.addWidget(expected_weight_label)

        row2 = QHBoxLayout()
        zone_label = QLabel(self.zone_dialog_text)
        zone_label.setFont(QFont(self.zone_dialog_font, self.zone_dialog_text_size))
        zone_label.setStyleSheet(f"color: {self.zone_dialog_text_color};")
        row2.addWidget(zone_label)

        self.text_box = QLineEdit()
        row2.addWidget(self.text_box)

        layout.addLayout(row2)

        confirm_button = QPushButton(self.confirm_button_label)
        confirm_button.setStyleSheet(f"""QPushButton {{
                                     background-color: {self.confirm_button_color}; 
                                     color: {self.confirm_button_text_color}; 
                                     border: {self.confirm_button_border}; 
                                     border-radius: {self.confirm_button_border_radius}; }}""")
        confirm_button.setFont(QFont(self.confirm_button_font, self.confirm_button_text_size))
        confirm_button.clicked.connect(self.confirm_and_close)
        layout.addWidget(confirm_button)

        layout.setAlignment(Qt.AlignCenter)

        if not self.capture_window_auto_size:
            self.resize(self.capture_window_width, self.capture_window_height)

    def confirm_and_close(self):
        self.accept()
