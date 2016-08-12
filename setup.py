#!/usr/bin/env python
# -*- coding: utf-8 -*-

import audiotrans
from setuptools import setup, find_packages

install_requires = [
    'PyAudio',
    'numpy',
    'matplotlib'
]

setup(name='audiotrans',
      version=audiotrans.__version__,
      description=audiotrans.__desc__,
      author=audiotrans.__author__,
      author_email=audiotrans.__author_email__,
      url=audiotrans.__url__,
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'audiotrans = audiotrans.__main__:main',
          ],
      },
      install_requires=install_requires)
