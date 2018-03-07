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
    re_number = re.match(r'^[+-]?\d+\.?\d*', lisp_str)
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
        return LOCAL_ENV[symbol], lisp_str
    return None

def keyword_parser(lisp_str):
    lisp_str = lisp_str.strip()
    re_keyword = re.match(r'^define|lambda|if', lisp_str)
    if re_keyword:
        keyword, lisp_str = re_keyword.group(), lisp_str[re_keyword.end():].strip()
        # print(keyword)
    else:
        return None

    re_variable = re.match(r'^\w+', lisp_str)
    if keyword == 'define' and re_variable:
        variable, lisp_str = re_variable.group(), lisp_str[re_variable.end():]
    if number_parser(lisp_str):
        LOCAL_ENV[variable], lisp_str = number_parser(lisp_str)
        next_exp = lisp_str.index("(")+1
        lisp_str = lisp_str[next_exp:].replace(variable, str(LOCAL_ENV[variable]))
        print(lisp_str)
        return lisp_str

    elif keyword == 'lambda':
        pass
    return None


def arthmetic_eval(parsed_list):
    if parsed_list[0] in ENV.values():
        procedure = parsed_list.pop(0)
        pargs = []
    for parg  in parsed_list:
        if isinstance(parg, list):
            pargs.append(evaluator(parg))
        else:
            pargs.append(parg)
    return reduce(procedure, pargs)

def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None

    exp_list = []
    if lisp_str[0] == '(':
        nested_exp = input_parser(lisp_str[1:])
        parsed, lisp_str = nested_exp[0], nested_exp[1]
        exp_list.append(parsed)

    sub_parsers = [bool_parser, number_parser, symbol_parser, ]
    for sub_parser in sub_parsers:
        if sub_parser(lisp_str):
            parsed, lisp_str = sub_parser(lisp_str)
            exp_list.append(parsed)

    if lisp_str and lisp_str[0] == ")":
        return exp_list, lisp_str[1:]

    print(exp_list, lisp_str)
    return exp_list, lisp_str

def input_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[0] == "(":
        lisp_str = lisp_str[1:]
    else:
        print("\nsyntax error\n")
        os.sys.exit()

    parsed_lists = []
    if keyword_parser(lisp_str):
        lisp_str = keyword_parser(lisp_str)

    while expression_parser(lisp_str):
        expression_parsed, lisp_str = expression_parser(lisp_str)
        parsed_lists.extend(expression_parsed)
    print(parsed_lists, lisp_str)
    return parsed_lists, lisp_str

def evaluator(parsed_lists):
    # for parsed_list in parsed_lists:
    if parsed_lists:
        procedure = parsed_lists.pop(0)
        pargs = []
    else:
        return None
    for parg  in parsed_lists:
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
