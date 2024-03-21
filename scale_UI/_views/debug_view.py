from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QApplication
from yaml import safe_load

from _serial.serial_thread import SerialReaderThread

class DebugWindow(QDialog):
    def __init__(self, style_guide, units, serial_thread, parent=None):
        super().__init__(parent)

        self.units = units

        debug_style = style_guide.get("debug", {})
        window_style = debug_style.get("window", {})
        text_box_style = debug_style.get("text box", {})

        self.debug_window_title = window_style.get("title")
        self.debug_window_color = window_style.get("color")
        self.debug_window_width = window_style.get("width")
        self.debug_window_height = window_style.get("height")
        self.debug_window_offset = window_style.get("offset")
        self.debug_window_auto_size = window_style.get("auto size")
        self.debug_window_font = window_style.get("font")
        self.debug_window_text_color = window_style.get("text color")

        self.debug_text_box_width = text_box_style.get("width")
        self.debug_text_box_height = text_box_style.get("height")

        self.serial_thread = serial_thread

        self.init_UI()

        self.connect_serial_port()

    def init_UI(self):
        self.setWindowTitle(self.debug_window_title)
        self.setStyleSheet(f"color: {self.debug_window_text_color}; background-color: {self.debug_window_color};")

        layout = QVBoxLayout(self)

        self.debug_body_text = QTextEdit()
        self.debug_body_text.setReadOnly(True)
        self.debug_body_text.setStyleSheet("border: none;")
        self.debug_body_text.setHtml(self.base_debug_text(strings=["", "", "", ""]))
        self.debug_body_text.setMinimumSize(self.debug_text_box_width, self.debug_text_box_height)
        layout.addWidget(self.debug_body_text)

        self.setLayout(layout)

        if not self.debug_window_auto_size:
            self.resize(self.debug_window_width, self.debug_window_height)

        desktop = QApplication.desktop()
        desktop_rect = desktop.availableGeometry()
        self.move(desktop_rect.topRight())

        self.show()

    def connect_serial_port(self):
        self.serial_thread.new_data.connect(self.update_weight)

    def update_weight(self, weight_string):
        self.debug_body_text.setHtml(self.debug_text(weight_string=weight_string))

    def debug_text(self, weight_string: str):
        split_weights = weight_string.split(sep=":")
        return self.base_debug_text(strings=split_weights)

    def base_debug_text(self, strings: [str]):
        leg_1_value = round(float(strings[0]), 3) if strings[0] else 0.0
        leg_2_value = round(float(strings[1]), 3) if strings[1] else 0.0
        leg_3_value = round(float(strings[2]), 3) if strings[2] else 0.0
        leg_4_value = round(float(strings[3]), 3) if strings[3] else 0.0
        
        return f"""
        <p style="font-size: 24px;">Leg 1: {leg_1_value} {self.units}</p>
        <p style="font-size: 24px;">Leg 2: {leg_2_value} {self.units}</p>
        <p style="font-size: 24px;">Leg 3: {leg_3_value} {self.units}</p>
        <p style="font-size: 24px;">Leg 4: {leg_4_value} {self.units}</p>
        """




