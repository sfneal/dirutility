from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.2.15',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'looptools',
        'databasetools',
        'PySimpleGUI'
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='walk.py GUI converted to a function call.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
