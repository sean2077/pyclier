"""
Author       : zhangxianbing
Date         : 2021-05-24 19:20:27
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-26 09:51:08
"""
import codecs
import json
import sys
from typing import Any, Dict, List

import yaml


class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        value = self.func(instance)
        setattr(instance, self.func.__name__, value)
        return value


class LoadMixin:
    @staticmethod
    def _load(type_, name, value, cls, **kwargs) -> Any:
        # * forward reference type
        if isinstance(type_, str):
            type_ = sys.modules[cls.__module__].__dict__.get(type_)
        if hasattr(type_, "__forward_arg__"):
            type_ = sys.modules[cls.__module__].__dict__.get(type_.__forward_arg__)

        # * specified generic type
        if not hasattr(type_, "__origin__"):
            if value is None:
                return type_()  # default value of type

            if issubclass(type_, LoadMixin):
                return type_.from_dict(value, **kwargs)

            return value

        # * __origin__ keeps a reference to a type that was subscribed,
        #   e.g., Union[T, int].__origin__ == Union;`
        o_type = type_.__origin__
        g_type = type_.__args__

        if o_type in (list, List):
            if value is None:
                return []
            return [
                LoadMixin._load(g_type[0], f"{name}.{i}", v, cls, **kwargs)
                for i, v in enumerate(value)
            ]

        if o_type in (dict, Dict):
            if value is None:
                return {}
            return {
                k: LoadMixin._load(g_type[0], f"{name}.{k}", v, cls, **kwargs)
                for k, v in value.items()
            }

        raise RuntimeError(f"This generics is not supported `{o_type}`")

    @classmethod
    def from_dict(cls, d: dict, **kwargs):
        if isinstance(d, cls):
            return d

        instance = cls()

        for n, t in cls.__annotations__.items():
            arg_v = d.get(n)
            def_v = getattr(instance, n, None)
            setattr(instance, n, LoadMixin._load(t, n, arg_v or def_v, cls, **kwargs))

        return instance

    @classmethod
    def from_json(cls, s: str, **kwargs):
        return cls.from_dict(json.loads(s), **kwargs)

    @classmethod
    def from_jsonf(cls, fpath: str, **kwargs):
        with codecs.open(fpath, mode="r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f), **kwargs)

    @classmethod
    def from_yamlf(cls, fpath: str, **kwargs):
        with codecs.open(fpath, mode="r", encoding="utf-8") as f:
            return cls.from_dict(yaml.safe_load(f), **kwargs)


class DumpMixin:
    @staticmethod
    def _dump(value, **kwargs):

        if isinstance(value, DumpMixin):
            return value.to_dict(**kwargs)

        if isinstance(value, list):
            return [DumpMixin._dump(i, **kwargs) for i in value]

        if isinstance(value, dict):
            # filtering `__` prefix variable
            return {
                k: DumpMixin._dump(v, **kwargs)
                for k, v in value.items()
                if not k.startswith("__")
            }

        return value

    def to_dict(self, **kwargs) -> dict:
        return DumpMixin._dump(self.__dict__, **kwargs)

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(**kwargs))

    def to_pretty_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(**kwargs), indent=4)

    def to_jsonf(self, fpath: str, **kwargs):
        with codecs.open(fpath, mode="w", encoding="utf-8") as f:
            json.dump(self.to_dict(**kwargs), f)

    @LazyProperty
    def __pretty_json__repr__(self):
        return self.to_pretty_json()

    def __repr__(self):
        return self.__pretty_json__repr__


class LDMixin(LoadMixin, DumpMixin):
    pass
