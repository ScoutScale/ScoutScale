import os
import sys
import pandas as pd
import firebase_admin
import socket

from firebase_admin import credentials
from firebase_admin import firestore
from yaml import safe_load
from datetime import datetime
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                             QDialog, QFrame, QDesktopWidget)

from _views.configuration_view import ConfigurationWindow
from _views.capture_view import CaptureWindow
from _views.calibrate_view import CalibrateWindow
from _views.tare_view import TareWindow
from _views.info_view import InfoWindow
from _views.qr_code_view import QRCodeWindow
from _views.confirm_action_view import ConfirmWindow
from _views.message_view import MessageWindow
from _views.check_list_view import ChecklistWindow
from _serial.serial_thread import SerialReaderThread
from _views.debug_view import DebugWindow

class SideMenu(QFrame):
    delete_last_entry_signal = pyqtSignal()
    debug_signal = pyqtSignal()
    generate_qr_code_signal = pyqtSignal()
    show_check_list_signal = pyqtSignal()
    show_configuration_menu_signal = pyqtSignal()

    def __init__(self, style_guide):
        super().__init__()

        self.style_guide = style_guide

        menu_buttons = style_guide.get("main view", {}).get("header", {}).get("buttons", {}).get("menu", {}).get("buttons", {})

        self.checklist_button_label = menu_buttons.get("checklist", {}).get("label")
        self.checklist_button_label_font = menu_buttons.get("checklist", {}).get("label font")
        self.checklist_button_label_text_size = menu_buttons.get("checklist", {}).get("label text size")
        self.checklist_button_label_color = menu_buttons.get("checklist", {}).get("label color")
        self.checklist_button_padding = menu_buttons.get("checklist", {}).get("padding")
        self.checklist_button_text_alignment = menu_buttons.get("checklist", {}).get("text alignment")
        self.checklist_button_width = menu_buttons.get("checklist", {}).get("width")
        self.checklist_button_height = menu_buttons.get("checklist", {}).get("height")

        self.delete_last_entry_button_label = menu_buttons.get("delete entry", {}).get("label")
        self.delete_last_entry_button_label_font = menu_buttons.get("delete entry", {}).get("label font")
        self.delete_last_entry_button_label_text_size = menu_buttons.get("delete entry", {}).get("label text size")
        self.delete_last_entry_button_label_color = menu_buttons.get("delete entry", {}).get("label color")
        self.delete_last_entry_button_padding = menu_buttons.get("delete entry", {}).get("padding")
        self.delete_last_entry_button_text_alignment = menu_buttons.get("delete entry", {}).get("text alignment")
        self.delete_last_entry_button_width = menu_buttons.get("delete entry", {}).get("width")
        self.delete_last_entry_button_height = menu_buttons.get("delete entry", {}).get("height")

        self.qr_code_button_image_location = menu_buttons.get("qr code", {}).get("image", {}).get("location")
        self.qr_code_button_image_width = menu_buttons.get("qr code", {}).get("image", {}).get("width")
        self.qr_code_button_image_height = menu_buttons.get("qr code", {}).get("image", {}).get("height")
        self.qr_code_button_width = menu_buttons.get("qr code", {}).get("width")
        self.qr_code_button_height = menu_buttons.get("qr code", {}).get("height")
        self.qr_code_button_border = menu_buttons.get("qr code", {}).get("border")

        self.settings_button_label = menu_buttons.get("settings", {}).get("label")
        self.settings_button_label_font = menu_buttons.get("settings", {}).get("label font")
        self.settings_button_label_text_size = menu_buttons.get("settings", {}).get("label text size")
        self.settings_button_label_color = menu_buttons.get("settings", {}).get("label color")
        self.settings_button_padding = menu_buttons.get("settings", {}).get("padding")
        self.settings_button_text_alignment = menu_buttons.get("settings", {}).get("text alignment")
        self.settings_button_width = menu_buttons.get("settings", {}).get("width")
        self.settings_button_height = menu_buttons.get("settings", {}).get("height")

        self.debug_button_label = menu_buttons.get("debug", {}).get("label")
        self.debug_button_label_font = menu_buttons.get("debug", {}).get("label font")
        self.debug_button_label_text_size = menu_buttons.get("debug", {}).get("label text size")
        self.debug_button_label_color = menu_buttons.get("debug", {}).get("label color")
        self.debug_button_color = menu_buttons.get("debug", {}).get("color")
        self.debug_button_padding = menu_buttons.get("debug", {}).get("padding")
        self.debug_button_text_alignment = menu_buttons.get("debug", {}).get("text alignment")
        self.debug_button_width = menu_buttons.get("debug", {}).get("width")
        self.debug_button_height = menu_buttons.get("debug", {}).get("height")

        self.exit_button_label = menu_buttons.get("exit", {}).get("label")
        self.exit_button_label_font = menu_buttons.get("exit", {}).get("label font")
        self.exit_button_label_text_size = menu_buttons.get("exit", {}).get("label text size")
        self.exit_button_label_color = menu_buttons.get("exit", {}).get("label color")
        self.exit_button_color = menu_buttons.get("exit", {}).get("color")
        self.exit_button_padding = menu_buttons.get("exit", {}).get("padding")
        self.exit_button_text_alignment = menu_buttons.get("exit", {}).get("text alignment")
        self.exit_button_width = menu_buttons.get("exit", {}).get("width")
        self.exit_button_height = menu_buttons.get("exit", {}).get("height")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(6)

        settings_button_font = QFont(self.settings_button_label_font, self.settings_button_label_text_size)
        settings_button_font.setWeight(QFont.Bold)


        self.settings_button = QPushButton(self.settings_button_label)
        self.settings_button.setFont(settings_button_font)
        self.settings_button.setStyleSheet(F"""
                                            color: {self.settings_button_label_color}; 
                                            padding-top: {self.settings_button_padding}; 
                                            text-align: {self.settings_button_text_alignment};""")
        self.settings_button.setFlat(True)
        self.settings_button.setFixedSize(QSize(self.settings_button_width, self.settings_button_height)) 
        self.settings_button.clicked.connect(self.show_configuration_menu_signal.emit)
        layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)


        checklist_button_font = QFont(self.checklist_button_label_font, self.checklist_button_label_text_size)
        checklist_button_font.setWeight(QFont.Bold)

        self.checklist_button = QPushButton(self.checklist_button_label)
        self.checklist_button.setFont(checklist_button_font)
        self.checklist_button.setStyleSheet(F"""
                                            color: {self.checklist_button_label_color}; 
                                            padding-top: {self.checklist_button_padding}; 
                                            text-align: {self.checklist_button_text_alignment};""")
        self.checklist_button.setFlat(True)
        self.checklist_button.setFixedSize(QSize(self.checklist_button_width, self.checklist_button_height)) 
        self.checklist_button.clicked.connect(self.show_check_list_signal.emit)
        layout.addWidget(self.checklist_button, alignment=Qt.AlignCenter)

        self.qr_button = QPushButton()
        self.qr_button.setIcon(QIcon(self.qr_code_button_image_location)) 
        self.qr_button.setIconSize(QSize(self.qr_code_button_image_width, self.qr_code_button_image_height))
        self.qr_button.setFixedSize(QSize(self.qr_code_button_width, self.qr_code_button_height))
        self.qr_button.setStyleSheet(f"border: {self.qr_code_button_border};")
        self.qr_button.clicked.connect(self.generate_qr_code_signal.emit)
        layout.addWidget(self.qr_button, alignment=Qt.AlignCenter)

        delete_last_entry_button_font = QFont(self.delete_last_entry_button_label_font, self.delete_last_entry_button_label_text_size)
        delete_last_entry_button_font.setWeight(QFont.Bold)

        self.delete_last_entry_button = QPushButton(self.delete_last_entry_button_label)
        self.delete_last_entry_button.setFont(delete_last_entry_button_font)
        self.delete_last_entry_button.setStyleSheet(F"""
                                            color: {self.delete_last_entry_button_label_color}; 
                                            padding-top: {self.delete_last_entry_button_padding}; 
                                            text-align: {self.delete_last_entry_button_text_alignment};""")
        self.delete_last_entry_button.setFlat(True)
        self.delete_last_entry_button.setFixedSize(QSize(self.delete_last_entry_button_width, self.delete_last_entry_button_height)) 
        self.delete_last_entry_button.clicked.connect(self.delete_last_entry_signal.emit)
        layout.addWidget(self.delete_last_entry_button, alignment=Qt.AlignCenter)

        debug_button_font = QFont(self.debug_button_label_font,
                                  self.debug_button_label_text_size)
        debug_button_font.setWeight(QFont.Bold)

        self.debug_button = QPushButton(self.debug_button_label)
        self.debug_button.setFont(debug_button_font)
        self.debug_button.setStyleSheet(F"""
                                                    color: {self.debug_button_label_color}; 
                                                    padding-top: {self.debug_button_padding}; 
                                                    text-align: {self.debug_button_text_alignment};""")
        self.debug_button.setFlat(True)
        self.debug_button.setFixedSize(
            QSize(self.debug_button_width, self.debug_button_height))
        self.debug_button.clicked.connect(self.debug_signal.emit)
        layout.addWidget(self.debug_button, alignment=Qt.AlignCenter)

        layout.addStretch()

        exit_button_font = QFont(self.exit_button_label_font, self.exit_button_label_text_size)
        exit_button_font.setWeight(QFont.Bold)

        self.exit_button = QPushButton(self.exit_button_label)
        self.exit_button.setFont(exit_button_font)
        self.exit_button.setStyleSheet(F"""
                                        background-color: {self.exit_button_color};
                                        color: {self.exit_button_label_color}; 
                                        padding-top: {self.exit_button_padding}; 
                                        text-align: {self.exit_button_text_alignment};""")
        self.exit_button.setFlat(True)
        self.exit_button.setFixedSize(QSize(self.exit_button_width, self.exit_button_height)) 
        self.exit_button.clicked.connect(self.exit_button_pressed)
        layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.hide()

    def exit_button_pressed(self):
        confirm_window = ConfirmWindow(self.style_guide, "end program")
        if confirm_window.exec_():
            QCoreApplication.quit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.retrieve_config_file()
        self.retrieve_style_guide()

        self.get_main_window_style_guide_parameters()

        self.prev_capture_available = False

        self.weight = 0

        cred = credentials.Certificate(self.config_parameters["Firebase"]["key"])
        firebase_admin.initialize_app(cred)

        self.units = self.config_parameters["weight units"]["default unit"]
        self.known_weight = float(self.config_parameters["known weight"]["default"])

        self.selected_serial_port = self.config_parameters["Serial"]["mock ports"][0]
        self.uploading = self.config_parameters["Firebase"]["uploading data"]
        
        self.connect_to_output_file("__init__")

        self.serial_thread = SerialReaderThread(self.config_parameters, self.selected_serial_port)
        self.connect_signals()
        self.serial_thread.start()

        self.init_UI()
    
    def retrieve_config_file(self):
        with open("_config/config.yaml", 'r') as file:
            self.config_parameters = safe_load(file)

    def retrieve_style_guide(self):
        with open("_config/style_guide.yaml", 'r') as file:
            self.style_guide = safe_load(file)

    def connect_signals(self):

        self.serial_thread.new_data.connect(self.update_weight)

        self.serial_thread.tare_signal.connect(self.serial_thread.tare_scale)

        self.serial_thread.tare_in_progress_signal.connect(self.show_tare_menu)

        self.serial_thread.tare_complete_signal.connect(self.close_tare_menu)

        self.serial_thread.calibrate_signal.connect(self.serial_thread.calibrate_scale)

        self.serial_thread.zeroed_out_signal.connect(self.serial_thread.zeroed_scale)

        self.serial_thread.calibrate_capture_signal.connect(self.serial_thread.capture_calibrated_weight_scale)

        self.serial_thread.calibrated_weight_scale_value_signal.connect(self.serial_thread.calibrated_weight_scale_value)

        self.serial_thread.calibration_abort_signal.connect(self.serial_thread.send_calibration_abort_signal)

        self.serial_thread.change_port_signal.connect(self.serial_thread.connect_to_serial_port)

    def closeEvent(self, event):
        self.terminate()
        super().closeEvent(event)

    def terminate(self):
        QCoreApplication.quit()
        self.serial_thread.terminate()
        super().close()

    def get_main_window_style_guide_parameters(self):
        main_view_style = self.style_guide.get("main view", {})
        window_style = main_view_style.get("window", {})
        header_style = main_view_style.get("header", {})
        dynamic_font_resizing_style = main_view_style.get("dynamic font resizing", {})
        label_styles = main_view_style.get("labels", {})
        button_styles = main_view_style.get("buttons", {})

        self.main_window_title = window_style.get("title")
        self.main_window_color = window_style.get("color")
        self.main_window_width = window_style.get("width")
        self.main_window_height = window_style.get("height")
        self.main_window_auto_size = window_style.get("auto size")

        header_buttons = header_style.get("buttons", {})
        scoutscale_button_info = header_buttons.get("ScoutScale", {})
        self.scoutscale_image_location = scoutscale_button_info.get("image", {}).get("location")
        self.scoutscale_image_width = scoutscale_button_info.get("image", {}).get("width")
        self.scoutscale_image_height = scoutscale_button_info.get("image", {}).get("height")
        self.scoutscale_button_width = scoutscale_button_info.get("width", {})
        self.scoutscale_button_height = scoutscale_button_info.get("height", {})
        self.scoutscale_button_border = scoutscale_button_info.get("border", {})

        self.menu_button_label = header_buttons.get("menu", {}).get("label")
        self.menu_button_label_font = header_buttons.get("menu", {}).get("label font")
        self.menu_button_label_text_size = header_buttons.get("menu", {}).get("label text size")
        self.menu_button_label_color = header_buttons.get("menu", {}).get("label color")
        self.menu_button_padding = header_buttons.get("menu", {}).get("padding")
        self.menu_button_text_alignment = header_buttons.get("menu", {}).get("text alignment")
        self.menu_button_width = header_buttons.get("menu", {}).get("width")
        self.menu_button_height = header_buttons.get("menu", {}).get("height")

        self.header_title = header_style.get("title")
        self.header_font = header_style.get("font")
        self.header_text_size = header_style.get("text size")
        self.header_text_color = header_style.get("text color")

        self.window_divisor = dynamic_font_resizing_style.get("window divisor")
        self.weight_display_correction = dynamic_font_resizing_style.get("weight display correction")

        self.current_weight_label_text = label_styles.get("current weight", {}).get("text")
        self.current_weight_label_font = label_styles.get("current weight", {}).get("font")
        self.current_weight_label_text_color = label_styles.get("current weight", {}).get("text color")

        self.capture_button_label = button_styles.get("capture button", {}).get("label")
        self.capture_button_color = button_styles.get("capture button", {}).get("color")
        self.capture_button_font_style = button_styles.get("capture button", {}).get("font")
        self.capture_button_text_color = button_styles.get("capture button", {}).get("text color")
        self.capture_button_border = button_styles.get("capture button", {}).get("border")
        self.capture_button_border_radius = button_styles.get("capture button", {}).get("border radius")

        self.tare_button_label = button_styles.get("tare button", {}).get("label")
        self.tare_button_color = button_styles.get("tare button", {}).get("color")
        self.tare_button_font_style = button_styles.get("tare button", {}).get("font")
        self.tare_button_text_color = button_styles.get("tare button", {}).get("text color")
        self.tare_button_border = button_styles.get("tare button", {}).get("border")
        self.tare_button_border_radius = button_styles.get("tare button", {}).get("border radius")

        self.calibrate_button_label = button_styles.get("calibrate button", {}).get("label")
        self.calibrate_button_color = button_styles.get("calibrate button", {}).get("color")
        self.calibrate_button_font_style = button_styles.get("calibrate button", {}).get("font")
        self.calibrate_button_text_color = button_styles.get("calibrate button", {}).get("text color")
        self.calibrate_button_border = button_styles.get("calibrate button", {}).get("border")
        self.calibrate_button_border_radius = button_styles.get("calibrate button", {}).get("border radius")

        
    def init_UI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle(self.main_window_title)
        self.centralWidget.setStyleSheet(f"background-color: {self.main_window_color};") 

        layout = QHBoxLayout()

        main_view = QVBoxLayout()

        row1 = QHBoxLayout()

        self.image_button = QPushButton()
        self.image_button.setIcon(QIcon(self.scoutscale_image_location))
        self.image_button.setIconSize(QSize(self.scoutscale_image_width, self.scoutscale_image_height))
        self.image_button.setFixedSize(self.scoutscale_button_width, self.scoutscale_button_height)
        self.image_button.setStyleSheet(f"border: {self.scoutscale_button_border};")
        self.image_button.clicked.connect(self.show_information_page)
        row1.addWidget(self.image_button)

        scout_scale_logo_font = QFont(self.header_font, self.header_text_size)
        scout_scale_logo_font.setWeight(QFont.Bold)

        title = QLabel(self.header_title)
        title.setFont(scout_scale_logo_font)
        title.setStyleSheet(f"color: {self.header_text_color};") 
        row1.addWidget(title)

        row1.addStretch()

        hamburger_button_font = QFont(self.menu_button_label_font, self.menu_button_label_text_size)
        hamburger_button_font.setWeight(QFont.Bold)

        self.hamburger_button = QPushButton(self.menu_button_label)
        self.hamburger_button.setFont(hamburger_button_font)
        self.hamburger_button.setStyleSheet(F"""
                                            color: {self.menu_button_label_color}; 
                                            padding-top: {self.menu_button_padding}; 
                                            text-align: {self.menu_button_text_alignment};""")
        self.hamburger_button.setFlat(True)
        self.hamburger_button.setFixedSize(QSize(self.menu_button_width, self.menu_button_height)) 
        self.hamburger_button.clicked.connect(self.toggle_side_menu)
        row1.addWidget(self.hamburger_button)

        main_view.addLayout(row1)

        self.weight_display = QLabel(self.current_weight_label_text)
        self.weight_display_font = QFont(self.current_weight_label_font)
        self.weight_display_font.setBold(True)
        self.weight_display.setFont(self.weight_display_font)
        self.weight_display.setStyleSheet(f"color: {self.current_weight_label_text_color};") 
        main_view.addWidget(self.weight_display, alignment=Qt.AlignCenter)

        self.capture_button = QPushButton(self.capture_button_label)
        self.capture_button_font = QFont(self.capture_button_font_style)
        self.capture_button_font.setBold(True)
        self.capture_button.setFont(QFont(self.capture_button_font))
        self.capture_button.setStyleSheet(f"""QPushButton {{ 
                                          background-color: {self.capture_button_color}; 
                                          color: {self.capture_button_text_color}; 
                                          border: {self.capture_button_border}; 
                                          border-radius: {self.capture_button_border_radius}; }}""")
        self.capture_button.clicked.connect(self.capture_scale_output)
        main_view.addWidget(self.capture_button)

        self.tare_button = QPushButton(self.tare_button_label)
        self.tare_button_font = QFont(self.tare_button_font_style)
        self.tare_button_font.setBold(True)
        self.tare_button.setFont(self.tare_button_font)
        self.tare_button.setStyleSheet(f"""QPushButton {{
                                       background-color: {self.tare_button_color}; 
                                       color: {self.tare_button_text_color}; 
                                       border: {self.tare_button_border}; 
                                       border-radius: {self.tare_button_border_radius}; }}""")
        self.tare_button.clicked.connect(self.tare_scale)
        main_view.addWidget(self.tare_button)

        self.calibrate_button = QPushButton(self.calibrate_button_label)
        self.calibrate_button_font = QFont(self.calibrate_button_font_style)
        self.calibrate_button_font.setBold(True)
        self.calibrate_button.setFont(self.calibrate_button_font)
        self.calibrate_button.setStyleSheet(f"""QPushButton {{
                                background-color: {self.calibrate_button_color}; 
                                color: {self.calibrate_button_text_color}; 
                                border: {self.calibrate_button_border}; 
                                border-radius: {self.calibrate_button_border_radius}; }}""")
        self.calibrate_button.clicked.connect(self.calibrate_scale)
        main_view.addWidget(self.calibrate_button)

        layout.addLayout(main_view)

        self.centralWidget.setLayout(layout)

        self.side_menu = SideMenu(self.style_guide)
        self.side_menu.delete_last_entry_signal.connect(self.delete_previous_capture)
        self.side_menu.show_check_list_signal.connect(self.toggle_checklist)
        self.side_menu.debug_signal.connect(self.toggle_debug)
        self.side_menu.generate_qr_code_signal.connect(self.generate_qr_code)
        self.side_menu.show_configuration_menu_signal.connect(self.show_configuration_menu)
        self.side_menu_layout = QVBoxLayout()
        self.side_menu_layout.addWidget(self.side_menu)
        self.side_menu_layout.setAlignment(Qt.AlignRight)
        self.centralWidget.layout().addLayout(self.side_menu_layout)

        self.checklist = ChecklistWindow(self.style_guide, self)

        self.debug = DebugWindow(self.style_guide, self.units, self.serial_thread, self)
        self.debug.hide()

        if not self.main_window_auto_size:
            self.resize(self.main_window_width, self.main_window_height)
        
        self.center_on_screen()

    def toggle_side_menu(self):
        if self.side_menu.isVisible():
            self.side_menu.hide()
        else:
            self.side_menu.show()

    def show_configuration_menu(self):
        csv_file_name = self.csv_file.replace(self.config_parameters["Local Data Collection"]["folder"], "")
        config_window = ConfigurationWindow(self.style_guide, self.config_parameters, csv_file_name, self.units, self.known_weight, self.serial_thread, self)
        config_window.change_units_signal.connect(self.update_units)
        config_window.change_output_file_signal.connect(self.connect_to_output_file)
        config_window.change_known_weights_signal.connect(self.update_known_weight)
        config_window.exec_()
    
    def connect_to_output_file(self, file_name):
        self.prev_capture_available = False

        date_header = self.config_parameters["Local Data Collection"]["labels"]["date"]
        weight_header = self.config_parameters["Local Data Collection"]["labels"]["weight"]
        unit_header = self.config_parameters["Local Data Collection"]["labels"]["units"]
        zone_header = self.config_parameters["Local Data Collection"]["labels"]["zone"]

        if self.config_parameters["Local Data Collection"]["new file creation mode"] is True:
            self.csv_file = self.config_parameters["Local Data Collection"]["folder"] + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
            pd.DataFrame(columns=[date_header, weight_header, unit_header, zone_header]).to_csv(self.csv_file, index=False)
        else:
            if file_name != "__init__":
                self.csv_file = self.config_parameters["Local Data Collection"]["folder"] + file_name
            else:
                self.csv_file = self.config_parameters["Local Data Collection"]["folder"] + self.config_parameters["Local Data Collection"]["default file name"]

            if not os.path.exists(self.csv_file):
                pd.DataFrame(columns=[date_header, weight_header, unit_header, zone_header]).to_csv(self.csv_file, index=False, mode='w')


    def show_information_page(self):
        self.InfoWindow = InfoWindow(self.style_guide)
        self.InfoWindow.exec_()

    def tare_scale(self):
        self.serial_thread.tare_signal.emit()
    
    def show_tare_menu(self):
        self.tare_menu = TareWindow(self.style_guide)
        self.tare_menu.exec_()
    
    def close_tare_menu(self):
        self.tare_menu.accept()

    def calibrate_scale(self):
        self.serial_thread.calibrate_signal.emit() 
        calibrate_window = CalibrateWindow(self.style_guide, self.config_parameters, self.units, self.serial_thread)
        calibrate_window.exec_()  

    def capture_scale_output(self):
        temp_weight = self.weight
        capture_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        date_header = self.config_parameters["Local Data Collection"]["labels"]["date"]
        weight_header = self.config_parameters["Local Data Collection"]["labels"]["weight"]
        unit_header = self.config_parameters["Local Data Collection"]["labels"]["units"]
        zone_header = self.config_parameters["Local Data Collection"]["labels"]["zone"]

        desktop = QApplication.desktop()
        desktop_rect = desktop.availableGeometry()
        capture_window = CaptureWindow(self.style_guide, temp_weight, self.units, self.debug.isVisible(), desktop_rect, self.known_weight)
        if capture_window.exec_() == QDialog.Accepted:
            zone = capture_window.text_box.text()
            
            if zone != "" and temp_weight != 0:
                pd.DataFrame([[capture_date, temp_weight, self.units, zone]], columns=[date_header, weight_header, unit_header, zone_header]).to_csv(self.csv_file, mode='a', header=False, index=False)
                self.send_to_backend(temp_weight, zone) 
                self.prev_capture_available = True
    
    def delete_previous_capture(self):
        confirm_window = ConfirmWindow(self.style_guide, "delete entry")
        if confirm_window.exec_():
            if self.prev_capture_available:
                try:
                    df = pd.read_csv(self.csv_file)
                except FileNotFoundError:
                    df = pd.DataFrame()

                if not df.empty:
                    previous_entry = df.iloc[-1]
                    
                    df = df.drop(df.index[-1])
                    df.to_csv(self.csv_file, index=False)

                    if self.uploading:
                        db = firestore.client()
                        data = {
                        "Device ID" : socket.gethostname(),
                        self.config_parameters["Firebase"]["labels"]["weight"] : float(-previous_entry[1]),
                        self.config_parameters["Firebase"]["labels"]["units"] : previous_entry[2],
                        self.config_parameters["Firebase"]["labels"]["date"] : firestore.SERVER_TIMESTAMP,
                        self.config_parameters["Firebase"]["labels"]["zone"] : int(previous_entry[3])
                        }
                        doc_ref = db.collection(self.config_parameters["Firebase"]["collection name"]).document()
                        doc_ref.set(data)
                    self.prev_capture_available = False

            else:
                window = MessageWindow(self.style_guide, "no prev entry")
                window.exec()

    def update_weight(self, weight: str):
        self.weight = round(sum([float(split_weight) for split_weight in weight.split(":")]), self.config_parameters["output rounding"]["decimal place"])
        self.update_weight_display()

    def update_units(self, units):
        self.units = units
        self.debug.units = units

    def update_known_weight(self, known_weight):
        self.known_weight = known_weight

    def update_weight_display(self):
        self.weight_display.setText(f"{self.current_weight_label_text} {self.weight} {self.units}")

    def send_to_backend(self, weight, zone):
        if self.uploading:
            db = firestore.client()
            data = {
            "Device ID" : socket.gethostname(),
            self.config_parameters["Firebase"]["labels"]["weight"] : float(weight),
            self.config_parameters["Firebase"]["labels"]["units"] : self.units,
            self.config_parameters["Firebase"]["labels"]["date"] : firestore.SERVER_TIMESTAMP,
            self.config_parameters["Firebase"]["labels"]["zone"] : int(zone)
            }
            doc_ref = db.collection(self.config_parameters["Firebase"]["collection name"]).document()
            doc_ref.set(data)

    def generate_qr_code(self):
        qr_code_menu = QRCodeWindow(self. style_guide, self.config_parameters["web app URL"], self)
        qr_code_menu.exec_()

    def resizeEvent(self, event):
        font_size = event.size().height() // self.window_divisor
        self.weight_display_font.setPointSize(font_size + 10)
        self.capture_button_font.setPointSize(font_size)
        self.tare_button_font.setPointSize(font_size)
        self.calibrate_button_font.setPointSize(font_size)

        self.weight_display.setFont(self.weight_display_font)
        self.capture_button.setFont(self.capture_button_font)
        self.tare_button.setFont(self.tare_button_font)
        self.calibrate_button.setFont(self.calibrate_button_font)
        super().resizeEvent(event)

    def toggle_checklist(self):
        if self.checklist.isVisible():
            self.checklist.hide()
        else:
            self.checklist.show()

    def toggle_debug(self):
        if self.debug.isVisible():
            self.debug.hide()
        else:
            self.debug.show()
        
    def center_on_screen(self):
        window_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
