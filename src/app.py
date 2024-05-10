import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound


class EyeProtectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("20-20-20 Eye Protection App")

        self.MAIN_TIMER = True

        self.timer_label = QLabel("Time left: 20:00", self)
        self.timer_label.setGeometry(50, 20, 200, 30)

        self.duration_label = QLabel("Timer duration (minutes):", self)
        self.duration_label.setGeometry(50, 60, 200, 30)

        self.duration_combo = QComboBox(self)
        self.duration_combo.setGeometry(230, 60, 60, 30)
        self.duration_combo.addItems(["10", "15", "20", "25", "30"])  # Options for timer duration

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(50, 100, 100, 30)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(180, 100, 100, 30)
        self.stop_button.clicked.connect(self.stop_continue_timer)
        self.stop_button.setEnabled(False)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setGeometry(310, 100, 100, 30)
        self.reset_button.clicked.connect(self.reset_timer)

        self.seconds_left = 20 * 60  # 20 minutes initially
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.alert_sound = QSound("alert_sound.wav")
        self.alert_out = QSound("alert_out.wav")


    def start_timer(self):
        print("----Started Another Timer----")
        self.start_button.setEnabled(False)
        self.MAIN_TIMER = True
        self.stop_button.setEnabled(True)
        self.reset_button.setEnabled(False)  # Disable reset button during timer operation
        self.timer_duration = int(self.duration_combo.currentText()) * 60  # Convert minutes to seconds
        self.seconds_left = self.timer_duration
        self.update_timer()
        self.timer.start(1000)  # Timer interval: 1 second


    def stop_continue_timer(self):
        if self.timer.isActive():
            self.stop_button.setText("Continue")
            self.timer.stop()
            #self.break_timer.stop()
            self.reset_button.setEnabled(True)  # Enable reset button when timer is stopped
        else:
            self.stop_button.setText("Stop")
            self.update_timer()
            self.timer.start(1000)


    def reset_timer(self):
        self.timer_label.setText("Time left: 00:00")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.timer.stop()
        #self.timer.stop()
        self.stop_button.setText("Stop")  # Set the text of stop_button to "Stop"


    def update_timer(self):
        minutes = self.seconds_left // 60
        seconds = self.seconds_left % 60
        self.timer_label.setText(f"Time left: {minutes:02}:{seconds:02}")
        if self.seconds_left > 0:
            self.seconds_left -= 1
        else:
            self.timer.stop()
            if self.MAIN_TIMER:
                print(f"Alert sound with main timer {self.MAIN_TIMER}")
                self.alert_sound.play()
                self.MAIN_TIMER = False
                self.seconds_left = 20
                self.timer.start(1000)
            else:
                print(f"Alert out with main timer {self.MAIN_TIMER}")
                self.alert_out.play()
                #self.timer.start(1000)
                self.start_timer()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EyeProtectionApp()
    window.setGeometry(100, 100, 450, 150)
    window.show()
    sys.exit(app.exec_())
