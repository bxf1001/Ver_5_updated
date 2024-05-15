from run_me_queuing import UserContactApp
from PyQt5.QtWidgets import QProgressBar

def test_update_progress():
    window = UserContactApp()
    window.progress_bar = QProgressBar()
    
    # Set the maximum value of the progress bar
    window.progress_bar.setMaximum(100)
    
    # Call the update_progress method with a value of 50
    window.update_progress(50)
    
    # Check if the value of the progress bar has been updated
    assert window.progress_bar.value() == 50