import os
import sys
import shutil
import smtplib
import netrc
from difflib import context_diff
from email.mime.application import MIMEApplication
from filecmp import cmp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from watcher import get_last_svlbi_schedule
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -'
                                                ' %(message)s')
# logging.disable()


def func(f1, f2):
    """
    Note that by default, this looks to check your netrc credentials
    to use this feature, create a .netrc file, so that only you can read and
    write it

        touch ~/.netrc
        chmod 600 ~/.netrc
    and then add the information for the gmail smtp server, i.e.
    ``machine smtp.gmail.com login yourusername@gmail.com password
    yourpassword``
    """
    smtpserver = "smtp.gmail.com"
    tls = True
    fromaddr = "in4pashchenko@gmail.com"
    toaddr = "in4-pashchenko@yandex.ru"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    if not cmp(f1, f2):
        logging.debug("Files {} & {} differs!".format(basename(f1),
                                                      basename(f2)))
        diff = context_diff(open(f1).readlines(), open(f2).readlines(),
                            fromfile=basename(f1), tofile=basename(f2))
        text = ''.join(diff)
        with open(f2, "rb") as fil:
            msg.attach(MIMEApplication(fil.read(),
                                       Content_Disposition='attachment; filename="%s"' % basename(f2),
                Name=basename(f2)))
        body = text
        msg['Subject'] = "Changes in SVLBI schedule"
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP(smtpserver)
        secrets = netrc.netrc()
        netrclogin, netrcaccount, netrcpassword = secrets.authenticators(smtpserver)
        if tls:
            s.starttls()
            s.login(netrclogin, netrcpassword)
        s.sendmail('in4pashchenko@gmail.com', ['in4-pashchenko@yandex.ru'],
                   msg.as_string())
        s.quit()

        logging.debug("Moving file {} to {}!".format(basename(f2),
                                                     basename(f1)))
        shutil.move(f2, f1)
    else:
        logging.debug("Files {} & {} are the same!".format(basename(f1),
                                                           basename(f2)))
        text = ''.join('')
        body = text
        msg['Subject'] = "No changes in SVLBI schedule"
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP(smtpserver)
        secrets = netrc.netrc()
        netrclogin, netrcaccount, netrcpassword = secrets.authenticators(smtpserver)
        if tls:
            s.starttls()
            s.login(netrclogin, netrcpassword)
        s.sendmail('in4pashchenko@gmail.com', ['in4-pashchenko@yandex.ru'],
                   msg.as_string())
        s.quit()
        os.unlink(f2)


if __name__ == '__main__':
    month = sys.argv[1]
    year = sys.argv[2]
    # User-specified directory
    dir = sys.argv[3]
    # Get last SVLBI schedule
    get_last_svlbi_schedule(month, year, os.path.join(dir, 'svlbi_new.txt'))
    func(os.path.join(dir, 'svlbi.txt'), os.path.join(dir, 'svlbi_new.txt'))
