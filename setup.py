from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.2.13',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'looptools',
        'databasetools',
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='GUI window added to walk.py, accessible when walk.py is called as main script.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
