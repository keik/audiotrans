#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

install_requires = [
    'PyAudio',
    'numpy',
    'matplotlib',
    'subarg'
]

setup(name='audiotrans',
      version='0.0.1.dev1',
      description="""Transform audio in real-time""",
      author='keik',
      author_email='k4t0.kei@gmail.com',
      url='https://github.com/keik/audiotrans',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Topic :: Multimedia :: Sound/Audio :: Conversion',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'audiotrans = audiotrans.__main__:main',
          ],
      },
      install_requires=install_requires)
