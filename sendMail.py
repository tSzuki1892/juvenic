import smtplib
from email.mime.text import MIMEText


def formSendMail(bodytext, account, password, subject, from_email, to_email, to_email2):
    print(bodytext)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(account, password)

    msg = MIMEText(bodytext)
    msg['subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server.send_message(msg)
    server.close()

    if to_email2 != '':
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(account, password)
        msg = MIMEText(bodytext)
        msg['subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email2
        server.send_message(msg)
        server.close()
