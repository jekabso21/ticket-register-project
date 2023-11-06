import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from pyzbar.pyzbar import decode

class QRCodeScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Code Scanner")
        self.setGeometry(100, 100, 640, 480)

        self.video_frame = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_frame)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print(f"QR Code Data: {data}")
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_frame.setPixmap(pixmap)

    def closeEvent(self, event):
        self.camera.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = QRCodeScannerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
