"""
Author       : zhangxianbing
Date         : 2021-06-02 23:16:06
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-06-06 16:49:46
"""
from typing import Callable, Dict, List, Optional

from .actor import FieldActor, Item


class Sorter(FieldActor):
    def _sort(self, data: List[Item]) -> List[Item]:
        if not self.fields:
            return data

        def _sort_by_field(field, reverse=False):
            if self.field_converters and field in self.field_converters:
                key = lambda item, field=field: self.field_converters[field](
                    item.get_or_extract(field, extractors=self.field_extractors)
                )
            else:
                key = lambda item, field=field: item.get_or_extract(
                    field, extractors=self.field_extractors
                )
            data.sort(key=key, reverse=reverse)

        for field in reversed(self.fields):
            if not field.startswith(self.reverse_symbol):
                _sort_by_field(field)
            else:
                _sort_by_field(field[1:], True)

        return data

    def __call__(self, data: List[Item]) -> List[Item]:
        return self._sort(data)


if __name__ == "__main__":
    d = [
        Item({"id": 1, "name": "d"}),
        Item({"id": 2, "name": "a"}),
        Item({"id": 2, "name": "c"}),
        Item({"id": 4, "name": "b"}),
    ]

    f = Sorter("id", "name")
    print(f(d))
