import logging
from argparse import Namespace

log = logging.getLogger(__name__)


def demo_func(args: Namespace):
    """test command function

    Args:
        args ([type]): [description]
    """
    log.info(f"running cmd: {args._prog} | args: {args}")
