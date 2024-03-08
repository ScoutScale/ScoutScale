import serial.tools.list_ports
from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QVBoxLayout, QLabel, QButtonGroup, QComboBox
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtGui import QFont
import os


class ConfigurationWindow(QDialog):

    change_units_signal = pyqtSignal(str)
    change_output_file_signal = pyqtSignal(str)

    def __init__(self, style_guide, config_parameters, default_output_file, units, serial_thread, parent=None):
        super().__init__(parent)

        configuration_view_style = style_guide.get("configuration view", {})
        window_style = configuration_view_style.get("window", {})
        dialog_styles = configuration_view_style.get("dialogs", {})
        button_styles = configuration_view_style.get("buttons", {})

        self.configuration_window_title = window_style.get("title")
        self.configuration_window_color = window_style.get("color")
        self.configuration_window_width = window_style.get("width")
        self.configuration_window_height = window_style.get("height")
        self.configuration_window_auto_size = window_style.get("auto size")

        self.ports_dialog_text = dialog_styles.get("ports", {}).get("text")
        self.ports_dialog_font = dialog_styles.get("ports", {}).get("font")
        self.ports_dialog_text_color = dialog_styles.get("ports", {}).get("text color")
        self.ports_dialog_text_size = dialog_styles.get("ports", {}).get("text size")

        self.units_dialog_text = dialog_styles.get("units", {}).get("text")
        self.units_dialog_font = dialog_styles.get("units", {}).get("font")
        self.units_dialog_text_color = dialog_styles.get("units", {}).get("text color")
        self.units_dialog_text_size = dialog_styles.get("units", {}).get("text size")

        self.output_file_dialog_text = dialog_styles.get("output file", {}).get("text")
        self.output_file_font = dialog_styles.get("output file", {}).get("font")
        self.output_file_text_color = dialog_styles.get("output file", {}).get("text color")
        self.output_file_text_size = dialog_styles.get("output file", {}).get("text size")

        self.exit_button_label = button_styles.get("exit", {}).get("label")
        self.exit_button_color = button_styles.get("exit", {}).get("color")
        self.exit_button_font = button_styles.get("exit", {}).get("font")
        self.exit_button_text_color = button_styles.get("exit", {}).get("text color")
        self.exit_button_text_size = button_styles.get("exit", {}).get("text size")
        self.exit_button_border = button_styles.get("exit", {}).get("border")
        self.exit_button_border_radius = button_styles.get("exit", {}).get("border radius")

        self.radio_button_ports_font = button_styles.get("radio buttons", {}).get("ports", {}).get("font")
        self.radio_button_ports_text_color = button_styles.get("radio buttons", {}).get("ports", {}).get("text color")
        self.radio_button_ports_text_size = button_styles.get("radio buttons", {}).get("ports", {}).get("text size")

        self.radio_button_units_font = button_styles.get("radio buttons", {}).get("units", {}).get("font")
        self.radio_button_units_text_color = button_styles.get("radio buttons", {}).get("units", {}).get("text color")
        self.radio_button_units_text_size = button_styles.get("radio buttons", {}).get("units", {}).get("text size")

        self.mock_ports = config_parameters["Serial"]["mock ports"]
        self.supported_units = config_parameters["weight units"]["compatible units"]
        self.data_folder = config_parameters["Local Data Collection"]["folder"]

        self.current_unit = units
        self.serial_thread = serial_thread
        self.default_output_file = default_output_file

        self.port_button_group = QButtonGroup(self)
        self.unit_button_group = QButtonGroup(self)

        self.init_UI()

    def init_UI(self):

        self.setWindowTitle(self.configuration_window_title)
        self.setStyleSheet(f"background-color: {self.configuration_window_color};")

        self.layout = QVBoxLayout(self)
        
        port_label = QLabel(self.ports_dialog_text)
        port_label.setFont(QFont(self.ports_dialog_font, self.ports_dialog_text_size))
        self.setStyleSheet(f"color: {self.ports_dialog_text_color}")
        self.layout.addWidget(port_label)

        self.ports_layout = QVBoxLayout()
        self.populate_ports()

        port_label = QLabel(self.units_dialog_text)
        port_label.setFont(QFont(self.units_dialog_font, self.units_dialog_text_size))
        port_label.setStyleSheet(f"color: {self.units_dialog_text_color}")
        self.layout.addWidget(port_label)

        self.units_layout = QVBoxLayout()
        self.populate_units()

        port_label = QLabel(self.output_file_dialog_text)
        port_label.setFont(QFont(self.output_file_font, self.output_file_text_size))
        port_label.setStyleSheet(f"color: {self.output_file_text_color}")
        self.layout.addWidget(port_label)

        self.file_combo_box = QComboBox()
        self.file_combo_box.currentIndexChanged.connect(self.on_file_selected)
        self.populate_files()
        self.set_default_selected_file()
        self.layout.addWidget(self.file_combo_box)

        self.layout.addStretch()

        kill_button = QPushButton(self.exit_button_label)
        kill_button.setFont(QFont(self.exit_button_font, self.exit_button_text_size))
        kill_button.setStyleSheet(f"""QPushButton {{
                                  background-color: {self.exit_button_color}; 
                                  color: {self.exit_button_text_color}; 
                                  border: {self.exit_button_border}; 
                                  border-radius: {self.exit_button_border_radius}; }}""")
        kill_button.clicked.connect(QCoreApplication.quit)
        self.layout.addWidget(kill_button)

        if not self.configuration_window_auto_size:
            self.resize(self.configuration_window_width, self.configuration_window_height)

    def populate_ports(self):
        ports = self.get_available_serial_ports()

        for port in ports:
            button = QRadioButton(port, self)
            button.setFont(QFont(self.radio_button_ports_font, self.radio_button_ports_text_size))
            button.setStyleSheet(f"color: {self.radio_button_ports_text_color}")
            button.setChecked(port == self.serial_thread.serial_port_name)
            button.toggled.connect(lambda checked, port=port: self.on_port_radio_button_toggled(checked, port))
            self.port_button_group.addButton(button)
            self.ports_layout.addWidget(button)

        self.layout.addLayout(self.ports_layout)
    
    def on_port_radio_button_toggled(self, checked, port):
        if checked:
            self.serial_thread.change_port_signal.emit(port)

    def get_available_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        port_list += self.mock_ports
        return port_list

    def populate_units(self):

        for possible_unit in self.supported_units:
            button = QRadioButton(possible_unit, self)
            button.setFont(QFont(self.radio_button_units_font, self.radio_button_units_text_size))
            button.setStyleSheet(f"color: {self.radio_button_units_text_color}")
            button.setChecked(possible_unit == self.current_unit)
            button.toggled.connect(lambda checked, unit=possible_unit: self.on_units_radio_button_toggled(checked, unit))
            self.unit_button_group.addButton(button)
            self.units_layout.addWidget(button)

        self.layout.addLayout(self.units_layout)

    def on_units_radio_button_toggled(self, checked, unit):
        if checked:
            self.change_units_signal.emit(unit)

    def populate_files(self):
        data_files = os.listdir(self.data_folder)
        for file_name in data_files:
            self.file_combo_box.addItem(file_name)

    def on_file_selected(self):
        selected_file = self.file_combo_box.currentText()
        self.change_output_file_signal.emit(selected_file)

    def set_default_selected_file(self):
        default_file_name =self.default_output_file
        index = self.file_combo_box.findText(default_file_name)
        if index != -1:
            self.file_combo_box.setCurrentIndex(index)
    



