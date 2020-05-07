import freezerstate.config
import smtplib, ssl

class EmailSender():
    
    def __init__(self, test_enabled = None, test_smtp_server = None):
        self.module = '[EMAIL]'
        self.enabled = freezerstate.config.SMTP_ENABLED if test_enabled is None else test_enabled
        self.smtp_server = freezerstate.config.SMTP_SERVER if test_smtp_server is None else test_smtp_server
        
    def notify(self, message, test_recipient = None, test_username = None, test_password = None, test_smtp_port = None):
        smtp_port = freezerstate.config.SMTP_PORT if test_smtp_port is None else test_smtp_port
        recipient = freezerstate.config.NOTIFICATION_EMAIL_ADDRESS if test_recipient is None else test_recipient
        smtp_username = freezerstate.config.SMTP_USERNAME if test_username is None else test_username
        smtp_password = freezerstate.config.SMTP_PASSWORD if test_password is None else test_password

        if self.enabled is True:
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(module, smtp_port, context=context) as server:
                server.login()
            # TODO: Complete this code
            
            print(f'--- {module} - Sending {message} to {recipient}')
        return