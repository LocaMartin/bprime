import sys
import time
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QFontDatabase, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QPoint

class DigitalStopwatch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Stopwatch")
        self.setFixedSize(500, 300)

        # Frameless transparent window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0.0
        self.oldPos = None
        self.last_display = ""

        self.load_font()
        self.init_ui()

    def get_font_path(self):
        """Return the correct font path if it exists."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_path, "..", "digi7", "digital-7.ttf")

        if os.path.exists(font_path):
            print(f"Found font at: {font_path}")
            return font_path

        print(f"Font file not found at: {font_path}")
        return ""

    def load_font(self):
        """Load Digital-7 font if available, otherwise use fallback."""
        font_path = self.get_font_path()

        if font_path and os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                self.digital_font = QFont(font_family, 48)
                print(f"Loaded Digital-7 font: {font_family}")
                return

        print("Using fallback font (Courier)")
        self.digital_font = QFont("Courier", 48)
        self.digital_font.setBold(True)

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)

        central_widget.setStyleSheet("""
            QWidget#centralWidget {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 15px;
            }
        """)

        self.time_label = QLabel("00:00:00.00")
        self.time_label.setFont(self.digital_font)
        self.time_label.setAlignment(Qt.AlignCenter)

        palette = self.time_label.palette()
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        self.time_label.setPalette(palette)

        main_layout.addWidget(self.time_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(100, 40)
        self.start_button.setStyleSheet(
            "QPushButton { background-color: rgba(46, 125, 50, 200); color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: rgba(56, 142, 60, 200); }"
        )
        self.start_button.clicked.connect(self.toggle_start_stop)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setFixedSize(100, 40)
        self.pause_button.setStyleSheet(
            "QPushButton { background-color: rgba(21, 101, 192, 200); color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: rgba(25, 118, 210, 200); }"
            "QPushButton:disabled { background-color: rgba(144, 164, 174, 100); }"
        )
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.pause)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedSize(100, 40)
        self.reset_button.setStyleSheet(
            "QPushButton { background-color: rgba(198, 40, 40, 200); color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: rgba(211, 47, 47, 200); }"
        )
        self.reset_button.clicked.connect(self.reset)

        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 30); color: white; border-radius: 15px; }"
            "QPushButton:hover { background-color: rgba(255, 0, 0, 200); }"
        )
        self.close_button.clicked.connect(self.close)

        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(self.close_button)
        main_layout.addLayout(close_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.setInterval(50)  # ✅ optimized to reduce jitter

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def toggle_start_stop(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_button.setText("Stop")
            self.pause_button.setEnabled(True)
            self.timer.start()
        else:
            self.running = False
            self.start_button.setText("Start")
            self.pause_button.setEnabled(False)
            self.timer.stop()

    def pause(self):
        if self.running:
            self.running = False
            self.start_button.setText("Start")
            self.pause_button.setEnabled(False)
            self.timer.stop()

    def reset(self):
        self.running = False
        self.elapsed_time = 0.0
        self.start_button.setText("Start")
        self.pause_button.setEnabled(False)
        self.timer.stop()
        self.update_display()

    def update_display(self):
        if self.running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time

        total_seconds = self.elapsed_time
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        hundredths = int((total_seconds - int(total_seconds)) * 100)

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{hundredths:02d}"

        # ✅ Only update label if value changed
        if time_str != self.last_display:
            self.time_label.setText(time_str)
            self.last_display = time_str

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    stopwatch = DigitalStopwatch()
    stopwatch.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
