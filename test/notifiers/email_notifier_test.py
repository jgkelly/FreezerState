import unittest
from freezerstate.notifiers.email import EmailSender

class Email_Notifier_Tests(unittest.TestCase):
    
    def setUp(self):
        self.email = EmailSender(True, 'smtp.email.com')

    
    