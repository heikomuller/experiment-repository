#! /usr/bin/env python

from setuptools import setup

setup(
    name='exprepo',
    version='0.1.0',
    description='Library to manage and manipulate experiment settings, command, and results',
    keywords='research ',
    author='Heiko Mueller',
    author_email='heiko.muller@gmail.com',
    url='https://github.com/heikomuller/experiment-repository',
    license='GPLv3',
    packages=['exprepo'],
    package_data={'': ['LICENSE']},
    install_requires=['pyyaml']
)
