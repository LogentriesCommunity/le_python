from distutils.core import setup

setup(
    name='Logentries',
    version='0.4',
    author='Mark Lacomber',
    author_email='marklacomber@gmail.com',
    packages=['logentries'],
    scripts=[],
    url='http://pypi.python.org/pypi/Logentries/',
    license='LICENSE.txt',
    description='Python Logger plugin to send logs to Logentries',
    long_description=open('README.rst').read(),
    install_requires=[
        "certifi",
    ],
)
