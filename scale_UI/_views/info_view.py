from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

info_text = """
<p style="font-size: 24px;">Welcome to <b>ScoutScale</b></p>
<p style="font-size: 32px;"><b>This window is under development.<b></p>
"""


class InfoWindow(QDialog):
    def __init__(self, style_guide, config_paramters, parent=None):
        super().__init__(parent)

        info_view_style = style_guide.get("info view", {})
        window_style = info_view_style.get("window", {})
        header_style = info_view_style.get("header", {})
        image_styles = header_style.get("images", {})


        self.info_window_title = window_style.get("title")
        self.info_window_color = window_style.get("color")
        self.info_window_width = window_style.get("width")
        self.info_window_height = window_style.get("height")
        self.info_window_auto_size = window_style.get("auto size")
        self.info_window_font = window_style.get("font")
        self.info_window_text_color = window_style.get("text color")


        self.info_header_title = header_style.get("title")
        self.info_header_font = header_style.get("font")
        self.info_header_text_size = header_style.get("text size")
        self.info_header_text_color = header_style.get("text color")


        self.scoutscale_icon_location = image_styles.get("ScoutScale icon", {}).get("location")
        self.scoutscale_icon_width = image_styles.get("ScoutScale icon", {}).get("width")
        self.scoutscale_icon_height = image_styles.get("ScoutScale icon", {}).get("height")
        self.dev_team_icon_location = image_styles.get("dev team icon", {}).get("location")
        self.dev_team_icon_width = image_styles.get("dev team icon", {}).get("width")
        self.dev_team_icon_height = image_styles.get("dev team icon", {}).get("height") 


        self.init_UI()

    def init_UI(self):

        self.setWindowTitle(self.info_window_title)
        self.setStyleSheet(f"color: {self.info_window_text_color}; background-color: {self.info_window_color};")

        layout = QVBoxLayout(self)
        row1 = QHBoxLayout()

        ss_image_Label = QLabel()
        pixmap = QPixmap(self.scoutscale_icon_location).scaled(self.scoutscale_icon_width, self.scoutscale_icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ss_image_Label.setPixmap(pixmap)
        row1.addWidget(ss_image_Label)
        row1.addStretch()

        scout_scale_font = QFont(self.info_header_font, self.info_header_text_size)
        scout_scale_font.setWeight(QFont.Bold)
        title = QLabel(self.info_header_title)
        title.setFont(scout_scale_font)
        title.setStyleSheet(f"color: {self.info_header_text_color};") 
        row1.addWidget(title)

        row1.addStretch()

        temp_group_name_image_Label = QLabel()
        pixmap = QPixmap(self.dev_team_icon_location).scaled(self.dev_team_icon_width, self.dev_team_icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        temp_group_name_image_Label.setPixmap(pixmap)
        row1.addWidget(temp_group_name_image_Label)
        
        layout.addLayout(row1)

        info_body_text = QTextEdit()
        info_body_text.setReadOnly(True)
        info_body_text.setStyleSheet("border: none;")
        info_body_text.setHtml(info_text)

        layout.addWidget(info_body_text)

        layout.addStretch()

        self.setLayout(layout)

        if not self.info_window_auto_size:
            self.resize(self.info_window_width, self.info_window_height)
    
