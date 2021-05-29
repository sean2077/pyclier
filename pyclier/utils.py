"""
Author       : zhangxianbing
Date         : 2021-05-26 08:59:38
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-28 22:37:24
"""
import json
import os

import yaml


def load_json(filename: str) -> dict:
    with open(filename) as f:
        d = json.load(f)
    return d


def load_yaml(filename: str) -> dict:
    with open(filename, "r") as f:
        d = yaml.safe_load(f)
    return d


def expand_path(path):
    r = os.path.expandvars(path)
    r = os.path.expanduser(r)
    return r
