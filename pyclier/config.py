"""
Author       : zhangxianbing
Date         : 2021-05-26 16:50:32
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-28 22:39:45
"""
import logging
import logging.config
import os
from typing import Callable, List, Tuple

from ._argparse import ArgumentParser
from .utils import expand_path, load_json, load_yaml

log = logging.getLogger(__name__)

# Only supporting yaml and json format config file, and the yaml file is recommended.
SUPPORTED_FORMATS = ("yml", "yaml", "json")
DEFAULT_CONF_NAME = "config"
DEFAULT_LOG_CONF_NAME = "logging"


def load_conf_parser(
    global_conf_setter: Callable[[dict], None],
    conf_dirs: List[str],
    formats: Tuple[str, ...] = SUPPORTED_FORMATS,
    conf_name: str = DEFAULT_CONF_NAME,
    log_conf_name: str = DEFAULT_LOG_CONF_NAME,
) -> ArgumentParser:
    """parses and sets up the command line argument system above with config file parsing.

    Args:
        global_conf_setter (Callable[[dict], None]): method that sets the global config instance
        conf_dirs (List[str]): directories of config files, support pattern `~` (meaning root) and `$ENVIRONMENT_VARIABLE`
        formats (Tuple[str, ...], optional): supported config file formats. Defaults to ("yml", "yaml", "json").
        conf_name (str, optional): basename of config file. Defaults to "config".
        log_conf_name (str, optional): basename of logging config file. Defaults to "logging".

    Returns:
        ArgumentParser: returned parser
    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "-c",
        "--conf-dir",
        help=f"Directory of configuration files (logging.yml, config.yml).\nPriority: file specified by option \"-c\" > {' > '.join(reversed(conf_dirs))}\n",
        default=None,
    )

    args, remainder_argv = parser.parse_known_args()
    if args.conf_dir:
        conf_dirs.insert(0, args.conf_dir)

    conf_dirs = list(map(expand_path, conf_dirs))

    # Load configuration
    # first load logging config file
    load_conf(logging.config.dictConfig, conf_dirs, formats, log_conf_name)

    # then load config file
    load_conf(global_conf_setter, conf_dirs, formats, conf_name)

    return parser


def load_conf(
    global_conf_setter: Callable[[dict], None],
    conf_dirs: List[str],
    formats: Tuple[str, ...],
    conf_name: str,
):
    """load config file and set global config instance

    Args:
        global_conf_setter (Callable[[dict], None]): method that sets the global config instance
        conf_dirs (List[str]): directory of config files
        formats (Tuple[str, ...]): supported config file formats.
        conf_name (str): basename of config file.
    """
    conf_locations = [
        os.path.join(d, f"{conf_name}.{f}")
        for f in formats
        for d in reversed(conf_dirs)
    ]
    for conf_path in conf_locations:
        if os.path.exists(conf_path):
            try:
                dict_conf = {}
                if conf_path.endswith(".yml"):
                    dict_conf = load_yaml(conf_path)
                elif conf_path.endswith(".json"):
                    dict_conf = load_json(conf_path)
                global_conf_setter(dict_conf)
                log.info(f"Loaded {conf_name} from {conf_path}")
            except Exception as err:
                log.error(err)
                continue
            break


def load_general_conf(global_conf_loader, conf_files):
    real_conf_paths = list(map(expand_path, conf_files))
    for conf_file in reversed((real_conf_paths)):
        try:
            global_conf_loader(conf_file)
        except Exception as e:
            log.error(e)
            continue
        break
