from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

info_text = """
<p style="font-size: 24px;">Welcome to <b>ScoutScale</b></p>
<p style="font-size: 32px;"><b>This window is under development.<b></p>
"""


class InfoWindow(QDialog):
    def __init__(self, config_paramters, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ScoutScale Information View")
        self.resize(400, 300)
        self.setStyleSheet("color: black; background-color: rgb(254,248,234);") 

        self.team_logo_location = config_paramters["team logo"]
        self.ss_logo_location = config_paramters["ScoutScale logo"]

        self.init_UI()

    def init_UI(self):
        layout = QVBoxLayout(self)

        font = QFont()
        font.setWeight(QFont.Bold)
        font.setPointSize(20)

        row1 = QHBoxLayout()

        ss_image_Label = QLabel()
        pixmap = QPixmap(self.ss_logo_location).scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ss_image_Label.setPixmap(pixmap)

        row1.addWidget(ss_image_Label)

        row1.addStretch()

        scout_scale_font = QFont("Gill Sans", 56)
        scout_scale_font.setWeight(QFont.Bold)
        title = QLabel("ScoutScale")
        title.setFont(scout_scale_font)
        title.setStyleSheet("color: black;") 
        row1.addWidget(title)

        row1.addStretch()

        temp_group_name_image_Label = QLabel()
        pixmap = QPixmap(self.team_logo_location).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        temp_group_name_image_Label.setPixmap(pixmap)
        row1.addWidget(temp_group_name_image_Label)
        
        layout.addLayout(row1)

        info_body_text = QTextEdit()
        info_body_text.setReadOnly(True)
        info_body_text.setStyleSheet("font-size: 14px; border: none;")
        info_body_text.setHtml(info_text)

        layout.addWidget(info_body_text)

        layout.addStretch()

        self.setLayout(layout)

        self.resize(700, 700)
    
