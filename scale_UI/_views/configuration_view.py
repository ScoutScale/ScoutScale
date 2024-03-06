import serial.tools.list_ports
from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QVBoxLayout, QLabel, QButtonGroup
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtGui import QFont

class ConfigurationWindow(QDialog):

    change_units_signal = pyqtSignal(str)

    def __init__(self, config_parameters, units, serial_thread, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Menu")
        self.resize(400, 300)
        self.mock_ports = config_parameters["mock ports"]
        self.supported_units = config_parameters["units"]
        self.current_unit = units
        self.serial_thread = serial_thread

        self.port_button_group = QButtonGroup(self)
        self.unit_button_group = QButtonGroup(self)

        self.init_UI()

    def init_UI(self):
        self.label_font = QFont()
        self.label_font.setPointSize(20)

        self.button_font = QFont()
        self.button_font.setPointSize(16)

        self.layout = QVBoxLayout(self)
        
        port_label = QLabel("Serial Ports")
        port_label.setFont(self.label_font)
        self.layout.addWidget(port_label)

        self.ports_layout = QVBoxLayout()
        self.populate_ports()

        port_label = QLabel("Output Units")
        port_label.setFont(self.label_font)
        self.layout.addWidget(port_label)

        self.units_layout = QVBoxLayout()
        self.populate_units()

        self.layout.addStretch()

        kill_button = QPushButton("Exit Program")
        kill_button.setFont(self.button_font)
        kill_button.setStyleSheet("QPushButton {background-color: rgb(210, 54, 54); color: white; border: 2px solid black; border-radius: 10px; }")
        kill_button.clicked.connect(QCoreApplication.quit)
        self.layout.addWidget(kill_button)

    def populate_ports(self):
        ports = self.get_available_serial_ports()

        for port in ports:
            button = QRadioButton(port, self)
            button.setFont(self.button_font)
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
            button.setFont(self.button_font)
            button.setChecked(possible_unit == self.current_unit)
            button.toggled.connect(lambda checked, unit=possible_unit: self.on_units_radio_button_toggled(checked, unit))
            self.unit_button_group.addButton(button)
            self.units_layout.addWidget(button)

        self.layout.addLayout(self.units_layout)

    def on_units_radio_button_toggled(self, checked, unit):
        if checked:
            self.change_units_signal.emit(unit)



