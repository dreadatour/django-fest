import os
from setuptools import setup, find_packages
from fest import get_version


setup(
	name = 'django-fest',
	version = get_version(),
	packages = find_packages(),
	package_data = {'fest': ['static/fest/lib/*.js',]},

	install_requires=[
		'PyV8==1.0',
	],
	dependency_links=[
		'svn+http://pyv8.googlecode.com/svn/trunk/@429#egg=PyV8-1.0',
	],

	author = 'Vladimir Rudnyh',
	author_email = 'rudnyh@corp.mail.ru',
	description = 'Use fest templates with Django'
)

