import sys
import requests
from io import BytesIO
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import pytz

COUNTRIES = {
    "Manila, Philippines": {"timezone": "Asia/Manila", "code": "ph"},
    "Honolulu, HI, USA": {"timezone": "Pacific/Honolulu", "code": "us"},
    "New Delhi, India": {"timezone": "Asia/Kolkata", "code": "in"},
    "London, UK": {"timezone": "Europe/London", "code": "gb"},
    "Tokyo, Japan": {"timezone": "Asia/Tokyo", "code": "jp"},
}

class TimeZoneApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Zone Converter (No Tk)")
        self.setGeometry(300, 300, 500, 400)

        self.base_selector = QComboBox()
        self.base_selector.addItems(COUNTRIES.keys())
        self.base_selector.currentIndexChanged.connect(self.update_times)

        self.labels = {}
        self.flag_labels = {}

        layout = QVBoxLayout()
        base_layout = QHBoxLayout()
        base_layout.addWidget(QLabel("Base Location:"))
        base_layout.addWidget(self.base_selector)
        layout.addLayout(base_layout)

        for city in COUNTRIES:
            hbox = QHBoxLayout()

            flag = QLabel()
            flag.setFixedWidth(40)
            self.flag_labels[city] = flag
            self.load_flag(flag, COUNTRIES[city]["code"])

            name_label = QLabel(city)
            name_label.setFixedWidth(150)

            time_label = QLabel("")
            self.labels[city] = time_label

            hbox.addWidget(flag)
            hbox.addWidget(name_label)
            hbox.addWidget(time_label)
            layout.addLayout(hbox)

        self.setLayout(layout)
        self.update_times()

        # refresh every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_times)
        self.timer.start(1000)

    def load_flag(self, label, code):
        try:
            url = f"https://flagcdn.com/w40/{code}.png"
            resp = requests.get(url)
            pixmap = QPixmap()
            pixmap.loadFromData(resp.content)
            label.setPixmap(pixmap)
        except:
            label.setText("🏳️")

    def update_times(self):
        base_city = self.base_selector.currentText()
        if not base_city:
            return

        base_tz = pytz.timezone(COUNTRIES[base_city]["timezone"])
        base_now = datetime.now(base_tz)

        for city, info in COUNTRIES.items():
            tz = pytz.timezone(info["timezone"])
            local_time = base_now.astimezone(tz).strftime('%a, %b %d — %I:%M %p')
            self.labels[city].setText(local_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeZoneApp()
    window.show()
    sys.exit(app.exec_())