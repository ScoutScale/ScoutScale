from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

import os

info_text = """
<p style="font-size: 24px;">Welcome to <b>ScoutScale</b></p>
<p style="font-size: 16px;">a one-of-a-kind, digital food-weighing scale crafted to support The Boy Scouts of America in their mission to maximize the donated food through their Scouting For Food program. </p>
<p style="font-size: 24px;"><b>Main Menu Buttons<b></p>
<p style="font-size: 16px;">Capture Output - Used to capture the current weight of items on the scale.</p>
<p style="font-size: 16px;">Tare Scale - Used to zero out the scale.</p>
<p style="font-size: 16px;">Calibrate Scale - Used to calibrate the scale to output the correct unit values.</p>
<p style="font-size: 16px;">☰ - Toggles the side menu.</p>
<p style="font-size: 24px;"><b>Side Menu Buttons<b></p>
<p style="font-size: 16px;">⚙ - Settings Menu</p>
<p style="font-size: 16px;">☑ - Toggle Checklist</p>
<p style="font-size: 16px;">⌫ - Delete Previous Entry</p>
<p style="font-size: 16px;">🐞 - Toggle Debugging Mode</p>
<p style="font-size: 16px;">ⓧ - Exit Program</p>
<p style="font-size: 16px;">
<p style="font-size: 24px;"><b>Additional Info<b></p>
Please note that additional operational information can be found in the users manual hosted in the ScoutScale GitHub repository. 
</p>
<p>GitHub Repository:<br>
    <a href="https://github.com/tsallwasser/ScoutScale/tree/master">https://github.com/tsallwasser/ScoutScale/tree/master</a>
</p>
"""


class InfoWindow(QDialog):
    def __init__(self, style_guide, parent=None):
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
        self.info_txt_box_width = window_style.get("desc width")
        self.info_txt_box_height = window_style.get("desc height")


        self.info_header_title = header_style.get("title")
        self.info_header_font = header_style.get("font")
        self.info_header_text_size = header_style.get("text size")
        self.info_header_text_color = header_style.get("text color")


        self.scoutscale_icon_location = os.path.dirname(__file__) + "/../" + image_styles.get("ScoutScale icon", {}).get("location")
        self.scoutscale_icon_width = image_styles.get("ScoutScale icon", {}).get("width")
        self.scoutscale_icon_height = image_styles.get("ScoutScale icon", {}).get("height")
        self.dev_team_icon_location = os.path.dirname(__file__) + "/../" + image_styles.get("dev team icon", {}).get("location")
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
        info_body_text.setFixedSize(self.info_txt_box_width, self.info_txt_box_height)

        layout.addWidget(info_body_text)

        layout.addStretch()

        self.setLayout(layout)

        if not self.info_window_auto_size:
            self.resize(self.info_window_width, self.info_window_height)
    
