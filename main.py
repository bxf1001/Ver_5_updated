import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtGui import QPixmap, QIcon
from run_me_queuing import PhonePortal
from add_user import AddUser
from data_entry import DataEntryApp
from rt_data import DataView
from search_data import TimestampedDataSearch
from qt_material import apply_stylesheet


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phone Potral")  # Set your window title
            
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create buttons
        self.btn_add_user = QPushButton('Add User', self)
        self.btn_connect = QPushButton('Connect', self)
        self.btn_data_entry = QPushButton('Data Entry', self)
        self.btn_data_view = QPushButton('Data View', self)
        self.btn_call_logs = QPushButton('Call Logs', self)
        self.btn_exit = QPushButton('Exit', self)

        # Connect buttons to functions
        self.btn_add_user.clicked.connect(self.addUser)
        self.btn_connect.clicked.connect(self.connect)
        self.btn_data_entry.clicked.connect(self.dataEntry)
        self.btn_data_view.clicked.connect(self.dataView)
        self.btn_call_logs.clicked.connect(self.callLogs)
        self.btn_exit.clicked.connect(self.exitApp)

        # Add buttons to the layout
        layout.addWidget(self.btn_add_user)
        layout.addWidget(self.btn_connect)
        layout.addWidget(self.btn_data_entry)
        layout.addWidget(self.btn_data_view)
        layout.addWidget(self.btn_call_logs)
        layout.addWidget(self.btn_exit)

        # Set the layout on the application's window
        self.setLayout(layout)

        self.setWindowTitle('Phone Portal V5')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def addUser(self):
        # This is the slot function for the "Add User" button
        self.ex = AddUser()
        apply_stylesheet(self.ex, theme='dark_blue.xml')
        self.ex.show()

    def connect(self):
        self.ex_4 = PhonePortal()
        self.ex_4.show()

    def dataEntry(self):
        self.ex_2 = DataEntryApp()
        apply_stylesheet(self.ex_2, theme='dark_blue.xml')
        self.ex_2.show()

    def dataView(self):
        headers = ['Date', 'AB-Block-1', 'AB-Block-2', 'Cellular-Block', 'HS-Block', 'A-Class', 'Quarantine', 'Hospital', 'Emulakath', 'Video', 'Audio', 'Total']
        self.app_demo = DataView(headers)  # Create an instance of the AppDemo class
        apply_stylesheet(self.app_demo, theme='dark_blue.xml')
        self.app_demo.setup_export_buttons()
        self.app_demo.show() 

    def callLogs(self):
        self.ex_3 = TimestampedDataSearch()
        self.ex_3.results_table.cellClicked.connect(self.ex_3.cellClicked)
        apply_stylesheet(self.ex_3, theme='dark_blue.xml')
        self.ex_3.show()

    def exitApp(self):
        # Empty function for "Exit" button
        pass

def main():
    app = QApplication(sys.argv)
    pixmap = QPixmap("logo.png")

    # Create and show the splash screen
    splash = QSplashScreen(pixmap)
    splash.show()
    
    ex = MyApp()
    ex.show()
    apply_stylesheet(ex, theme='dark_blue.xml')
    splash.finish(ex)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
