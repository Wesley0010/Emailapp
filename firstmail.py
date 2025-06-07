import smtplib
from email.message import EmailMessage


gmail_address = 'mbewewesley37@gmail.com'
app_password = 'yrok sois knfx uoow'  # Use the 16-char password (no spaces)
recipient = 'mbewewesley37@gmail.com'

msg = EmailMessage()
msg['Subject'] = 'Test Email from Python (Gmail SMTP)'
msg['From'] = gmail_address
msg['To'] = recipient
msg.set_content('Hello! This is a test email sent using Gmail SMTP and Python.')

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Secure the connection
        smtp.login(gmail_address, app_password)
        smtp.send_message(msg)
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
