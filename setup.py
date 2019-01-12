#!/usr/bin/env python
from os.path import dirname, join
from setuptools import setup


setup(
    name='sleepguard',
    version='1.0',
    author='Robin Lange',
    author_email='robin.langenc@gmail.com',
    license='MIT',
    py_modules=['sleepguard'],
    entry_points={
        'console_scripts': [
            'sleepguard=sleepguard:main',
        ],
    },
    package_data={'sleepguard': ['notify-send-all', 'bleep.wav']},
    keywords=['sleep', 'guard', 'timer'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
