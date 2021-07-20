from setuptools import setup, find_packages

setup(name='ish_parser',
  version='0.0.24',
  author_email='thayden@gmail.com',
  description='Parser for NOAA ISH (integrated surface hourly) reports',
  author='thayden',
  url='https://github.com/haydenth/ish_parser',
  packages=find_packages(exclude=['contrib', 'docs', 'tests']),
  py_modules=['ish_parser', 'ish_report'])
