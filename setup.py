from distutils.core import setup

setup(
	name='LogentriesLogger',
	version='0.2.1',
	author='Mark Lacomber',
	author_email='marklacomber@gmail.com',
	packages=['logentries'],
	scripts=[],
	url='http://pypi.python.org/pypi/LogentriesLogger/',
	license='LICENSE.txt',
	description='Python Logger plugin to send logs to Logentries',
	long_description=open('README.md').read(),
)
