"""
Author       : zhangxianbing
Date         : 2021-06-02 23:14:17
Description  : Filter:  List[item] -> List[item]
LastEditors  : zhangxianbing
LastEditTime : 2021-06-06 17:34:58
"""
import logging
import re
from typing import Callable, Dict, Optional

from .actor import Item

log = logging.getLogger(__name__)

REP_CONDITION = re.compile(
    r"^(\S*?)\s*(<=|>=|==|!=|>|<| in | not in | is | not is | is not)\s*(.*?)$"
)
REVERSE_OPERATORS = {
    "==": "!=",
    "!=": "==",
    ">": "<",
    ">=": "<=",
    "<": ">",
    "<=": ">=",
    " in ": " not in ",
    " not in ": " in ",
    " is ": " not is ",
    " not is ": " is ",
}


class Filter:
    def __init__(
        self,
        condition: str,
        *,
        field_extractors: Optional[Dict[str, Callable]] = None,
        field_converter: Optional[Callable] = None,
        value_scope=None,
        value_converter: Optional[Callable] = None,
        reverse_symbol="~",
        interval_symbol=",",
    ):
        r = REP_CONDITION.search(condition)
        if not r:
            raise ValueError("Invalid regular expression")

        self.field = r.group(1)

        op = r.group(2)
        if op not in REVERSE_OPERATORS:
            raise ValueError(
                f"{op} not in supported operators: {tuple(REVERSE_OPERATORS.keys())}"
            )
        self.op = op

        values = r.group(3).split(interval_symbol)
        if value_scope:
            for value in values:
                value = value.strip()
                if value.startswith(reverse_symbol):
                    value = value[1:]
                if value not in value_scope:
                    raise ValueError(f"{value} not in scope: {value_scope}")
        self.values = values

        self.interval_symbol = interval_symbol
        self.reverse_symbol = reverse_symbol
        self.field_extractors = field_extractors
        self.field_converter = field_converter
        self.value_converter = value_converter

    def _filter(self, item: Item) -> bool:
        field = item.get_or_extract(self.field, extractors=self.field_extractors)
        if self.field_converter:
            field = self.field_converter(field)

        if isinstance(field, str):
            quote = '"'
        else:
            quote = ""

        _exprs = []

        def _add_expr(op, right):
            _exprs.append(f"__field{op}{quote}{right}{quote}")

        for value in self.values:
            value = value.strip(" ")
            if not value.startswith(self.reverse_symbol):
                if self.value_converter:
                    value = self.value_converter(value)
                _add_expr(self.op, value)
            else:
                value = value[1:]
                if self.value_converter:
                    value = self.value_converter(value)
                _add_expr(REVERSE_OPERATORS[self.op], value)

        final_expr = " or ".join(_exprs)
        return eval(final_expr, None, {"__field": field})

    def __call__(self, data: Item) -> bool:
        return self._filter(data)


if __name__ == "__main__":
    from miga.jp.app import get_extractors

    from ..utils import load_json

    extractors = get_extractors()

    d = load_json("test/data/app.json")
    print(extractors["id"](d))

    item = Item(d)

    filter_ = Filter("status==CANCELED", field_extractors=get_extractors())
    print(filter_(item))
