from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.2.17',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'looptools',
        'databasetools',
        'PySimpleGUI',
        'tkinter'
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Added tkinter as a dependency.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
