"""
Author       : zhangxianbing
Date         : 2021-06-03 12:21:37
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-06-17 16:22:50
"""
import argparse
from typing import Any, Callable, Dict, List, Optional, Sequence, Text, Union

from .displayer import Displayer
from .filter import Filter
from .sorter import Sorter


def split_action(split=lambda s: s.split(",")):
    class _Action(argparse.Action):
        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[Text, Sequence[Any], None],
            option_string: Optional[Text],
        ) -> None:
            setattr(namespace, self.dest, split(values))

    return _Action


def filter_action(
    field_name,
    op="==",
    *,
    field_extractors: Optional[Dict[str, Callable]] = None,
    field_converter: Optional[Callable] = None,
    value_scope: List[str] = None,
    value_converter: Optional[Callable] = None,
    reverse_symbol="~",
    interval_symbol=",",
    save_dest=False,
):
    class _Action(argparse.Action):
        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[Text, Sequence[Any], None],
            option_string: Optional[Text],
        ) -> None:
            condition = f"{field_name}{op}{values}"
            f = Filter(
                condition,
                field_extractors=field_extractors,
                field_converter=field_converter,
                value_scope=value_scope,
                value_converter=value_converter,
                reverse_symbol=reverse_symbol,
                interval_symbol=interval_symbol,
            )

            if not hasattr(namespace, "filters"):
                setattr(namespace, "filters", {})

            namespace.filters[self.dest] = f

            if not hasattr(namespace, "filter_regulars"):
                setattr(namespace, "filter_regulars", [])

            namespace.filter_regulars.append(condition)

            if save_dest:
                setattr(namespace, self.dest, values)

    return _Action


def sorter_action(
    *,
    field_scope: List[str] = None,
    field_extractors: Optional[Dict[str, Callable]] = None,
    field_converters: Optional[Dict[str, Callable]] = None,
    interval_symbol=",",
    reverse_symbol="~",
):
    class _Action(argparse.Action):
        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[Text, Sequence[Any], None],
            option_string: Optional[Text],
        ) -> None:
            sorter = Sorter(
                values,
                field_scope=field_scope,
                field_extractors=field_extractors,
                field_converters=field_converters,
                interval_symbol=interval_symbol,
                reverse_symbol=reverse_symbol,
            )

            if not hasattr(namespace, "sorters"):
                setattr(namespace, "sorters", {})

            namespace.sorters[self.dest] = sorter

            if not hasattr(namespace, "sorter_regulars"):
                setattr(namespace, "sorter_regulars", [])

            namespace.sorter_regulars.append(values)

    return _Action


def displayer_action(
    *,
    field_scope: List[str] = None,
    field_extractors: Optional[Dict[str, Callable]] = None,
    interval_symbol=",",
    mode="table",
    displayer_kwargs: dict = None,
):
    class _Action(argparse.Action):
        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[Text, Sequence[Any], None],
            option_string: Optional[Text],
        ) -> None:
            displayer = Displayer(
                values,
                field_scope=field_scope,
                field_extractors=field_extractors,
                interval_symbol=interval_symbol,
                mode=mode,
                displayer_kwargs=displayer_kwargs,
            )

            if not hasattr(namespace, "displayers"):
                setattr(namespace, "displayers", {})

            namespace.displayers[self.dest] = displayer

    return _Action


def merge_filters(filters: dict):
    filter_list = []
    for k, filter in filters.items():
        if k == "default" and len(filters) != 1:
            continue
        filter_list.append(filter)

    if not filter_list:
        return lambda x: True

    return lambda x: all(f(x) for f in filter_list)


def read_regulars(regulars, extractors: Optional[Dict[str, Callable]] = None):
    filters = [Filter(regular, field_extractors=extractors) for regular in regulars]
    if not filters:
        return lambda x: True
    return lambda x: all(f(x) for f in filters)
