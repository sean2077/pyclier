import logging

from pyclier import Command

from . import __version__, prog_name
from .config import conf_parser, get_conf

log = logging.getLogger(__name__)


def gen_cmd(name, **kwargs):
    def func(args):
        print(f"running {name} command")

    return Command(name, help=f"{name} command", func=func, **kwargs)


def cmd_func(args):
    conf = get_conf()
    log.info(conf)


def main():
    cmd = Command(prog_name, func=cmd_func, parents=[conf_parser])
    cmd.add("-V", "--version", action="version", version=f"%(prog)s-{__version__}")

    cmd1 = gen_cmd("cmd1")
    cmd2 = gen_cmd("cmd2")
    cmd3 = gen_cmd("cmd3")

    cmd1_1 = gen_cmd("cmd1_1", require_args=True)
    cmd1_1.add("-a", help="a options")
    cmd1_2 = gen_cmd("cmd1_2")

    # cmd1 should add its subcmds before it was added by cmd
    cmd1.add_sub(cmd1_1)
    cmd1.add_sub(cmd1_2)

    cmd.add_sub(cmd1)
    cmd.add_sub(cmd2)
    cmd.add_sub(cmd3)

    cmd.run()

    log.info(cmd._args)


if __name__ == "__main__":
    main()
