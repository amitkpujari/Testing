import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Port for TLS
    sender_email = 'amit.sam124@gmail.com'
    receiver_email = 'amitkpujari@gmail.com'
    password = 'axdd sitj ikkt oyzz'

    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Test Email'
    body = 'This is a test email sent using Python.'
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('Email sent successfully')

    except Exception as e:
        print(f'Failed to send email: {e}')

    finally:
        # Disconnect from SMTP server
        server.quit()

if __name__ == "__main__":
    send_email()
