from datetime import datetime, date
import re
import smtplib
from email.mime.text import MIMEText

# Define constants
LOG_FILE = '/var/log/celery/reviewWorker.log'
THRESHOLD = 1  # Number of occurrences to trigger the email
sender_email = 'aashish.pandey@collegedunia.com'
receiver_email = [ 'aashish.pandey@collegedunia.com','chandrakant.sharma@collegedunia.com','rohini.mishra@collegedunia.com']
mail_server = 'smtp.gmail.com'
mail_port = 587
mail_username = 'aashish.pandey@collegedunia.com'
mail_password = "Ap@123456"


def send_email( e):
    subject = "Serp Api not responding"
    body = f"Institution scraping stop because serp API gives: {e}"
    
    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    
    try:
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to authenticate SMTP server: {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    return False

# Initialize the count variable
# count = 0

# # Run the check function
# for i in [0,1,4,5,6,7,0,4,2,0,3,5,0,0,6,0,4,1,0]:
#     try:
#         12 / i
#     except Exception as e:
#         print('exception occurs')
#         e = str(e)
#         if count < 4:
#             if send_email(count, e):
#                 count += 1