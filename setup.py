#!/usr/bin/env python
from distutils.core import setup

VERSION = "0.0.1"

setup(
    author='Nikolai Tschacher',
    name = "proxychecker",
    version = VERSION,
    description = "A Python proxychecker module that makes use of socks",
    url = "http://incolumitas.com",
    license = "BSD",
    author_email = "admin@incolumitas.com",
    keywords = ["socks", "proxy", "proxychecker"],
    py_modules = ['proxychecker', 'sockshandler', 'socks']
)
