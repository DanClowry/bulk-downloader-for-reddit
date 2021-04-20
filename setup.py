#!/usr/bin/env python3
# encoding=utf-8

import sys

from setuptools import setup

if sys.version_info >= (3,9):
    setup(setup_requires=['pbr', 'appdirs'], pbr=True, data_files=[('config', ['bdfr/default_config.cfg'])])
else:
    raise RuntimeError("This package requres Python 3.9+")
