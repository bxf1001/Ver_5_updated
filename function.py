import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QListWidget,QListWidgetItem, QPushButton, QHBoxLayout, QGridLayout, QProgressBar
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QThread, QObject, pyqtSignal
from time import sleep
import json
import subprocess
from pywinauto import Application
from pywinauto.keyboard import send_keys
import warnings

warnings.simplefilter("ignore", UserWarning)

class WhatsApp(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.aborted = False

    def precheck_events(self):
        # Your implementation here
        pass

    def postcheck_events(self):
        # Your implementation here
        pass

    def abort(self):
        self.aborted = True

    def run_whatsapp_process(self, contacts, timers):
        for contact, timer_input in zip(contacts, timers):
            self.grab_contact(contact)
            self.precheck_events()
            self.start_timer(timer_input)
            self.postcheck_events()
        self.finished.emit()

    def grab_contact(self, number):
        # Your implementation here
        pass

    def start_timer(self, minutes):
        seconds = minutes * 60
        for remaining_time in range(seconds, -1, -1):
            sleep(1)

class PhonePortal(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your initialization code here

        self.thread = QThread()
        self.worker = WhatsApp()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_whatsapp_process)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)

    def start_process(self, contacts, timers):
        self.thread.start()
        self.thread.contacts = contacts
        self.thread.timers = timers

    # Other methods here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhonePortal()
    window.show()
    sys.exit(app.exec())
