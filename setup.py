import os
from setuptools import setup, find_packages
from fest import get_version


setup(
	name = 'django-fest',
	version = get_version(),
	packages = find_packages(),
	package_data = {'fest': ['static/fest/lib/*.js',]},

	install_requires=[
		'PyV8',
	],

	author = 'Vladimir Rudnyh',
	author_email = 'rudnyh@corp.mail.ru',
	description = 'Use fest templates with Django'
)

