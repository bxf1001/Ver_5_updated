import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QListWidget,QListWidgetItem, QPushButton, QHBoxLayout, QGridLayout, QTextBrowser, QProgressBar
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal , pyqtSlot, QThreadPool,QTimer
import warnings
import uuid
from queue import Queue
from pywinauto import Application
from pywinauto.keyboard import send_keys
import keyboard
from time import sleep
from AppOpener import open as op  # Assuming this is a custom module of yours
import json
from time import sleep

warnings.simplefilter("ignore", UserWarning)


class WorkerSignals(QObject):
    progress = pyqtSignal(int)
    completed = pyqtSignal(str)
    timer_progress = pyqtSignal(int)
    timer_progress_completed = pyqtSignal()


class WhatsApp(QRunnable):
    def __init__(self, number, timer):
        super().__init__()
        self.signals = WorkerSignals()
        self.aborted = False
        self.timer = float(timer) * 60
        self.number = number
        self.uuid = str(uuid.uuid4())
        

    
    @pyqtSlot()
    def run(self):
        
        tasks_list =[self.start_applications_py,
                    self.get_phonenumber,
                    self.get_phonenumber,               
                    self.click_call_button,
                    self.start_recording,
                    self.lock_screen,
                    self.timer_count,  # Start the timer_count function
                    self.click_end_button,
                    self.unlock_screen,
                    self.stop_recording,
                    self.lock_screen ]
        for task in tasks_list:
            if self.aborted:
                break
            task()

            self.signals.completed.emit(self.uuid)
        self.signals.completed.emit(self.uuid)



    @pyqtSlot()
    def abort(self):
        print("Aborted")  # Add this line to print "Aborted"
        self.aborted = True

    def start_applications_py(self):
        sleep(3)
        self.startapp = Application(backend='uia').start(r"cmd.exe /c start shell:appsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App", create_new_console=True, wait_for_idle=False)
        sleep(2)
        self.appwhatsapp = Application(backend='uia').connect(title_re="WhatsApp", timeout=30)
        self.signals.progress.emit(10)

    def get_phonenumber(self):
        sleep(0.25)
        self.url = f"whatsapp://send?phone=+91{self.number}"
        self.subwhatsapp = subprocess.Popen(["cmd", "/C", f"start {self.url}"], shell=True)
        sleep(0.25)
        self.url = f"whatsapp://send?phone=+91{self.number}"
        self.subwhatsapp = subprocess.Popen(["cmd", "/C", f"start {self.url}"], shell=True)
        self.signals.progress.emit(20)
    
    def click_call_button(self):
        while True:
            try:
                self.appwhatsapp.WhatsAppDialog.child_window(title="Video call", auto_id="VideoCallButton", control_type="Button").click()
                break
            except:
                sleep(1)
                continue
        self.signals.progress.emit(30)

    def start_recording(self):
        self.dialog = self.appwhatsapp.window(title="Video call ‎- WhatsApp")
        sleep(2)
        self.dialog.maximize()
        self.button = self.dialog.child_window(title="Add members", auto_id="ParticipantSideBarTriggerButton", control_type="Button")
        self.panel = self.dialog.child_window(title="Device settings", auto_id="MoreButton", control_type="Button").wait('visible', timeout=30, retry_interval=0.5)
        self.panel.set_focus()
        while True:
            send_keys("{TAB}")
            try:
                if self.button.is_enabled():
                    send_keys("{VK_F12}")
                    break
            except:
                sleep(3)
                continue
        self.signals.progress.emit(50)



    def stop_recording(self):
        sleep(1)
        if not self.click_end_button():  # Check if the call was successfully ended
            print("Call could not be ended, attempting emergency shutdown...")
            try:
                subprocess.call("TASKKILL /F /IM WhatsApp.exe", shell=True)
                print("WhatsApp process terminated successfully.")
                sleep(1)
                send_keys("{VK_F12}")
            except Exception as e:
                print("Error:", e)
        else:
            print("Call ended successfully.")
        sleep(1)
        self.signals.progress.emit(100)
        


    def lock_screen(self):
        sleep(1)
        send_keys("^%{VK_NUMPAD0}")

    def unlock_screen(self):
        sleep(1)
        send_keys("^%{VK_NUMPAD0}")


    def click_end_button(self):
        try:
            sleep(2)
            button = self.appwhatsapp.Dialog.child_window(title="End call", auto_id="EndCallButton", control_type="Button")
            if button.exists():  # Check if the button exists before attempting to click it
                button.set_focus()
                button.click()
                sleep(0.5)
                button.click()
                send_keys("{VK_F12}")
                return True  # Return True if the button was clicked successfully
        except Exception as e:
            print("ERROR:", e)
        self.signals.progress.emit(80)
        return False  # Return False if the button could not be clicked




    def timer_count(self):
        count_down = 0
        while count_down < self.timer and not self.aborted:
            if keyboard.is_pressed("space"):
                print("you breaked the process")
                break
            else:
                sleep(1)
                count_down += 1
                progress_percentage = int((count_down / self.timer) * 100)
                self.signals.timer_progress.emit(progress_percentage)  # Emit only progress_percentage
        self.signals.timer_progress_completed.emit()  # Emit signal to indicate timer progress is completed
            

