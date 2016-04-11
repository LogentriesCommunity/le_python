from setuptools import setup

setup(
    name='Logentries',
    version='0.8',
    author='Mark Lacomber',
    author_email='marklacomber@gmail.com',
    packages=['logentries'],
    scripts=[],
    url='http://pypi.python.org/pypi/Logentries/',
    license='LICENSE.txt',
    description='Python Logger plugin to send logs to Logentries',
    long_description=open('README.md').read(),
    install_requires=[
        "certifi",
    ],
)
