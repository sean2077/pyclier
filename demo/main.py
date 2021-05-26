import logging

from config import conf_parser, get_conf
from pyclier import Command

log = logging.getLogger(__name__)


def gen_cmd(name):
    def func(args):
        print(f"running {name} command")

    return Command(name, help=f"{name} command", func=func)


def cmd_func(args):
    conf = get_conf()
    log.info(conf)
    log.info(args)


def main():
    cmd = Command("demo", func=cmd_func, parents=[conf_parser])
    cmd.add("-V", "--version", action="version", version=f"%(prog)s-0.0.1")

    cmd1 = gen_cmd("cmd1")
    cmd2 = gen_cmd("cmd2")
    cmd3 = gen_cmd("cmd3")

    cmd1_1 = gen_cmd("cmd1_1")
    cmd1_1.add("-a", help="a options")
    cmd1_2 = gen_cmd("cmd1_2")

    # cmd1 should add its subcmds before it was added by cmd
    cmd1.add_sub(cmd1_1)
    cmd1.add_sub(cmd1_2)

    cmd.add_sub(cmd1)
    cmd.add_sub(cmd2)
    cmd.add_sub(cmd3)

    cmd.run()


if __name__ == "__main__":
    main()
