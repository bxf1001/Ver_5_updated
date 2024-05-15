import keyboard
from PyQt5.QtCore import QRunnable, pyqtSlot
from PyQt5.QtWidgets import QApplication
from pywinauto import Application
from time import sleep
import subprocess
from pywinauto.keyboard import send_keys
import uuid


class WhatsApp: # Remove inheritance from QRunnable

    def __init__(self, number, timer): # Add the timer parameter and contact parameter
        self.timer = float(timer) * 60 # Convert the timer to seconds
        self.number = number  
        self.aborted = False       # Store the contact number
        self.uuid = uuid.uuid4().hex          # Generate a unique identifier for the worker
        
    @pyqtSlot(int)        
    def run(self):          # Remove the run method
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
