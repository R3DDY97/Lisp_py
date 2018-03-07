#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
import re
from functools import reduce
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
            number = int(number)
    except ValueError:
        number = float(number)
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
    elif symbol in LOCAL_ENV:
        pass
    elif symbol in KEY_WORDS:
        pass
    return None

def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    sub_parsers = [bool_parser, number_parser, symbol_parser]
    exp_list = []
    while lisp_str[0] != ')':
        if lisp_str[0] == '(':
            new_exp = []
            return new_exp.append(expression_parser(lisp_str[1:]))
        for sub_parser in sub_parsers:
            if sub_parser(lisp_str):
                parsed, lisp_str = sub_parser(lisp_str)
                exp_list.append(parsed)
        return exp_list, lisp_str

def input_parser(lisp_str):
    # lisp_str = lisp_str.strip()
    #     lisp_str = lisp_str[1:]
    # else:
    #     print("\nsyntax error\n")
    #     os.sys.exit()
    # while lisp_str:

    if expression_parser(lisp_str):
        # expression_parsed, lisp_str = expression_parser(lisp_str)
        # parsed_list.append(expression_parsed)
        print(expression_parser(lisp_str))
    return expression_parser(lisp_str)
    #     print(parsed_list, lisp_str)
    # return parsed_list, lisp_str

    # if not lisp_str and parsed_list:
    #     evaluator(parsed_list)
#
# def evaluator(parsed_list):
#     if parsed_list[0] in ENV:
#         procedure = parsed_list.pop(0)
#         pargs = []
#     if not parsed_list:
#         return None
#     for parg in parsed_list:
#         if isinstance(parsed_list, list):
#             pargs.append(evaluator(parg))
#         else:
#             pargs.append(parg)
#     print(reduce(procedure, pargs))
#     return reduce(procedure, pargs)

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
