<div align="left">
  <h1>style-transfer-utility</h1>
</div>

<!-- TOC -->

- [About](#about)
  - [Status](#status)
- [Requirements](#requirements)
- [Setup](#setup)
  - [Download the models](#download-the-models)
  - [Install dependencies](#install-dependencies)
- [Usage](#usage)
- [Development](#development)
- [TODO](#todo)
- [References](#references)

<!-- /TOC -->

## About

Utility for applying style transfer models into images or videos

### Status

**ALPHA** - bleeding edge / work-in-progress

## Requirements

- [pyenv](https://github.com/pyenv/pyenv)
- [pipenv](https://github.com/pypa/pipenv)


## Setup

### Download the models

```sh
$ bash setup.sh
```

### Install dependencies

```sh
$ pipenv install --dev
$ pipenv shell
```

## Usage

```
$ stu --help
Usage: stu [OPTIONS]

  style-transfer-utility: stu
  Utility for applying style transfer models into images or videos.

Options:
  -i, --input-path TEXT           [required]
  --style [candy|composition 6|feathers|la_muse|mosaic|starry night|the scream|the wave|udnie]
                                  [required]
  -o, --output TEXT               the output name
  --debug                         [default: False]
  --all-style                     apply all styles to the image  [default:
                                  False]

  --version                       Show the version and exit.
  --help                          Show this message and exit.
```


## Development

```sh
$ pipenv install --dev
$ pipenv shell
$ pre-commit install
```

## TODO
- GPU acceleration
- Colab notebook

## References
- [amalshaji/style-transfer](https://github.com/amalshaji/style-transfer)
