"""
Author       : zhangxianbing
Date         : 2021-05-26 08:59:38
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-26 14:14:31
"""
import argparse
import logging
import sys
from typing import NoReturn, Text, Tuple

log = logging.getLogger(__name__)


class ArgumentParserError(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: Text) -> NoReturn:
        raise ArgumentParserError(message)


class SmartHelpFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        lines = text.splitlines() if "\n" in text else [text]
        wrap_lines = []
        for each_line in lines:
            wrap_lines.extend(super()._split_lines(each_line, width))
        return wrap_lines


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, SmartHelpFormatter):
    pass


class Command:
    _parser: ArgumentParser
    _subparsers: argparse._SubParsersAction

    def __init__(self, name, **kwargs):
        self.name = name

        self.help = kwargs.pop("help", None)
        self.func = kwargs.pop("func", None)
        self.require_args = kwargs.pop("require_args", False)

        self._parser = ArgumentParser(
            prog=self.name, formatter_class=CustomFormatter, **kwargs
        )
        self._subparsers = None

        if self.func:
            self.set_func(self.func)

        self.set_defaults(require_args=self.require_args)

    # interface compatible with argparse.ArgumentParser

    def set_defaults(self, **kwargs):
        self._parser.set_defaults(**kwargs)

    def add_argument(self, *args, **kwargs):
        self._parser.add_argument(*args, **kwargs)

    def add_parser(self, parser: ArgumentParser, **kwargs):
        if self._subparsers is None:
            self._subparsers = self._parser.add_subparsers(title="Commands")
        kwargs.pop("parents", None)
        add_help = kwargs.pop("add_help", False)
        self._subparsers.add_parser(
            parser.prog, parents=[parser], add_help=add_help, **kwargs
        )

    # simplified custom interface

    def set_func(self, func):
        self.set_defaults(func=func)

    def add_sub(self, command: "Command"):
        self.add_parser(command._parser, help=command.help)

    def add(self, *args, **kwargs):
        self.add_argument(*args, **kwargs)

    # executor method

    def run(self):
        # parser argument and execute
        subparser, idx = find_cmd(self._parser, 0)

        try:
            args = self._parser.parse_args()
        except ArgumentParserError as err:
            log.error(f"{err}\n")
            if subparser:

                subparser.print_help()
            else:
                self._parser.print_help()
            sys.exit(2)

        if not hasattr(args, "func"):
            self._parser.print_help()
        elif args.require_args and idx + 1 == len(sys.argv):
            subparser.print_help()
        else:
            args.func(args)


def find_cmd(parser: ArgumentParser, idx: int) -> Tuple[ArgumentParser, int]:
    remainder_argv = sys.argv[idx + 1 :]
    if (
        remainder_argv
        and parser
        and parser._subparsers
        and parser._subparsers._group_actions
    ):
        for action in parser._subparsers._group_actions:
            action: argparse._SubParsersAction
            for k, v in action._name_parser_map.items():
                if k in remainder_argv:
                    return find_cmd(v, sys.argv.index(k))
    return parser, idx
