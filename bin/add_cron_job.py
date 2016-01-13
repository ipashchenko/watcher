import os
import sys
import subprocess
from crontab import CronTab
path = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, path)
from watcher import watcher
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -'
                                                ' %(message)s')
# logging.disable()


def add_svlbi_cron_job(month, year, save_dir, user=True):
    """
    Function that adds entry to crontab with checking last SVLBI schedule for
    changes.

    :param month:
        Month [1 - 12].
    :param year:
        Year (eg. 2016).
    :param save_dir:
        Directory to store files.
    :param user: (optional)
        User of crontab. If ``True`` then current user. (default: ``True``)
    """
    # First download current version of SVLBI schedule and put it to
    # user-specified directory
    logging.debug("Downloading last SVLBI schedule to {}".format(save_dir))
    if not os.mkdir(save_dir):
        subprocess.Popen(['mkdir', '-p', save_dir])
    watcher.get_last_svlbi_schedule(month, year, os.path.join(save_dir,
                                                              'svlbi.txt'))

    # Add crontab with user specified dates and directory
    cron = CronTab(user=user)
    cmd = 'cron_command {} {} {}'.format(month, year, save_dir)
    cron_job = cron.new(command=cmd, comment="checking SVLBI schedule for"
                                             " {}-{}".format(month, year))
    cron_job.hour.every(1)
    if month == 1:
        month_ = 12
    else:
        month_ = month - 1
    cron_job.month.during(month_, month)
    assert cron_job.is_valid() == True
    comments = cron.find_comment('SVLBI schedule for {}-{}'.format(month, year))
    if comments:
        raise Exception("There is already job with given parameters!")
    print cron_job.render()
    cron.write_to_user(user=user)


if __name__ == '__main__':
    if not len(sys.argv) == 4:
        print("Usage: add_cron_job.py month year directory")
        sys.exit(0)
    month = sys.argv[1]
    year = sys.argv[2]
    # User-specified directory
    dir = sys.argv[3]
    # Add cron job
    add_svlbi_cron_job(month, year, dir)
