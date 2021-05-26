"""
Author       : zhangxianbing
Date         : 2021-05-26 08:59:38
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-26 09:00:53
"""
import json

import yaml


def load_json(filename: str) -> dict:
    with open(filename) as f:
        d = json.load(f)
    return d


def load_yaml(filename: str) -> dict:
    with open(filename, "r") as f:
        d = yaml.safe_load(f)
    return d
