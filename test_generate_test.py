import unittest
from PyQt5.QtWidgets import QApplication
from run_me_queuing import PhonePortal

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