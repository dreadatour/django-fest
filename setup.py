from distutils.core import setup
import os

from fest import get_version


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
	os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('fest'):
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'): del dirnames[i]
	if '__init__.py' in filenames:
		pkg = dirpath.replace(os.path.sep, '.')
		if os.path.altsep:
			pkg = pkg.replace(os.path.altsep, '.')
		packages.append(pkg)
	elif filenames:
		prefix = dirpath[5:] # Strip "fest/" or "fest\"
		if prefix == 'static/fest/lib':
			for f in filenames:
				data_files.append(os.path.join(prefix, f))


setup(name='django-fest',
	version=get_version(),
	description='Use fest templates with Django',
	author='Vladimir Rudnyh',
	author_email='rudnyh@corp.mail.ru',
	package_dir={'fest': 'fest'},
	packages=packages,
	package_data={'fest': data_files},
)

