"""
Author       : zhangxianbing
Date         : 2021-06-02 14:32:13
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-06-17 15:24:10
"""
import json
import logging
import os
import re
import uuid
from collections import defaultdict
from functools import partial
from io import FileIO
from typing import Any, Callable, Dict, Pattern

from pyclier.utils import sanitize_filepath
from ..utils import get_now

log = logging.getLogger(__name__)

RAND = "rand"
IDX = "index"
TIME = "time"
ITIME = "itime"

NAMING_STYLES = {
    RAND: "use random uuid code as filename",
    IDX: "use index as filename",
    TIME: "use datatime str as filename",
    ITIME: "use index+time as filename",
}


def naming_patterns(*, prefix: str = "", suffix: str = "") -> Dict[str, Pattern]:
    return {
        RAND: re.compile(
            fr"^{prefix}([a-f0-9]{{8}}-?[a-f0-9]{{4}}-?4[a-f0-9]{{3}}-?[89ab][a-f0-9]{{3}}-?[a-f0-9]{{12}}){suffix}$"
        ),
        IDX: re.compile(fr"^{prefix}(\d+){suffix}$"),
        TIME: re.compile(
            fr"^{prefix}(\d{{4}}-\d\d-\d\dT\d\d[:-]\d\d[:-]\d\dZ){suffix}$"
        ),
        ITIME: re.compile(
            fr"^{prefix}(\d+)-(\d{{4}}-\d\d-\d\dT\d\d[:-]\d\d[:-]\d\dZ){suffix}$"
        ),
    }


class Persister:
    def __init__(
        self,
        root,
        dump=lambda v, f: f.write(str(v)),
        file_type="txt",
        compressed=False,
        *,
        naming_style="index",  # index, time
        append_timestamp_to_root=True,
    ):
        if append_timestamp_to_root:
            root = os.path.join(root, sanitize_filepath(get_now()))
        self.root = root
        print(self.root)

        self.compressed = compressed
        self.file_type = file_type
        self.dump: Callable[[Any, FileIO]] = dump

        if naming_style not in NAMING_STYLES:
            raise ValueError(
                f"{naming_style} not in supported naming styles: {NAMING_STYLES}"
            )
        self.naming_style = naming_style

        self.file_handles: Dict[tuple, FileIO] = {}
        self.counter = defaultdict(int)

    def __call__(self, key: tuple, value):
        return self.persist(key, value)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.close()

    def open(self):
        os.makedirs(self.root, exist_ok=True)

    def close(self):
        for f in self.file_handles.values():
            if f:
                f.close()

    def get_count(self, key):
        return self.counter[key]

    def persist(self, key: tuple, value):
        if self.compressed:
            sanitize_key = tuple(map(sanitize_filepath, key))
            path = os.path.join(self.root, f'{"-".join(sanitize_key)}.{self.file_type}')
            if self.file_handles.get(key) is None:
                self.file_handles[key] = open(path, "a")
            self.dump(value, self.file_handles[key])
            self.file_handles[key].write("\n")

        else:
            sanitize_key = tuple(map(sanitize_filepath, key))
            outdir = os.path.join(self.root, *sanitize_key)
            os.makedirs(outdir, exist_ok=True)
            if self.naming_style == RAND:
                filename = f"{uuid.uuid4()}.{self.file_type}"
            elif self.naming_style == IDX:
                filename = f"{self.counter[key]}.{self.file_type}"
            elif self.naming_style == TIME:
                filename = f"{get_now()}.{self.file_type}"
            elif self.naming_style == ITIME:
                filename = f"{self.counter[key]}-{get_now()}.{self.file_type}"
            else:
                filename = f"{uuid.uuid4()}.{self.file_type}"

            filename = sanitize_filepath(filename)
            path = os.path.join(outdir, filename)
            with open(path, "w") as f:
                self.dump(value, f)

        self.counter[key] += 1

        return path, self.counter[key]


class JsonPersister(Persister):
    def __init__(self, root, compressed=False, **kwargs):
        if compressed:
            dump = json.dump
        else:
            dump = partial(json.dump, indent=4)
        super().__init__(root, dump, "json", compressed, **kwargs)


if __name__ == "__main__":
    pats = naming_patterns(suffix=".json")

    s = f"{str(uuid.uuid4())}.json"
    print(s)
    print(pats[RAND].match(s).groups())

    now = f"{get_now()}.json"
    print(now)
    print(pats[TIME].match(now).groups())

    print(pats[ITIME].match(f"1-{now}").groups())
