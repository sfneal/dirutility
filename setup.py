from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'looptools',
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Utility functions for reading directory contents and refactoring folder structure',
    long_description='Utility functions for reading directory contents and refactoring folder structure'
)
