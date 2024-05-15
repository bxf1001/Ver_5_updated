import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QListWidget,QListWidgetItem, QPushButton, QHBoxLayout, QGridLayout, QProgressBar
import warnings
import uuid
from queue import Queue
from pywinauto import Application
from pywinauto.keyboard import send_keys
import keyboard
from add_user import AddUser
from qt_material import apply_stylesheet
from time import sleep
import json
from PyQt5.QtCore import QRunnable, pyqtSignal, pyqtSlot, QThreadPool,QObject
from queue import Queue

warnings.simplefilter("ignore", UserWarning)
class WorkerSignals(QObject): # Create a class to hold the

    progress = pyqtSignal(int) # Create a progress signal with an additional string parameter
    finished = pyqtSignal(int) # Create a finished signal

class WhatsApp(QRunnable): # Inherit from QRunnable 


    def __init__(self, number, timer): # Add the timer parameter and contact parameter
        super().__init__()
        self.setAutoDelete(True) # Automatically delete the thread when it finishes
        self.timer = float(timer) * 60 # Convert the timer to seconds
        self.number = number  
        self.aborted = False       # Store the contact number
        self.uuid = uuid.uuid4().hex          # Generate a unique identifier for the worker
        self.signals = WorkerSignals() # Create an instance of the WorkerSignals class
        
    @pyqtSlot(int)        
    def run(self):          # Override the run method
        tasks_list = [self._precheck_events, self._postcheck_events] # Create a list of tasks
        for task in tasks_list:
            task()
            if self.aborted:
                break

    def abort(self): # Add an abort method to stop the worker
        self.aborted = True

    def _precheck_events(self):
        self.start_applications() # Start the applications
        self.get_phonenumber()  # Get the phone number  
        #self.click_call_button()   # Click the call button
        #self.start_recording() # Start the recording
        self.lock_screen() # Lock the screen

    def _postcheck_events(self):
        self.timer_count()  # Start the timer_count function
        self.click_end_button() # Click the end button
        sleep(1)
        self.unlock_screen() # Unlock the screen
        sleep(1)
        self.stop_recording() # Stop the recording
        sleep(1)
        self.lock_screen()  # Lock the screen
        self.signals.finished.emit(self.uuid)


    def start_applications(self): # Start the applications whatsapp using pywinauto
        sleep(3)
        self.startapp = Application(backend='uia').start(r"cmd.exe /c start shell:appsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App", create_new_console=True, wait_for_idle=False)
        sleep(2)
        self.appwhatsapp = Application(backend='uia').connect(title_re="WhatsApp", timeout=30)

    def get_phonenumber(self):  # Get the phone number from the user and open the whatsapp chat window
        sleep(0.25)
        self.url = f"whatsapp://send?phone=+91{self.number}"
        self.subwhatsapp = subprocess.Popen(["cmd", "/C", f"start {self.url}"], shell=True)
        sleep(0.25)
        self.url = f"whatsapp://send?phone=+91{self.number}"
        self.subwhatsapp = subprocess.Popen(["cmd", "/C", f"start {self.url}"], shell=True)

    def click_call_button(self): # Click the call button in the WhatsApp chat window
        while True: # Loop until the call button is clicked
            try:
                self.appwhatsapp.WhatsAppDialog.child_window(title="Video call", auto_id="VideoCallButton", control_type="Button").click()
                break
            except:
                sleep(1)
                continue


    def start_recording(self): # Start the recording of the video call once the call is connected
        self.dialog = self.appwhatsapp.window(title="Video call ‎- WhatsApp")
        sleep(2)
        try:
            self.dialog.maximize()
        except:
            pass
        self.button = self.dialog.child_window(title="Add members", auto_id="ParticipantSideBarTriggerButton", control_type="Button")
        self.panel = self.dialog.child_window(title="Device settings", auto_id="MoreButton", control_type="Button").wait('visible', timeout=30, retry_interval=0.5)
        self.panel.set_focus()
        while True: # Loop until the button is enabled
            send_keys("{TAB}") # Press the TAB key to focus the button
            try:
                if self.button.is_enabled():
                    send_keys("{VK_F12}")   # Press the F12 key to start recording
                    break
            except:
                sleep(3)
                continue


    def lock_screen(self): # Lock the screen to prevent any interruptions
        sleep(1)
        send_keys("^%{VK_NUMPAD0}")


    def click_end_button(self): # Click the end call button to end the call
        try:
            sleep(2)
            button = self.appwhatsapp.Dialog.child_window(title="End call", auto_id="EndCallButton", control_type="Button")
            if button.exists():  # Check if the button exists before attempting to click it
                button.set_focus()
                sleep(0.5)
                button.click()
                send_keys("{VK_F12}")
                return True  # Return True if the button was clicked successfully
        except Exception as e:
            print("ERROR:", e)
        return False  # Return False if the button could not be clicked
    
    def unlock_screen(self): # Unlock the screen after the call has ended
        sleep(1)
        send_keys("^%{VK_NUMPAD0}")


    def stop_recording(self): # terminate whatsapp if the end button is not clicked
        sleep(1)
        if not self.click_end_button():  # Check if the call was successfully ended
            print("Call could not be ended, attempting emergency shutdown...")
            try:
                subprocess.call("TASKKILL /F /IM WhatsApp.exe", shell=True) # Terminate the WhatsApp process
                print("WhatsApp process terminated successfully.")
                sleep(1)
                send_keys("{VK_F12}")  # Press the F12 key to stop recording
            except Exception as e:
                print("Error:", e)
        else:
            print("Call ended successfully.")
        sleep(1)

    def timer_count(self): # Timer function to count down the call duration
        count_down = 0
        while count_down < self.timer : 
            if keyboard.is_pressed("space"):
                print("you breaked the process")
                break
            else:
                sleep(1)
                count_down += 1
                progress_percentage = int((count_down / self.timer) * 100) # Calculate the progress percentage 
                self.signals.progress.emit(progress_percentage) # Emit the progress signal with uuid parameter
            self.signals.finished.emit(self.uuid)
   

