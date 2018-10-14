import os
from setuptools import setup, find_packages


def get_version(version_file='_version.py'):
    """Retrieve the package version from a version file in the package root."""
    filename = os.path.join(os.path.dirname(__file__), 'dirutility', version_file)
    with open(filename, 'rb') as fp:
        return fp.read().decode('utf8').split('=')[1].strip(" \n'")


setup(
    name='dirutility',
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        'looptools>=1.0.0',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'zipbackup = dirutility.backup:main',
            'dirpaths = dirutility.walk.walk:gui',
        ]
    },
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Add compare module and GUI to parse two directories and return lists of unique files.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
