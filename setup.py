from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.2.24',
    packages=find_packages(),
    install_requires=[
        'looptools>=1.0.0',
        'tqdm',
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Add compare module and GUI to parse two directories and return lists of unique files.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
