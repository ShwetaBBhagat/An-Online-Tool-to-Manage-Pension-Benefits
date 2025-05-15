from flask_mail import Message, Mail
from threading import Thread
from flask import current_app
import os
from config import Config

mail = Mail()

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)

# WELCOME EMAIL TO EMPLOYEE WITH MFA QR
def send_welcome_email(user_email, user_name, qr_code_path, temp_password):
    """Send a real-time welcome email with the MFA QR code."""
    msg = Message("Welcome to Pension Benefits App!",
                  sender="your-email@example.com",
                  recipients=[user_email])
    
    msg.body = f"""Hello {user_name},

Welcome to the Pension Benefits Platform! Your account has been successfully created by your employer.

🛡 Your temporary login password is: {temp_password}

To complete your account setup, please enable Multi-Factor Authentication (MFA) using Google Authenticator:

1. Download Google Authenticator from your app store.
2. Scan the attached QR Code in Google Authenticator.
3. Use the generated 6-digit codes during login.

⚠️ Important:
- Please change your password after your first login for security.
- Your MFA 6-digit code will be required at every login.

Thank you,
Pension Benefits Team
"""

    # Attach QR Code to Email
    with open(qr_code_path, "rb") as qr_code_file:
        msg.attach("mfa_qr_code.png", "image/png", qr_code_file.read())

    # Send email in a separate thread
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

# RESET PASSWORD EMAIL
def send_reset_email(user_email, reset_url):
    """Send a password reset email with a reset link."""
    msg = Message("Password Reset Request",
                  sender="your-email@example.com",
                  recipients=[user_email])

    msg.body = f"""Hello,

To reset your password, please click the link below:

{reset_url}

If you did not request this reset, please ignore this email.

Thank you!
"""
    # Send email in a separate thread
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

#STATEMENT NOTIFICATION
def send_statement_notification(user_email, user_name):
    subject = "New Pension Statement Added"
    msg = Message(subject, recipients=[user_email])
    msg.body = f"""Hi {user_name},

A new pension statement has been added to your account.

Please log in to your pension dashboard to view the details:
{Config.CLIENT_URL}/login

Thank you,
Pension Benefits Team
"""
    try:
        mail.send(msg)
        print(f"Notification email sent to {user_email}")
    except Exception as e:
        print(f"Failed to send statement notification email: {e}")

#EMPLOYER ACCOUNT SETUP EMAIL
def send_employer_setup_email(email, name, qr_path, temp_password):
    """
    Sends a setup email to a new employer with MFA QR code and temporary password.
    """
    subject = " Set Up Your Pension Portal Employer Account"

    # Plain text fallback
    plain_body = f"""Hi {name},

You've been registered as an employer on the Pension Portal.

 Temporary Password: {temp_password}

To complete your setup:
1. Scan the attached MFA QR code in Google Authenticator.
2. Use the 6-digit code when logging in.

This email contains your MFA QR and a temporary password.
Please log in and change your password immediately.

Kind regards,  
Pension Benefits Team
"""

    # HTML body
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hello <strong>{name}</strong>,</p>

        <p>You've been successfully registered as an <strong>Employer</strong> in the <strong>Pension Portal</strong>.</p>

        <p><strong>Your Temporary Password:</strong> <code style="color:#d63384;">{temp_password}</code></p>

        <p>To complete your account setup:</p>
        <ol>
            <li>Download <strong>Google Authenticator</strong> from the app store.</li>
            <li>Scan the attached QR code.</li>
            <li>Use the 6-digit MFA code during login.</li>
        </ol>

        <p><strong>This email contains your MFA QR code and your initial login password.</strong></p>

        <p>Please log in immediately and change your password for security.</p>

        <p style="font-size: 0.9rem; color: #777;">
            Kind regards,<br>
            <strong>Pension Benefits Team</strong><br>
            <em>This is an automated email. Do not reply.</em>
        </p>
    </body>
    </html>
    """

    # Create and send message
    msg = Message(subject, recipients=[email])
    msg.body = plain_body
    msg.html = html_body

    # Attach MFA QR code
    with open(qr_path, "rb") as qr_file:
        msg.attach("mfa_qr_code.png", "image/png", qr_file.read())

    # Async email sending
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

