import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QSound


class EyeProtectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("20-20-20 Eye Protection App")

        self.timer_label = QLabel("Time left: 20:00", self)
        self.timer_label.setGeometry(50, 20, 200, 30)

        self.duration_label = QLabel("Timer duration (minutes):", self)
        self.duration_label.setGeometry(50, 60, 200, 30)

        self.duration_combo = QComboBox(self)
        self.duration_combo.setGeometry(230, 60, 60, 30)
        self.duration_combo.addItems(["1", "5", "10", "15", "20", "25", "30"])  # Options for timer duration

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(50, 100, 100, 30)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(180, 100, 100, 30)
        self.stop_button.clicked.connect(self.stop_timer)

        self.seconds_left = 20 * 60  # 20 minutes initially
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.alert_sound = QSound("alert_sound.wav")

        self.break_timer = QTimer(self)
        print("here i come")
        self.break_timer.timeout.connect(self.start_timer)

    def start_timer(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer_duration = int(self.duration_combo.currentText()) * 60  # Convert minutes to seconds
        self.seconds_left = self.timer_duration
        self.update_timer()
        self.timer.start(1000)  # Timer interval: 1 second

    def stop_timer(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.timer.stop()
        self.break_timer.stop()

    def update_timer(self):
        minutes = self.seconds_left // 60
        seconds = self.seconds_left % 60
        self.timer_label.setText(f"Time left: {minutes:02}:{seconds:02}")
        if self.seconds_left > 0:
            self.seconds_left -= 1
        else:
            self.timer.stop()
            print("Playing alert sound...")
            self.alert_sound.play()
            self.seconds_left = 20  # Reset for break duration (20 seconds)
            print("seconds left neew")
            self.break_timer.start(1000)  # Start break timer


    def start_break_timer(self):
        self.timer_label.setText("Take a 20-second break!")
        self.break_timer.stop()
        self.start_button.setEnabled(True)
        self.break_timer.start(1000)  # Start break timer



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EyeProtectionApp()
    window.setGeometry(100, 100, 350, 150)
    window.show()
    sys.exit(app.exec_())