class PhonePortal(QMainWindow): # Inherit from QMainWindow

    def __init__(self, *args, **kwargs): # Add *args and **kwargs
        super().__init__(*args, **kwargs) # Pass *args and **kwargs to the super class 

        self.setWindowTitle("Phone Portal Connect V5") # Set the window title
        self.setGeometry(100, 100, 600, 300)

        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("Enter User ID")
        self.search_button = QPushButton("Search", self)
        self.result_label = QLabel(self)
        self.result_text_browser = QListWidget(self)  # Three Contacts load from user_data.json
        self.result_text_browser.itemDoubleClicked.connect(self.add_contact_from_result)
        self.contact_text_browser = QListWidget(self)    # Selected contacts will be displayed here
        self.add_button = QPushButton("Add Contact", self) # Add selected contact to the contact_text_browser
        self.btn_add_user = QPushButton('Add User', self) # Add User button
        self.remove_button = QPushButton("Remove Contact", self) # Remove selected contact from the contact_text_browser
        self.connect_button = QPushButton("Connect", self) # Connect button
        self.swap_button = QPushButton("Swap", self) # Swap button to swap the selected contacts
        self.abort_button = QPushButton("Abort", self) # Abort button to abort the current operation
        self.reset_button = QPushButton("Reset", self)  # Reset button to reset the UI elements
        self.timer1_input = QLineEdit(self) # Timer input fields
        self.timer2_input = QLineEdit(self) # Timer input fields
        self.timer3_input = QLineEdit(self) # Timer input fields
        self.progress_bar = QProgressBar(self) # Create new progress bar
        self.progress_bar.setStyleSheet("QProgressBar { height: 20px; width: 200px; }")
        self.progress_bar.setValue(0) # Set the initial value of the progress bar to 0 
        self.progress_bar.setValue(0) # Set the initial value of the progress bar to 0
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
        grid_layout.addWidget(self.swap_button, 6, 1)
        grid_layout.addWidget(self.btn_add_user,0,2)
        grid_layout.addWidget(self.search_button, 0, 1)
        grid_layout.addWidget(self.result_label, 1, 0, 1, 3)
        grid_layout.addWidget(self.result_text_browser, 2, 0, 1, 3)
        grid_layout.addWidget(self.contact_text_browser, 3, 0, 1, 3)
        grid_layout.addWidget(self.add_button, 5, 0)
        grid_layout.addWidget(self.remove_button, 5, 1)
        grid_layout.addWidget(self.reset_button, 5, 2)
        grid_layout.addWidget(self.connect_button, 6, 0)
        grid_layout.addWidget(self.abort_button, 6, 2)
        grid_layout.addWidget(self.timer1_input, 4, 0)
        grid_layout.addWidget(self.timer2_input, 4, 1)
        grid_layout.addWidget(self.timer3_input, 4, 2)
        grid_layout.addWidget(self.progress_bar, 7, 0,1,3)
        layout.addLayout(grid_layout)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.search_button.clicked.connect(self.search_user) # Connect the search button to the search_user function
        self.add_button.clicked.connect(self.add_contact) # Connect the add button to the add_contact function 
        self.remove_button.clicked.connect(self.remove_contact) # Connect the remove button to the remove_contact function
        self.connect_button.clicked.connect(self.connect_function) # Connect the connect button to the connect_function
        self.swap_button.clicked.connect(self.swap_contacts) # Connect the swap button to the swap_contacts function
        self.abort_button.clicked.connect(self.abort_function)  # Connect the abort button to the abort_function
        self.reset_button.clicked.connect(self.reset_function) # Connect the reset button to the reset_function
        self.btn_add_user.clicked.connect(self.addUser) # Connect the add user button to the addUser function
        self.threadpool = QThreadPool.globalInstance() # Create a QThreadPool instance
        self.threadpool.setMaxThreadCount(3) # Set the maximum number of threads to 3
        self.worker_progress = {} # Create a dictionary to store the progress of each worker
        self.selected_contacts = [] # List to store the selected contacts
        self.worker_queue = Queue() # Create a queue to store the workers
    
    def addUser(self): # This is the slot function for the "Add User" button
        # This is the slot function for the "Add User" button
        self.ex = AddUser()
        apply_stylesheet(self.ex, theme='dark_blue.xml')
        self.ex.show()
    
    def search_user(self): # This is the slot function for the "Search" button
        with open("user_data.json", "r") as json_file:
            self.user_data = json.load(json_file)
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

    def add_contact(self): # This is the slot function for the "Add Contact" button
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
        
    def add_contact_from_result(self, item): # This is the slot function for the double-click event on the result_text_browser
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

    def remove_contact(self): # This is the slot function for the "Remove Contact" button
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


    def swap_contacts(self): # This is the slot function for the "Swap" button , to swap the selected contacts
        if len(self.selected_contacts) >= 2:
            self.selected_contacts[0], self.selected_contacts[1] = self.selected_contacts[1], self.selected_contacts[0]
            self.timer1_input.text, self.timer2_input.text = self.timer2_input.text, self.timer1_input.text
            self.update_contact_text_browser()
        elif len(self.selected_contacts) >= 3:
            self.selected_contacts[0], self.selected_contacts[1], self.selected_contacts[2] = self.selected_contacts[2], self.selected_contacts[1], self.selected_contacts[0]
            self.update_contact_text_browser()

    def update_contact_text_browser(self): # This function updates the contact_text_browser with the selected contacts
        self.contact_text_browser.clear()
        for contact in self.selected_contacts:
            item = QListWidgetItem(contact)
            self.contact_text_browser.addItem(item)

    def connect_function(self): # This is the slot function for the "Connect" button
        self.connect_button.setEnabled(False)
        timer1 = self.timer1_input.text()
        timer2 = self.timer2_input.text()   
        timer3 = self.timer3_input.text()
        self.progress_bar.setValue(0)  # Reset progress bar
        self.progress_bar.setMaximum(100) # Set maximum value for progress bar
        self.start_workers(self.selected_contacts, [timer1, timer2, timer3]) # Start the workers


    def start_workers(self, contacts, timers): # This function starts the workers

        while not self.worker_queue.empty(): # Check if the queue is not empty
            self.worker_queue.get() # Get the next worker from the queue

        # Create a worker for each contact and timer
        for contact, timer in zip(contacts, timers):
            worker = WhatsApp(contact, timer)
            worker.signals.progress.connect(self.progress_bar.setValue) # Connect the progress signal to the progress bar
            worker.signals.finished.connect(lambda :self.worker_completed(worker.uuid)) # Connect the finished signal to the worker_completed function
            self.worker_queue.put(worker) # Put the worker in the queue

            
        self.start_next_worker() # Start the next worker in the queue



    
    def start_next_worker(self): # This function starts the next worker in the queue
        
        if not self.worker_queue.empty(): # Check if the queue is not empty
            self.worker = self.worker_queue.get() # Get the next worker from the queue
            print(f"Starting worker with UUID {self.worker.uuid}") # Print the UUID of the worker
            self.threadpool.start(self.worker) # Start the worker

        else:
            print("All workers completed.")


    def worker_completed(self, uuid): # Add the uuid parameter to the worker_completed function
        self.connect_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.start_next_worker()  # Start the next worker in the queue
        self.refresh_progress(self.worker_queue.qsize()) # Update the progress bar based on the total number of workers

    def abort_function(self): # This is the slot function for the "Abort" button
        while not self.worker_queue.empty(): # Check if the queue is not empty
            worker = self.worker_queue.get() # Get the next worker from the queue
            worker.abort() # Abort the worker
            

    def refresh_progress(self, total_workers):
        if total_workers == 0:
            self.progress_bar.setValue(0)
        else:
            total_progress = sum(self.worker_progress.values())
            average_progress = total_progress / total_workers
            self.progress_bar.setValue(average_progress)


    def reset_function(self): # This is the slot function for the "Reset" button
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
        self.connect_button.setEnabled(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(f"Width: {app.primaryScreen().size().width()}")
    print(f"Height: {app.primaryScreen().size().height()}")
    window = PhonePortal()
    window.show()
    sys.exit(app.exec())
import unittest
from PyQt5.QtWidgets import QApplication
from generate_test import PhonePortal

class TestPhonePortal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.phone_portal = PhonePortal()

    def test_reset_function(self):
        self.phone_portal.user_id_input.setText("test")
        self.phone_portal.reset_function()
        self.assertEqual(self.phone_portal.user_id_input.text(), "")

    # Add more test methods here...

if __name__ == "__main__":
    unittest.main()import unittest
from PyQt5.QtWidgets import QApplication
from generate_test import PhonePortal

class TestPhonePortal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.phone_portal = PhonePortal()

    def test_reset_function(self):
        self.phone_portal.user_id_input.setText("test")
        self.phone_portal.reset_function()
        self.assertEqual(self.phone_portal.user_id_input.text(), "")

    # Add more test methods here...

if __name__ == "__main__":
    unittest.main()