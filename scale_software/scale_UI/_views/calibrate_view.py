from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import QEventLoop
from PyQt5.QtGui import QFont

from _views.known_weight_view import KnownWeightWindow

class CalibrateWindow(QDialog):
    def __init__(self, style_guide, config_parameters, units, serial_thread, parent=None):
        super().__init__(parent)

        calibrate_view_style = style_guide.get("calibrate view", {})
        self.window_title, self.window_color, self.window_width, self.window_height, self.auto_size= (
            calibrate_view_style.get("window", {}).get(key) for key in ("title", "color", "width", "height", "auto size")
        )
        (self.dialog_font, self.dialog_text_size, self.dialog_text_color, self.zero_dialog, self.initial_weight_dialog, 
         self.subsequent_weight_dialog, self.calibrating_dialog, self.calibration_complete_dialog, self.calibration_aborted_dialog) = (
            calibrate_view_style.get("dialogs", {}).get(key) for key in ("font", "text size", "text color", "zero", "initial weight", 
                                                                         "subsequent weight", "calibrating", "calibration complete", "calibration aborted")
        )
        zero_button_style = calibrate_view_style.get("buttons", {}).get("zero", {})
        self.zero_button_label = zero_button_style.get("label")
        self.zero_button_active_color = zero_button_style.get("active color")
        self.zero_button_disabled_color = zero_button_style.get("disabled color")
        self.zero_button_font = zero_button_style.get("font")
        self.zero_button_text_color = zero_button_style.get("text color")
        self.zero_button_text_size = zero_button_style.get("text size")
        self.zero_button_border = zero_button_style.get("border")
        self.zero_button_border_radius = zero_button_style.get("border radius")

        calibrate_button_style = calibrate_view_style.get("buttons", {}).get("calibrate", {})
        self.calibrate_button_label = calibrate_button_style.get("label")
        self.calibrate_button_active_color = calibrate_button_style.get("active color")
        self.calibrate_button_disabled_color = calibrate_button_style.get("disabled color")
        self.calibrate_button_font = calibrate_button_style.get("font")
        self.calibrate_button_text_color = calibrate_button_style.get("text color")
        self.calibrate_button_text_size = calibrate_button_style.get("text size")
        self.calibrate_button_border = calibrate_button_style.get("border")
        self.calibrate_button_border_radius = calibrate_button_style.get("border radius")
        self.known_weight_style_guide = style_guide.get("known weight view")

        self.serial_thread = serial_thread

        self.units = units

        self.calibration_ongoing = True

        self.number_of_data_points = config_parameters["calibrate data points"]

        self.zero_button_pressed = False

        self.weight_calibration_active = False

         # calls zeroingComplete function when the zeroed_out_tare_complete_signal is emitted by serial_thread
        self.serial_thread.zeroed_out_tare_complete_signal.connect(self.zeroingComplete)

        self.init_UI()

    def init_UI(self):

        self.setWindowTitle(self.window_title)
        self.setStyleSheet(f"background-color: {self.window_color};")

        layout = QVBoxLayout(self)

        label_font = QFont(self.dialog_font, self.dialog_text_size)

        self.dialog_label = QLabel(self.zero_dialog)
        self.dialog_label.setFont(label_font)
        self.dialog_label.setStyleSheet(f"color: {self.dialog_text_color}") 
        layout.addWidget(self.dialog_label)

        buttonLayout = QHBoxLayout()

        self.zero_button = QPushButton(self.zero_button_label)
        self.zero_button.setFont(QFont(self.zero_button_font, self.zero_button_text_size))
        self.zero_button.setStyleSheet(f"""QPushButton {{
                                      background-color: {self.zero_button_active_color};
                                      color: {self.zero_button_text_color}; 
                                      border: {self.zero_button_border}; 
                                      border-radius: {self.zero_button_border_radius}; }}""")
        self.zero_button.clicked.connect(self.on_zero_button_clicked)
        buttonLayout.addWidget(self.zero_button)

        self.calibrate_button = QPushButton(self.calibrate_button_label)
        self.calibrate_button.setFont(QFont(self.calibrate_button_font, self.calibrate_button_text_size))
        self.calibrate_button.setStyleSheet(f"""QPushButton {{
                                      background-color: {self.calibrate_button_disabled_color};
                                      color: {self.calibrate_button_text_color}; 
                                      border: {self.calibrate_button_border}; 
                                      border-radius: {self.calibrate_button_border_radius}; }}""")
        self.calibrate_button.clicked.connect(self.on_calibrate_button_clicked)
        buttonLayout.addWidget(self.calibrate_button)

        layout.addLayout(buttonLayout)

        if not self.auto_size:
            self.resize(self.window_width, self.window_height)

    def on_zero_button_clicked(self):
        if not self.zero_button_pressed:
            self.zero_button_pressed = True
            self.zero_button.setStyleSheet(f"""QPushButton {{
                                background-color: {self.zero_button_disabled_color};
                                color: {self.zero_button_text_color}; 
                                border: {self.zero_button_border}; 
                                border-radius: {self.zero_button_border_radius}; }}""")
            self.serial_thread.zeroed_out_signal.emit()

    def zeroingComplete(self):
        self.weight_calibration_active = True
        self.dialog_label.setText(self.initial_weight_dialog)
        self.calibrate_button.setStyleSheet(f"""QPushButton {{
                                background-color: {self.calibrate_button_active_color};
                                color: {self.calibrate_button_text_color}; 
                                border: {self.calibrate_button_border}; 
                                border-radius: {self.calibrate_button_border_radius}; }}""")

    def on_calibrate_button_clicked(self):
        if (self.weight_calibration_active):
            self.serial_thread.calibrate_capture_signal.emit()
            known_weight_dialog = KnownWeightWindow(self.known_weight_style_guide, self.units, self.serial_thread)
            known_weight_dialog.calibration_abort_change_dialog_signal.connect(self.calibration_abort_confirm)
            if known_weight_dialog.exec_() == QDialog.Accepted:
                if self.calibration_ongoing:
                    self.dialog_label.setText(self.calibrating_dialog)
                    event_loop = QEventLoop()
                    self.serial_thread.calibration_complete_signal.connect(event_loop.quit)
                    self.number_of_data_points -= 1
                    if (self.number_of_data_points == 1):
                        self.dialog_label.setText(self.calibration_complete_dialog)
                        self.calibrate_button.setStyleSheet("QPushButton {background-color: rgb(46,46,46); color: white; border: 2px solid black; border-radius: 10px; }")
                        self.weight_calibration_active = False
                        self.calibration_ongoing = False
                    else:
                        self.dialog_label.setText(self.subsequent_weight_dialog)

    def calibration_abort_confirm(self):
        self.calibration_ongoing = False
        self.dialog_label.setText(self.calibration_aborted_dialog)

    def closeEvent(self, event):
        if self.calibration_ongoing:
            self.serial_thread.calibration_abort_signal.emit()
            super().closeEvent(event)
