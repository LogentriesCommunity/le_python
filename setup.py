from setuptools import setup


with open('README.rst', 'r') as f:
    long_description = f.read()


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
    long_description=long_description,
    install_requires=[
        "certifi",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
