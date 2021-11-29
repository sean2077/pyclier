"""
Author       : zhangxianbing
Date         : 2021-05-26 08:59:38
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-30 11:49:42
"""
import argparse
import logging
from typing import NoReturn, Text

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
