#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
import re
# from functools import reduce
# from collections import deque
from lisp_repl import repl
from lisp_globals import lisp_env

ENV = lisp_env()
LOCAL_ENV = {}
KEY_WORDS = ['define', 'if', 'quote', 'set!', 'lambda']


def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t" or lisp_str[:2] == "#t":
        return lisp_str[:2], lisp_str[2:]
    return None

def number_parser(lisp_str):
    lisp_str = lisp_str.strip()
    re_number = re.match(r'^[+-]?\d+\.?\d* ', lisp_str)
    if re_number:
        number, lisp_str = re_number.group(), lisp_str[re_number.end():]
    else:
        return None
    try:
        if isinstance(int(number), int):
            number = int(lisp_str)
    except ValueError:
        number = int(lisp_str)
    return number, lisp_str

def symbol_parser(lisp_str):
    lisp_str = lisp_str.strip()
    re_symbol = re.match(r'^(\w+|[+-/*%]?)', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group(), lisp_str[re_symbol.end():]
    else:
        return None
    if symbol in ENV:
        return ENV[symbol], lisp_str
    # elif symbol in KEY_WORDS:
    return None

def expression_parser(parsed_list, lisp_str):
    lisp_str = lisp_str.strip()


def input_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[0] == "(":
        parsed_list = []
    else:
        print("\nsyntax error\n")
        os.sys.exit()
    return expression_parser(parsed_list, lisp_str)

    # sub_parsers = [expression_parser, bool_parser, number_parser, symbol_parser, ]

    # while lisp_str:
    #     for sub_parser in sub_parsers:
    #         sub_parsed = sub_parser(lisp_str)
    #         if sub_parsed:
    #             parsed, lisp_str = sub_parsed
    #             parsed_list.append(parsed)




def main():
    try:
        os.system("clear||cls")
        while True:
            input_parser(repl())
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
        os.sys.exit()
        print("\nInput error\n")

if __name__ == '__main__':
    main()
