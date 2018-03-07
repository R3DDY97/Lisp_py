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
        parsed_num = int(number) or float(number)
    except ValueError:
        parsed_num = float(number)
    return parsed_num, lisp_str

def symbol_parser(lisp_str):
    lisp_str = lisp_str.strip()
    re_symbol = re.match(r'^(\w+|[+-/*%]?\s)', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group().strip(), lisp_str[re_symbol.end():].strip()
    else:
        return None
    if symbol in ENV:
        return ENV[symbol], lisp_str
    elif symbol in LOCAL_ENV:
        pass
    elif symbol in KEY_WORDS:
        return symbol, lisp_str
    return None

def keyword_parser(keyword, lisp_str):
    if keyword == 'define':



def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    exp_list = []
    if lisp_str[0] == '(':
        nested_exp = input_parser(lisp_str)
        parsed, lisp_str = nested_exp[0], nested_exp[1]
        exp_list.append(parsed)

    sub_parsers = [bool_parser, number_parser, symbol_parser]
    for sub_parser in sub_parsers:
        if sub_parser(lisp_str):
            parsed, lisp_str = sub_parser(lisp_str)
            exp_list.append(parsed)
    if lisp_str and lisp_str[0] == ")":
        return exp_list, lisp_str[1:]
    return exp_list, lisp_str

def input_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[0] == "(":
        parsed_list = []
        lisp_str = lisp_str[1:]
    else:
        print("\nsyntax error\n")
        os.sys.exit()

    while expression_parser(lisp_str):
        expression_parsed, lisp_str = expression_parser(lisp_str)
        parsed_list.extend(expression_parsed)
    return parsed_list, lisp_str

def evaluator(parsed_list):
    if not isinstance(parsed_list, list):
        return None
    if parsed_list[0] in ENV.values():
        procedure = parsed_list.pop(0)
        pargs = []
    for parg  in parsed_list:
        if isinstance(parg, list):
            pargs.append(evaluator(parg))
        else:
            pargs.append(parg)
    print(reduce(procedure, pargs))
    return reduce(procedure, pargs)

def main():
    try:
        os.system("clear||cls")
        while True:
            evaluator(input_parser(repl())[0])
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
        os.sys.exit()
        print("\nInput error\n")

if __name__ == '__main__':
    main()
