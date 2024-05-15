import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
import uuid

class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)

    def run(self):
        tasks = [self.task1, self.task2, self.task3]  # Add your tasks here

        for task in tasks:
            task()

    def task1(self):
        # Task 1 logic here
        self.progress_updated.emit(25)
        self.msleep(1000)

    def task2(self):
        # Task 2 logic here
        self.progress_updated.emit(50)
        self.msleep(1000)

    def task3(self):
        # Task 3 logic here
        self.progress_updated.emit(75)
        self.msleep(1000)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.progress_bar = QProgressBar()
        self.start_button = QPushButton('Start')
        self.stop_button = QPushButton('Stop')

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.worker_thread = WorkerThread()
        self.worker_thread.progress_updated.connect(self.update_progress)

        self.start_button.clicked.connect(self.start_progress)
        self.stop_button.clicked.connect(self.stop_progress)

    def start_progress(self):
        self.worker_thread.start()

    def stop_progress(self):
        self.worker_thread.terminate()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    thread_id = str(uuid.uuid4())
    print(f"Thread ID: {thread_id}")
    sys.exit(app.exec_())