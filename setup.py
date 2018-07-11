from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'looptools',
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Added multiprocessing support to DirPaths class.  Speed improvements for directory walking.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
