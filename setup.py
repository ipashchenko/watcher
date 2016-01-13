import setuptools

setuptools.setup(
    name="watcher",
    version="0.1.0",
    url="[https://github.com/ipashchenko/watcher",

    author="Ilya Pashchenko",
    author_email="in4pashchenko@gmail.com",

    description="Checking RA schedules changes",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),
    scripts=['bin/cron_command.py', 'bin/add_cron_job.py'],

    install_requires=['python-crontab'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)
