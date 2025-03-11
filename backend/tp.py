import smtplib

sender_email = "pensionmanagementtool@gmail.com"
receiver_email = "shwetabhagat2025@gmail.com"
password = "Shivam@28"

message = """\
Subject: Test Email from Flask

This is a test email to check if SMTP is working."""

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Error sending email:", str(e))
