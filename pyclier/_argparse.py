"""
Author       : zhangxianbing
Date         : 2021-05-26 08:59:38
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-28 14:49:30
"""
import argparse
import logging
import sys
from typing import NoReturn, Text, Tuple

import argcomplete

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
    parser: ArgumentParser
    subparsers: argparse._SubParsersAction

    _final_parser: ArgumentParser
    _idx: int
    _args: argparse.Namespace

    def __init__(self, name, **kwargs):
        self.name = name

        self.help = kwargs.pop("help", None)
        self.func = kwargs.pop("func", None)
        self.require_args = kwargs.pop("require_args", False)

        self.parser = ArgumentParser(
            prog=self.name, formatter_class=CustomFormatter, **kwargs
        )
        self.subparsers = None

        self._args = None

        if self.func:
            self.set_func(self.func)

        self.set_defaults(require_args=self.require_args)

    # interface compatible with argparse.ArgumentParser

    def set_defaults(self, **kwargs):
        self.parser.set_defaults(**kwargs)

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def add_parser(self, parser: ArgumentParser, **kwargs):
        if self.subparsers is None:
            self.subparsers = self.parser.add_subparsers(title="Commands")
        kwargs.pop("parents", None)
        add_help = kwargs.pop("add_help", False)
        self.subparsers.add_parser(
            parser.prog, parents=[parser], add_help=add_help, **kwargs
        )

    def parse_args(self):
        if self._args:
            return self._args

        subparser, idx = find_cmd(self.parser, 0)
        self.set_defaults(_prog=subparser.prog)

        try:
            args = self.parser.parse_args()
        except ArgumentParserError as err:
            log.error(f"{err}\n")
            if subparser:
                subparser.print_help()
            else:
                self.parser.print_help()
            sys.exit(2)

        self._final_parser = subparser
        self._idx = idx
        self._args = args

        return args

    # simplified custom interface

    def set_func(self, func):
        self.set_defaults(func=func)

    def add_sub(self, command: "Command"):
        self.add_parser(command.parser, help=command.help)

    def add(self, *args, **kwargs):
        self.add_argument(*args, **kwargs)

    # executor method

    def run(self):
        "parser argument and execute"

        # for autocomplete
        argcomplete.autocomplete(self.parser)

        if not self._args:
            args = self.parse_args()
        else:
            args = self._args

        if not hasattr(args, "func"):
            self.parser.print_help()
        elif args.require_args and self._idx + 1 == len(sys.argv):
            self._final_parser.print_help()
        else:
            args.func(args)


def find_cmd(parser: ArgumentParser, idx: int) -> Tuple[ArgumentParser, int]:
    remainder_argv = sys.argv[idx + 1 :]
    if remainder_argv and parser:
        if parser._subparsers and parser._subparsers._group_actions:
            actions = parser._subparsers._group_actions
        else:
            actions = parser._actions
        for action in actions:
            action: argparse._SubParsersAction
            if hasattr(action, "_name_parser_map"):
                for k, v in action._name_parser_map.items():
                    if k in remainder_argv:
                        return find_cmd(v, sys.argv.index(k))

    return parser, idx
