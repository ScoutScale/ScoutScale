import serial.tools.list_ports
from PyQt5.QtWidgets import QDialog, QRadioButton, QVBoxLayout

class ConfigurationWindow(QDialog):
    def __init__(self, config_parameters, serial_thread, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration Menu")
        self.resize(400, 300)
        self.config_parameters = config_parameters
        self.serial_thread = serial_thread
        self.ports_layout = QVBoxLayout(self)
        self.populate_ports()

    def populate_ports(self):
        ports = self.get_available_serial_ports()

        for port in ports:
            button = QRadioButton(port, self)
            button.setChecked(port == self.serial_thread.serial_port_name)
            button.toggled.connect(lambda checked, port=port: self.on_radio_button_toggled(checked, port))
            self.ports_layout.addWidget(button)

        self.ports_layout.addStretch()

    def on_radio_button_toggled(self, checked, port):
        if checked:
            self.serial_thread.change_port_signal.emit(port) 

    def get_available_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        port_list += self.config_parameters["mock_ports"]
        return port_list
