# Pyclier

A python CLI framework base on [argparse](https://docs.python.org/3/library/argparse.html), supporting: config system, command-completion, rich-text log, friendly help message prompt and so on.

> Note: This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [`zhangxianbing/cookiecutter-pypackage`](https://github.com/zhangxianbing/cookiecutter-pypackage) project template.

## Features

- [x] support configuration file parsing system
- [x] support rich-text and flexible log system
- [x] support friendly help message prompt
- [x] support easy-to-use interface for building complex CLI program
- [ ] support interactive mode
- [ ] support command auto-completion

## Quick Start

### Installation

```bash

pip install pyclier

```

### Run demo

```bash
PYTHONPATH=. python demo/main.py
PYTHONPATH=. python demo/main.py -h
```
