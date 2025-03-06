from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_welcome_email(email, name):
    """Send a welcome email to the new user."""
    subject = "Welcome to the Pension Benefits Platform!"
    body = f"Hello {name},\n\nWelcome to our Pension Benefits platform! Your account has been successfully created.\n\nBest regards,\nPension Benefits Team"

    msg = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = body

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False
