# moddule responsible for handling email related tasks
import smtplib
from email.mime.text import MIMEText

# set up connection to email server
#
# @input smtp_server
# @input smtp_port
# @input smtp_user
# @input smtp_password
# 
# @return email server object
def connect_to_email_server(smtp_server, smtp_port, smtp_user, smtp_password):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    return server

# create email and send email
#
# @input subject
# @input body
# @input smtp_user
# @input recipient
# @input email_server
#
def send_email(subject,body,smtp_user,recipient,email_server):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = recipient

    # Send the email
    email_server.sendmail(smtp_user, recipient, msg.as_string())

# disconnect from email serfver
#
# @input email_server
#
def disconnect_email_server(email_server):
    email_server.quit()


if __name__ == '__main__':
    # testing
    import os
    os.chdir("C:\\Users\\samleung\\Documents\\workspace-py\\lung_classifier_daemon\\src")
    import password as pwd

    email_server = se.connect_to_email_server("smtp.mail.ubc.ca",587,pwd.smtp_user,pwd.smtp_password)
    se.send_email("testing","test email msg","map.core@ubc.ca","samuel.leung@vch.ca",email_server)
    se.disconnect_email_server(email_server)