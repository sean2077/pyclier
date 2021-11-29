"""
Author       : zhangxianbing
Date         : 2021-06-02 23:20:17
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-06-06 16:57:52
"""
import json
import logging
import sys
from functools import partial
from typing import Callable, Dict, List, Optional, Union

import yaml
from rich.table import Table

from miga.utils import pretty_table
from .actor import FieldActor, Item

log = logging.getLogger(__name__)

DISPLAY_MODES = {
    "table": "display data in table format.",
    "json": "display data in json format.",
    "yaml": "display data in yaml format.",
}


def display_in_table(items: Union[dict, List[dict]], **kwargs) -> None:
    from rich import get_console

    if not items:
        log.warning("empty content!")
        print([])
        return

    kwargs.update(
        {
            "style": "green",
            "header_style": "bold bright_cyan",
            "row_styles": ["bright_yellow", "yellow"],
        }
    )

    if isinstance(items, list):
        table = Table("", *tuple(map(str, items[0].keys())), **kwargs)
        for i, item in enumerate(items):
            table.add_row(str(i + 1), *tuple(map(str, item.values())), end_section=True)
    elif isinstance(items, dict):
        table = Table("key", "value", **kwargs)
        for k, v in items.items():
            table.add_row(str(k), str(v), end_section=True)

    get_console().print(table, justify="center")


def display_in_json(data: Union[dict, List[dict]], indent=4):
    print(json.dumps(data, indent=indent))


def display_in_yaml(data: Union[dict, List[dict]]):
    yaml.dump(data, sys.stdout, sort_keys=False)


class Displayer(FieldActor):
    def __init__(
        self,
        field: Optional[str] = None,
        *fields,
        field_scope: List[str] = None,
        field_extractors: Optional[Dict[str, Callable]] = None,
        interval_symbol=",",
        mode="table",
        displayer_kwargs: dict = None,
    ):
        super().__init__(
            field,
            *fields,
            field_scope=field_scope,
            field_extractors=field_extractors,
            interval_symbol=interval_symbol,
        )

        if mode not in DISPLAY_MODES:
            raise ValueError(f"mode must be one of: {pretty_table(DISPLAY_MODES)}")
        self.displayer = globals()[f"display_in_{mode}"]
        if displayer_kwargs:
            self.displayer = partial(self.displayer, **displayer_kwargs)

    def _display_item(self, item: Item):
        if self.fields:
            for field in self.fields:
                item.get_or_extract(field, extractors=self.field_extractors)
            self.displayer(item.dict)
        else:
            self.displayer(item.raw)

    def _display_items(self, data: List[Item]):
        if self.fields:
            dicts = [
                {
                    field: item.get_or_extract(field, extractors=self.field_extractors)
                    for field in self.fields
                }
                for item in data
            ]
            self.displayer(dicts)
        else:
            self.displayer([item.raw for item in data])

    def __call__(self, data: Union[Item, List[Item]]):
        if isinstance(data, Item):
            self._display_item(data)
        elif isinstance(data, list):
            self._display_items(data)
        else:
            raise ValueError("Invalid data type")


if __name__ == "__main__":
    from miga.jp.app import get_extractors

    from ..utils import load_json

    extractors = get_extractors()

    d = load_json("test/data/app.json")

    item = Item(d)

    disp = Displayer(
        # "id,status,name,language,file",
        # "created_at",
        mode="table",
        field_extractors=get_extractors(),
    )
    disp(item)
