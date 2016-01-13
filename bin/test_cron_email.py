import sys
import smtplib
import netrc
from difflib import context_diff
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(f1, f2):
    smtpserver = "smtp.gmail.com"
    diff = context_diff(open(f1).readlines(), open(f2).readlines(),
                        fromfile=basename(f1), tofile=basename(f2))
    text = ''.join(diff)
    fromaddr = "in4pashchenko@gmail.com"
    toaddr = "in4-pashchenko@yandex.ru"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Cron test mail send"
    body = text
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP(smtpserver)
    secrets = netrc.netrc()
    netrclogin, netrcaccount, netrcpassword = secrets.authenticators(smtpserver)
    s.starttls()
    s.login(netrclogin, netrcpassword)
    s.sendmail('in4pashchenko@gmail.com', ['in4-pashchenko@yandex.ru'],
               msg.as_string())
    s.quit()

if __name__ == '__main__':
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    send_email(f1, f2)
