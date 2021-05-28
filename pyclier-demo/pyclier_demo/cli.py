import logging

from pyclier import Command

from . import __version__, prog_name
from .commands.remote import cli as remote_cli
from .config import get_conf
from .utils import demo_func

log = logging.getLogger(__name__)


cmd = Command(prog_name, func=demo_func)
cmd.add("-V", "--version", action="version", version=f"%(prog)s-{__version__}")

cmd.add_sub(remote_cli.cmd)


def main():
    cmd.run()


if __name__ == "__main__":
    main()
