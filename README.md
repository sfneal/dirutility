# Directory Utilities

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

## Running Tests

Example use of the dirutility Python package

### DirPaths class usage

[DirPaths.Walk](https://i.imgur.com/NfmBYp6.gifv)

<iframe class="imgur-embed" width="100%" height="570" frameborder="0" src="https://i.imgur.com/NfmBYp6.gifv#embed"></iframe>

Generate list of all file paths within a directory.
Generate file paths list with filters specifying what files to include (not limited to file types, can be any string).
Generate file paths list and exclude particular files.
Generate file paths list with concatenated full paths.

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [looptools](https://github.com/mrstephenneal/looptools) - Logging output, timing processes and counting iterations.
* [tqdm](https://github.com/tqdm/tqdm) - A fast, extensible progress bar for Python

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Stephen Neal** - *Initial work* - [StephenNeal](https://github.com/mrstephenneal)

See also the list of [contributors](https://github.com/dirutility/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc