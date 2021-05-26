import argparse
import logging
import logging.config
import os
from enum import Enum
from typing import Any, List, Optional, Sequence, Text, Union

import appdirs
from pyclier import ArgumentParser, LDMixin, load_json, load_yaml

log = logging.getLogger(__name__)

# ======================   Config file locations   ====================== #

# Only supporting yaml and json format config file, and the yaml file is recommended.
CONFIG_FILE = ("config.yml", "config.json")
LOG_CONF_FILE = ("logging.yml", "logging.json")
_CONFIG_DIRS = [
    appdirs.user_config_dir("demo"),
    os.path.join("$DEMO_HOME", "conf"),
    "$DEMO_CONF_DIR",
    os.path.join(os.curdir, "conf"),
]
CONFIG_DIRS = [os.path.expandvars(d) for d in _CONFIG_DIRS]


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


def load_conf():
    conf_locations = [
        os.path.join(d, fname) for fname in CONFIG_FILE for d in reversed(CONFIG_DIRS)
    ]
    for conf_path in conf_locations:
        if os.path.exists(conf_path):
            try:
                dict_conf = {}
                if conf_path.endswith(".yml"):
                    dict_conf = load_yaml(conf_path)
                elif conf_path.endswith(".json"):
                    dict_conf = load_json(conf_path)
                set_conf(dict_conf)
                log.info(f"Loaded config from {conf_path}")
            except Exception as err:
                log.error(err)
                continue
            break


def load_logging_conf():
    log_locations = [
        os.path.join(d, fname) for fname in LOG_CONF_FILE for d in reversed(CONFIG_DIRS)
    ]
    for log_conf_path in log_locations:
        if os.path.exists(log_conf_path):
            try:
                dict_conf = load_yaml(log_conf_path)
                logging.config.dictConfig(dict_conf)
                log.info(f"Loaded logging config from {log_conf_path}")
            except Exception as err:
                log.error(err)
                continue
            break


def _conf_parser():
    """parses and sets up the command line argument system above with config file parsing."""
    parser = ArgumentParser(add_help=False)

    class ConfDirAction(argparse.Action):
        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[Text, Sequence[Any], None],
            option_string: Optional[Text],
        ) -> None:
            CONFIG_DIRS.insert(0, values)

    parser.add_argument(
        "-c",
        "--conf-dir",
        help=f"Directory of configuration files (logging.yml, config.yml).\nPriority: {' > '.join(reversed(_CONFIG_DIRS))}\n",
        default=None,
        action=ConfDirAction,
    )

    args, remainder_argv = parser.parse_known_args()

    # Load logging configuration
    load_logging_conf()

    # Load configuration
    load_conf()

    return parser


conf_parser = _conf_parser()
