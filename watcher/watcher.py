from ftplib import FTP
from fnmatch import fnmatch


month_dict = {'1': 'jan', '2': 'feb', '3': 'mar', '4': 'apr', '5': 'may',
              '6': 'jun', '7': 'jul', '8': 'aug', '9': 'sep', '10': 'oct',
              '11': 'nov', '12': 'dec'}


def get_last_svlbi_schedule(month, year, save_fn):
    """
    Get SVLBI schedule for given month and year.

    :param month:
        Month [1 - 12].
    :param year:
        Year (eg. 2016).
    :param save_fn:
        File to save.

    """
    ftp = FTP(host='jet.asc.rssi.ru', user='anonymous', passwd='')
    ftp.cwd('/outgoing/yyk/Radioastron/block_schedule/')
    fname = None
    year = str(year)
    for fn in ftp.nlst():
        if fnmatch(fn, 'RA_block_schedule.{}{}'.format(month_dict[month],
                                                       year[2:])):
            fname = fn
    if not fname:
        raise Exception()
    with open(save_fn, "wb") as write_file:
        ftp.retrbinary('RETR %s' % fname, write_file.write)
