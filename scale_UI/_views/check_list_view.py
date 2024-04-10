from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QApplication

checklist_text = """
<p style="font-size: 24px;">Checklist</p>
<ul style="list-style-type: disc;">
    <li style="font-size: 18px; margin-bottom: 10px;">Connect to Wi-Fi.</li>
    <li style="font-size: 18px; margin-bottom: 10px;">Verify that data is uploading to database.</li>
    <li style="font-size: 18px; margin-bottom: 10px;">Connect to arduino serial port.</li>
    <li style="font-size: 18px; margin-bottom: 10px;">Verify that the correct output file is selected in the settings menu.</li>
    <li style="font-size: 18px; margin-bottom: 10px;">Calibrate the scale.</li>
    <!-- Add more items as needed -->
</ul>
"""

class ChecklistWindow(QDialog):
    def __init__(self, style_guide, parent=None):
        super().__init__(parent)

        checklist_style = style_guide.get("checklist", {})
        window_style = checklist_style.get("window", {})
        text_box_style = checklist_style.get("text box", {})

        self.checklist_window_title = window_style.get("title")
        self.checklist_window_color = window_style.get("color")
        self.checklist_window_width = window_style.get("width")
        self.checklist_window_height = window_style.get("height")
        self.checklist_window_offset = window_style.get("offset")
        self.checklist_window_auto_size = window_style.get("auto size")
        self.checklist_window_font = window_style.get("font")
        self.checklist_window_text_color = window_style.get("text color")

        self.checklist_text_box_width = text_box_style.get("width")
        self.checklist_rext_box_height = text_box_style.get("height")

        self.init_UI()

    def init_UI(self):
        self.setWindowTitle(self.checklist_window_title)
        self.setStyleSheet(f"color: {self.checklist_window_text_color}; background-color: {self.checklist_window_color};")

        layout = QVBoxLayout(self)

        checklist_body_text = QTextEdit()
        checklist_body_text.setReadOnly(True)
        checklist_body_text.setStyleSheet("border: none;")
        checklist_body_text.setHtml(checklist_text)
        checklist_body_text.setMinimumSize(self.checklist_text_box_width, self.checklist_rext_box_height)
        layout.addWidget(checklist_body_text)

        layout.addStretch()

        self.setLayout(layout)

        if not self.checklist_window_auto_size:
            self.resize(self.checklist_window_width, self.checklist_window_height)

        desktop = QApplication.desktop()
        desktop_rect = desktop.availableGeometry()
        self.move(desktop_rect.left(), int(desktop_rect.center().y() - self.height() / 2) - self.checklist_window_offset)

        self.show()





