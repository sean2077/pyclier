"""
Author       : zhangxianbing
Date         : 2021-06-05 09:32:23
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-06-06 16:39:17
"""
import json
import logging
from operator import itemgetter
from typing import Callable, Dict, List, Optional

from ..argparse import ArgumentParserError

log = logging.getLogger(__name__)


class Item:
    def __init__(self, value: Dict):
        self._raw = value
        self._dict = {}

    @property
    def raw(self):
        return self._raw

    @property
    def dict(self):
        return self._dict

    def __repr__(self):
        if not self._dict:
            return f"\nraw: {json.dumps(self._raw, indent=4)}"
        return f"\ndict: {json.dumps(self._dict, indent=4)}"

    def set(self, key, value):
        self._dict[key] = value

    def set_defaults(self, **kwargs):
        self._dict.update(kwargs)

    def get(self, key):
        return self._dict.get(key)

    def get_or_extract(self, field, *, extractors=None):
        if field in self._dict:
            return self.get(field)

        if extractors and field in extractors:
            extractor = extractors[field]
        else:
            extractor = itemgetter(field)

        try:
            value = extractor(self._raw)
        except Exception as e:
            log.error(e)
            value = None

        self.set(field, value)
        return value


class FieldActor:
    def __init__(
        self,
        field: Optional[str] = None,
        *fields,
        field_scope: List[str] = None,
        field_extractors: Optional[Dict[str, Callable]] = None,
        field_converters: Optional[Dict[str, Callable]] = None,
        interval_symbol=",",
        reverse_symbol="~",
    ):
        self.field_extractors = field_extractors
        self.field_converters = field_converters
        self.interval_symbol = interval_symbol
        self.reverse_symbol = reverse_symbol

        self.fields = []
        self._add_field(field)
        for field in fields:
            self._add_field(field)

        if interval_symbol != " ":
            self.fields = [field.strip() for field in self.fields]

        if field_scope:
            for field in self.fields:
                if field.startswith(reverse_symbol):
                    field = field[1:]
                if field not in field_scope:
                    raise ArgumentParserError(f"{field} not in scope: {field_scope}")

    def _add_field(self, field):
        if isinstance(field, list):
            self.fields += field
        elif isinstance(field, str):
            self.fields += field.split(self.interval_symbol)
