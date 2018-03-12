import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        #check_call("apt-get install this-package".split())
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)


setup(
    name='aiogbchat',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Async Client-Server',
    long_description=README,
    url='https://github.com/achicha/chat/',
    author='achicha',
    keywords=['client', 'server', 'asyncio', 'Qt'],
    classifiers=[],
    cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },
    install_requires=['PyQt5', 'quamash', 'sqlalchemy'],
    entry_points={
        'console_scripts': [
            'server = aiogbserver.main:main',
            'client = aiogbclient.main:main',
        ]
    },
)
