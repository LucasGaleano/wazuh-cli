from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(emailFrom, emailTo, subject, content, mailServer):
    
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = subject
    MESSAGE['To'] = emailTo
    MESSAGE['From'] = emailFrom
    HTML_BODY = MIMEText(content, 'html')
    MESSAGE.attach(HTML_BODY)

    server = SMTP(host=mailServer, port=25)    
    
    server.sendmail(emailFrom, emailTo, MESSAGE.as_string())
    #server.sendmail(emailTo, emailFrom, 'Subject: {}\n\n{}'.format(subject, content))
    server.quit()
