import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gb-async-client',
    version='0.1',
    #packages=find_packages('secretdiary'),
    packages=find_packages(),
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Async Client',
    long_description=README,
    url='https://github.com/achicha/chat/tree/master/client',
    author='achicha',
    keywords=['client', 'server', 'async'],
    classifiers=[],
    install_requires=['PyQt5', 'quamash', 'sqlalchemy'],
    entry_points={
        'console_scripts': [
            'client = src.main:main',
        ]
    },
)
