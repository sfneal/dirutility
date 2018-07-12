from setuptools import setup, find_packages

setup(
    name='dirutility',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'looptools',
    ],
    url='https://github.com/mrstephenneal/dirutility',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Improved filtering system DirPaths class, filters are applied before adding directories and files to '
                'respective lists. Add level limiter parameters to retrieve files within min and max levels.',
    long_description='Utility functions for quickly reading directory contents and refactoring folder structure'
)
