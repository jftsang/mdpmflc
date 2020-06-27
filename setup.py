#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='mdpmflc',
      version='0.0.0-DEVELOPMENT',
      description='MercuryDPM Flask Controller',
      author='J. M. F. Tsang',
      author_email='j.m.f.tsang@cantab.net',
      url='https://www.github.com/jftsang/mdpmflc/',
      packages=find_packages(),
      install_requires=['Flask>=1.1.2',
                        'matplotlib>=3.2.0']
 )
