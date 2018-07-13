from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.2.6',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'looptools',
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Further improvements to functionality and structure of DirPaths.  More parameters added to further '
                'tune result set.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
