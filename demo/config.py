import logging.config
import os
from enum import Enum
from typing import Optional

import appdirs
from pyclier import LDMixin, load_conf_parser

log = logging.getLogger(__name__)

# ======================   Config file locations   ====================== #

CONFIG_DIRS = [
    appdirs.user_config_dir("demo"),
    os.path.join("$DEMO_HOME", "conf"),
    "$DEMO_CONF_DIR",
    os.path.join(os.curdir, "conf"),
]


# ======================   Config class definition   ====================== #


from typing import List


class Config1(LDMixin):
    number_type: int
    string_type: str


class Object(LDMixin):
    attr1: str
    attr2: int


class DictType(LDMixin):
    object1: Object
    object2: Object


class EnumType(Enum):
    JAVA = "JAVA"
    PYTHON = "PYTHON"
    CPP = "CPP"


class Config2(LDMixin):
    list_type: List[str]
    enum_type: List[EnumType]
    dict_type: DictType


class Config(LDMixin):
    config1: Config1
    config2: Config2


# ======================   Config   ====================== #

# global config
_conf: Optional[Config] = None


def set_conf(d: dict):
    global _conf
    _conf = Config.from_dict(d)


def get_conf():
    global _conf
    if _conf is None:
        _conf = Config()
    return _conf


conf_parser = load_conf_parser(set_conf, CONFIG_DIRS)
