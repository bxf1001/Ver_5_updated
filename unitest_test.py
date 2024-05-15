import unittest
from run_me_queuing import PhonePortal

class TestUserContactApp(unittest.TestCase):
    def setUp(self):
        self.app = PhonePortal()

    def test_update_progress(self):
        # Set the progress bar value to 0
        self.app.progress_bar.setValue(0)

        # Call the update_progress function with a value of 50
        self.app.update_progress(50)

        # Check if the progress bar value is now 50
        self.assertEqual(self.app.progress_bar.value(), 50)

if __name__ == '__main__':
    unittest.main()