# Pyclier

A python CLI framework base on [argparse](https://docs.python.org/3/library/argparse.html), supporting: config system, command-completion, rich-text log, friendly help message prompt and so on.

> Note: This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [`zhangxianbing/cookiecutter-pypackage`](https://github.com/zhangxianbing/cookiecutter-pypackage) project template.

## Features

- [x] support friendly help message prompt
- [x] support configuration file parsing system
- [x] support easy-to-use interface for building complex CLI program
- [x] support rich-text and flexible log system (base on [rich](https://github.com/willmcgugan/rich))
- [x] support command auto-completion (base on [argcomplete](https://github.com/kislyuk/argcomplete))
- [ ] support auto generating and updating usage (based on [auto-usage](https://github.com/zhangxianbing/auto-usage))
- [ ] support updating CLI program

## Quick Start

### Installation

```bash

pip install pyclier

```

For using auto completion, you should first install [argcomplete](https://github.com/kislyuk/argcomplete) and the activate it:

```bash
pip install argcomplete
activate-global-python-argcomplete
```

Then add the following lines in your setup.py:

```py
from setuptools import setup

setup(...)

# post installation

from pyclier.setuptools import copytree, enable_complete

command = sys.argv[-1]
if command == "install":
    copytree("conf", appdirs.user_config_dir(prog_name))
    enable_complete(prog_name)

    import pip

    pip.main(["install", ".", "-U", "--no-index"])

```

### Run demo

```bash
cd pyclier-demo && make install
# then refresh your bash environment
pyclier -h
```
