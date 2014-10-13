#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'BonfireManager',
    version = '0.1a',
    description = 'BonfireManager is a talk manager for unconferences.',
    author = 'Matt Copperwaite',
    author_email = 'matt@copperwaite.net',
    url = 'https://github.com/yamatt/bonfiremanager/',
    packages=["bonfiremanager"],
    install_requires = [
        "django>=1.7",
        "django-debug-toolbar",
        "django-bootstrap3"
    ],
    license = "AGPLv3",
    classifiers = [
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ]
)
