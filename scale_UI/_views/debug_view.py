from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QApplication
from yaml import safe_load

from _serial.serial_thread import SerialReaderThread

class DebugWindow(QDialog):
    def __init__(self, style_guide, units, parent=None):
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

        self.init_UI()

        self.retrieve_config_file()

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

        layout.addStretch()

        self.setLayout(layout)

        if not self.debug_window_auto_size:
            self.resize(self.checklist_window_width, self.checklist_window_height)

        desktop = QApplication.desktop()
        desktop_rect = desktop.availableGeometry()
        self.move(desktop_rect.topRight())

        self.show()

    def connect_serial_port(self):
        self.selected_serial_port = self.config_parameters["Serial"]["mock ports"][0]

        self.serial_thread = SerialReaderThread(self.config_parameters, self.selected_serial_port)
        self.serial_thread.start()
        self.serial_thread.new_data.connect(self.update_weight)

    def retrieve_config_file(self):
        with open("_config/config.yaml", 'r') as file:
            self.config_parameters = safe_load(file)

    def update_weight(self, weight_string):
        self.debug_body_text.setHtml(self.debug_text(weight_string=weight_string))

    def debug_text(self, weight_string: str):
        split_weights = weight_string.split(sep=":")
        return self.base_debug_text(strings=split_weights)

    def base_debug_text(self, strings: [str]):
        return f"""
        <p style="font-size: 24px;">Leg 1: {strings[0]} {self.units}</p>
        <p style="font-size: 24px;">Leg 2: {strings[1]} {self.units}</p>
        <p style="font-size: 24px;">Leg 3: {strings[2]} {self.units}</p>
        <p style="font-size: 24px;">Leg 4: {strings[3]} {self.units}</p>
        """