class UserContactApp(QMainWindow):
    work_requested = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("user_data.json", "r") as json_file:
            self.user_data = json.load(json_file)

        self.setWindowTitle("Phone Portal Connect V5")
        self.setGeometry(100, 100, 600, 300)

        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("Enter User ID")
        self.search_button = QPushButton("Search", self)
        self.result_label = QLabel(self)
        self.result_text_browser = QListWidget(self)  #QTextBrowser(self)
        self.result_text_browser.itemDoubleClicked.connect(self.add_contact_from_result)
        self.contact_text_browser = QListWidget(self)   #QTextBrowser(self)
        self.add_button = QPushButton("Add Contact", self)
        self.remove_button = QPushButton("Remove Contact", self)
        self.connect_button = QPushButton("Connect", self)
        self.swap_button = QPushButton("Swap", self)
        self.abort_button = QPushButton("Abort", self)
        self.reset_button = QPushButton("Reset", self)
        self.timer1_input = QLineEdit(self)
        self.timer2_input = QLineEdit(self)
        self.timer3_input = QLineEdit(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("QProgressBar { height: 20px; width: 200px; }")
        self.timer_progress_bar = QProgressBar(self)  # Create new progress bar
        self.timer_progress_bar.setStyleSheet("QProgressBar { height: 20px; width: 200px; }")
        self.timer_progress_bar.setValue(0)  # Set initial value
        self.progress_bar.setValue(0)
        self.timer1_input.setPlaceholderText("Timer 1")
        self.timer2_input.setPlaceholderText("Timer 2")
        self.timer3_input.setPlaceholderText("Timer 3")
        self.timer1_input.setMaxLength(3)
        self.timer2_input.setMaxLength(3)
        self.timer3_input.setMaxLength(3)
        self.timer1_input.setEnabled(False)
        self.timer2_input.setEnabled(False)
        self.timer3_input.setEnabled(False)

        layout = QHBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.user_id_input, 0, 0, 1, 1)
        grid_layout.addWidget(self.search_button, 0, 1)
        grid_layout.addWidget(self.result_label, 1, 0, 1, 3)
        grid_layout.addWidget(self.result_text_browser, 2, 0, 1, 3)
        grid_layout.addWidget(self.contact_text_browser, 3, 0, 1, 3)
        grid_layout.addWidget(self.add_button, 5, 0)
        grid_layout.addWidget(self.remove_button, 5, 1)
        grid_layout.addWidget(self.reset_button, 5, 2)
        grid_layout.addWidget(self.connect_button, 6, 0)
        grid_layout.addWidget(self.swap_button, 6, 1)
        grid_layout.addWidget(self.abort_button, 6, 2)
        grid_layout.addWidget(self.timer1_input, 4, 0)
        grid_layout.addWidget(self.timer2_input, 4, 1)
        grid_layout.addWidget(self.timer3_input, 4, 2)
        grid_layout.addWidget(self.progress_bar, 7, 0,1,3)
        grid_layout.addWidget(self.timer_progress_bar,8,0,1,3)
        layout.addLayout(grid_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.search_button.clicked.connect(self.search_user)
        self.add_button.clicked.connect(self.add_contact)
        self.remove_button.clicked.connect(self.remove_contact)
        self.connect_button.clicked.connect(self.connect_function)
        self.swap_button.clicked.connect(self.swap_contacts)
        self.abort_button.clicked.connect(self.abort_function)
        self.reset_button.clicked.connect(self.reset_function)
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(10)
        self.worker_progress = {}
        self.selected_contacts = []
        self.worker_queue = Queue()

    def search_user(self):
        user_id = self.user_id_input.text()
        if user_id in self.user_data:
            user_info = self.user_data[user_id]
            name = user_info.get("name", "")
            contacts = [user_info.get("1", ""), user_info.get("2", ""), user_info.get("3", "")]
            self.result_label.setText(f"Name: {name}")
            self.result_text_browser.clear()
            for contact in contacts:
                if contact:
                    self.result_text_browser.addItem(contact)  # Use addItem instead of append
        else:
            self.result_label.setText("User not found.")
            self.result_text_browser.clear()

    def add_contact(self):
        selected_contact = self.result_text_browser.currentItem().text()
        if selected_contact:
            self.selected_contacts.append(selected_contact)
            self.update_contact_text_browser()

            if len(self.selected_contacts) == 1:
                self.timer1_input.setEnabled(True)
            elif len(self.selected_contacts) == 2:
                self.timer2_input.setEnabled(True)
            elif len(self.selected_contacts) == 3:
                self.timer3_input.setEnabled(True)
        
    def add_contact_from_result(self, item):
        # Get the text of the double-clicked item
        contact = item.text()
        
        # Add the contact to the contact text browser
        self.selected_contacts.append(contact)
        self.update_contact_text_browser()
        
        # Enable timer inputs as needed
        if len(self.selected_contacts) == 1:
            self.timer1_input.setEnabled(True)
        elif len(self.selected_contacts) == 2:
            self.timer2_input.setEnabled(True)
        elif len(self.selected_contacts) == 3:
            self.timer3_input.setEnabled(True)

    def remove_contact(self):
        selected_contact = self.contact_text_browser.selectedItems()
        if selected_contact:
            for item in selected_contact:
                row = self.contact_text_browser.row(item)
                self.contact_text_browser.takeItem(row)
                del self.selected_contacts[row]

            # Update the input fields
            if len(self.selected_contacts) < 1:
                self.timer1_input.setEnabled(False)
            if len(self.selected_contacts) < 2:
                self.timer2_input.setEnabled(False)
            if len(self.selected_contacts) < 3:
                self.timer3_input.setEnabled(False)


    def swap_contacts(self):
        if len(self.selected_contacts) >= 2:
            self.selected_contacts[0], self.selected_contacts[1] = self.selected_contacts[1], self.selected_contacts[0]
            self.timer1_input.text, self.timer2_input.text = self.timer2_input.text, self.timer1_input.text
            self.update_contact_text_browser()
        elif len(self.selected_contacts) >= 3:
            self.selected_contacts[0], self.selected_contacts[1], self.selected_contacts[2] = self.selected_contacts[2], self.selected_contacts[1], self.selected_contacts[0]
            self.update_contact_text_browser()

    def update_contact_text_browser(self):
        self.contact_text_browser.clear()
        for contact in self.selected_contacts:
            item = QListWidgetItem(contact)
            self.contact_text_browser.addItem(item)

    def connect_function(self):
        self.connect_button.setEnabled(False)
        timer1 = self.timer1_input.text()
        timer2 = self.timer2_input.text()   
        timer3 = self.timer3_input.text()
        self.progress_bar.setValue(0)  # Reset progress bar
        self.timer_progress_bar.setValue(0)  # Reset timer progress bar
        self.progress_bar.setMaximum(100)
        self.timer_progress_bar.setMaximum(100)  # Set maximum value for timer progress bar

        self.start_workers(self.selected_contacts, [timer1, timer2, timer3])

    def start_workers(self, contacts, timers):
        # Clear any existing workers from the queue
        while not self.worker_queue.empty():
            self.worker_queue.get()

        # Create workers and add them to the queue
        for contact, timer_input in zip(contacts, timers):
            worker = WhatsApp(contact, timer_input)
            worker.signals.progress.connect(self.progress_bar.setValue)
            worker.signals.completed.connect(lambda uuid=worker.uuid: self.worker_completed(uuid)) # Pass the UUID to the lambda function
            worker.signals.timer_progress.connect(self.timer_progress_bar.setValue)  # Connect timer progress
            # Assuming `self.timer_progress_completed` is the signal connected to `cleanup`
            worker.signals.timer_progress_completed.connect(lambda uuid=worker.uuid: self.cleanup(uuid))
            self.worker_queue.put(worker)

        # Start the first worker
        self.start_next_worker()

    def start_next_worker(self):
        if not self.worker_queue.empty():
            worker = self.worker_queue.get()
            self.thread_pool.start(worker)
        else:
            # All workers have been started
            pass

    def cleanup(self, uuid):
        if uuid in self.worker_progress:
            del self.worker_progress[uuid]
            total_workers = len(self.worker_progress)
            self.refresh_progress(total_workers)

    def refresh_progress(self, total_workers):
        if total_workers > 0:
            progress = sum(self.worker_progress.values()) / total_workers
            self.progress_bar.setValue(progress)
        else:
            self.progress_bar.setValue(0)


    @pyqtSlot()
    def worker_completed(self):
        self.connect_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.timer_progress_bar.setValue(0)
        self.start_next_worker()  # Start the next worker in the queue

    def abort_function(self):
        for worker in self.worker_progress:
            worker.abort()
        

    def reset_function(self):
        self.user_id_input.clear()
        self.result_label.clear()
        self.result_text_browser.clear()
        self.contact_text_browser.clear()
        self.selected_contacts.clear()
        self.timer1_input.clear()
        self.timer2_input.clear()
        self.timer3_input.clear()
        self.timer1_input.setEnabled(False)
        self.timer2_input.setEnabled(False)
        self.timer3_input.setEnabled(False)
        self.progress_bar.setValue(0)
        self.timer_progress_bar.setValue(0)
        self.connect_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserContactApp()
    window.show()
    sys.exit(app.exec_())