# Directory Utilities

[![GuardRails badge](https://badges.production.guardrails.io/mrstephenneal/dirutility.svg)](https://www.guardrails.io)

dirutility is a Python package for generating an inventory of files within a directory tree.

_Often we encounter directories with vast file structures too large to sort through by manually.  Directory Utilities
allows users to create inventories of files and manipulated data structures._


### How it works

Directory Utilities is built using almost entirely builtin Python libraries making it extremely lightweight. The walk
module performs 'inventory' tasks that return information on file and folder contents of a root directory.  The move
module performs 'structure' tasks that reorganize the data structures within a directory based on a variety of
parameters.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Upgrade to the latest version of pip

```
pip install --upgrade pip
```

### Installing

Create a virtual development environment and install the latest version of dirutility from PyPi or github

PyPi distribution

```
pip install dirutility
```

GitHub distribution

```
pip install git+git://github.com/mrstephenneal/dirutility.git
```
or

```
pip install git+https://github.com/mrstephenneal/dirutility.git
```

## Example Usage

Outlined below are basic uses of the four main classes of the directory utility python package.

* DirPaths - Retrieve a list of paths within a root directory
* DirTree - Retrive a nested dictionary representing a roots file structure
* FlattenTree - Flattens the contents of a root directory by moviing all sub-folders and files to root
* CreateTree - Create organized file structure based on indexing of files within root

### DirPaths class

This class generates a list of either files and or folders within a root directory.  The walk method generates a directory list of files by walking the file tree top down or bottom up.  The files and folders method generate a list of files or folders in the top level of the tree.

Generate list of all file paths within a directory.
<br><img src="https://i.imgur.com/Ur7dGOC.gif" width="500"><br>

<a href="https://i.imgur.com/ogj9ZNQ.gif">Generate file paths list with filters specifying what files to include (not limited to file types, can be any string).<a>

<a href="https://i.imgur.com/dGAAdDO.gif">Generate file paths list and exclude particular files.<a>

<a href="https://i.imgur.com/cQjrL18.gif">Generate file paths list with concatenated full paths.<a>

```python
# Root directory
root = '/Volumes/Storage/test'
dirs = DirPaths(root, to_include=['.psd', '.png'], to_exclude=['.dwg'])
```

## Built With

* [looptools](https://github.com/mrstephenneal/looptools) - Logging output, timing processes and counting iterations.
* [tqdm](https://github.com/tqdm/tqdm) - A fast, extensible progress bar for Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/mrstephenneal/dirutility/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/dirutility/tags). 

## Authors

* **Stephen Neal** - *Initial work* - [StephenNeal](https://github.com/mrstephenneal)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details