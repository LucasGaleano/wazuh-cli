from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(emailTo, emailFrom, subject, content, mailServer):
    
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = subject
    MESSAGE['To'] = emailTo
    MESSAGE['From'] = emailFrom
    HTML_BODY = MIMEText(content, 'html')
    MESSAGE.attach(HTML_BODY)

    server = SMTP(host=mailServer, port=25)
    server.connect()
    
    
    server.sendmail(emailTo, emailFrom, MESSAGE.as_string())
    #server.sendmail(emailTo, emailFrom, 'Subject: {}\n\n{}'.format(subject, content))
    server.quit()
