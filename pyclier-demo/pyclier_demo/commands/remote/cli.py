import logging

from pyclier_demo.utils import demo_func
from pyclier import Command

from .commands import add, rename

log = logging.getLogger(__name__)


cmd = Command("remote", func=demo_func)
cmd.add_sub(add.cmd)
cmd.add_sub(rename.cmd)
