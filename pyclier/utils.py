"""
Author       : zhangxianbing
Date         : 2021-05-26 08:59:38
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-06-18 09:13:59
"""
import importlib.util
import json
import os
import time

import yaml


def load_json(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d


def load_yaml(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        d = yaml.safe_load(f)
    return d


def expand_path(path):
    r = os.path.expandvars(path)
    r = os.path.expanduser(r)
    return r


def get_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())


def load_module_from_location(location: str, name: str = "module.name"):
    "return module loaded from file location"
    spec = importlib.util.spec_from_file_location(name, location)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sanitize_filepath(path):
    return path.replace(":", "-").replace(os.path.sep, "")
