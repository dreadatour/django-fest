import os
from setuptools import setup, find_packages
from fest import get_version


# redefine V8_SVN_URL env variable (needs to install PyV8)
#v8_svn_url = getattr(os.environ, 'V8_SVN_URL', '')
#os.environ['V8_SVN_URL'] = 'http://v8.googlecode.com/svn/branches/3.7/'

setup(
	name = 'django-fest',
	version = get_version(),
	packages = find_packages(),
	package_data = {'fest': ['static/fest/lib/*.js',]},

#	install_requires=[
#		'PyV8==1.0',
#	],
#	dependency_links=[
#		'http://pyv8.googlecode.com/svn/trunk/#egg=PyV8-1.0',
#	],

	author = 'Vladimir Rudnyh',
	author_email = 'rudnyh@corp.mail.ru',
	description = 'Use fest templates with Django'
)

# restore V8_SVN_URL env variable
#os.environ['V8_SVN_URL'] = v8_svn_url

