from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import qrcode
import io

class QRCodeWindow(QDialog):
    def __init__(self, style_guide, website_url, parent=None):
        super().__init__(parent)
        self.website_url = website_url

        self.window_title = style_guide["qr code view"]["window"]["title"]
        self.window_color = style_guide["qr code view"]["window"]["color"]

        self.init_UI()

    def init_UI(self):
        self.setWindowTitle(self.window_title)
        self.setStyleSheet(f"background-color: {self.window_color};")
        
        window_size = self.size()

        max_qr_size = min(window_size.width(), window_size.height())
        box_size = max_qr_size // 25 
        
        qr_image = self.generate_qr_code_image(box_size)
        qr_label = QLabel()
        qr_label.setPixmap(qr_image)
        qr_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(qr_label)
        self.setLayout(layout)

    def generate_qr_code_image(self, box_size):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=4,
        )
        qr.add_data(self.website_url)
        qr.make(fit=True)
        img = qr.make_image()
        qr_image = self.qr_image_to_qpixmap(img)
        return qr_image

    def qr_image_to_qpixmap(self, img):
        img_bytes = io.BytesIO()
        img.save(img_bytes)
        return QPixmap.fromImage(QImage.fromData(img_bytes.getvalue()))
