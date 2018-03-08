#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
import re
from functools import reduce
# from collections import deque
from lisp_repl import repl
from lisp_globals import lisp_env

ENV = lisp_env()
# LOCAL_ENV = {}
LAMBDA_ENV = {}
# KEY_WORDS = ['define', 'if', 'quote', 'set!', 'lambda']


def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t":
        return True, lisp_str[2:]
    if lisp_str[:2] == "#f":
        return False, lisp_str[2:]
    return None

def number_parser(lisp_str):
    re_number = re.match(r'^\s*[+-]?\d+\.?\d*', lisp_str)
    if re_number:
        number, lisp_str = re_number.group(), lisp_str[re_number.end():].strip()
    else:
        return None
    try:
        parsed_num = int(number) or float(number)
    except ValueError:
        parsed_num = float(number)
    return parsed_num, lisp_str

def symbol_parser(lisp_str):
    re_symbol = re.match(r'^\s*\w+|[+-/*%]?\s*', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group().strip(), lisp_str[re_symbol.end():]
    else:
        return None
    if symbol in ENV:
        return ENV[symbol], lisp_str
    # elif symbol in LOCAL_ENV:
    #     return LOCAL_ENV[symbol], lisp_str
    # elif symbol in LAMBDA_ENV:
        # return LAMBDA_ENV[symbol], lisp_str
    return None


def define_parser(lisp_str):
    re_define = re.match(r'^\(?\s*define\s*', lisp_str)
    if re_define:
        lisp_str = lisp_str[re_define.end():]
    re_variable = re.match(r'^\s*\w+\s*', lisp_str)
    if re_variable:
        variable, lisp_str = re_variable.group().strip(), lisp_str[re_variable.end():].strip()
    else:
        return None
    parsed_number = number_parser(lisp_str)
    if parsed_number:
        ENV[variable], lisp_str = parsed_number
        # lisp_str = lisp_str.replace(variable, str(ENV[variable]))

    exp_parsed = lisp_interpreter(lisp_str)
    if exp_parsed:
        ENV[variable] = exp_parsed
        # lisp_str = lisp_str.replace(variable, str(ENV[variable]))
        return lisp_str

    parsed_lambda = lambda_parser(lisp_str)
    if parsed_lambda:
        LAMBDA_ENV[variable] = parsed_lambda
    # print(lisp_str)
    return lisp_str

def lambda_parser(lisp_str):
    re_lambda = re.match(r'^\s*\(?\s*lambda\s*', lisp_str)
    if re_lambda:
        lisp_str = lisp_str[re_lambda.end():]
    else:
        return None

    re_larg = re.match(r'^\s*\(\s*\w+\)\s*', lisp_str)
    if re_larg:
        larg, lisp_str = re_larg.group().strip()[1:-1], lisp_str[re_larg.end():]
    else:
        return None

    re_lbody = re.match(r'^\s*\(\s*.*?\s*\)\s*', lisp_str)
    if re_lbody:
        lbody, lisp_str = re_lbody.group().strip()[1:-1], lisp_str[re_lbody.end():]
        parsed_lbody = input_parser(lbody)[0]
        # LOCAL_ENV[variable] = parsed_body
        # return lisp_str
        return larg, parsed_lbody
    return None

def if_parser(lisp_str):
    pass


# def define_expression(parsed_list):
#     if parsed_list[0] in ENV.values():
#         procedure = parsed_list.pop(0)
#         pargs = []
#     for parg  in parsed_list:
#         if isinstance(parg, list):
#             pargs.append(evaluator(parg))
#         else:
#             pargs.append(parg)
#     return reduce(procedure, pargs)

def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    exp_list = []
    sub_parsers = [bool_parser, number_parser, symbol_parser, ]
    for sub_parser in sub_parsers:
        if sub_parser(lisp_str):
            parsed, lisp_str = sub_parser(lisp_str)
            exp_list.append(parsed)

    if lisp_str[0] == '(':
        nested_exp = input_parser(lisp_str)
        parsed, lisp_str = nested_exp[0], nested_exp[1]
        exp_list.append(parsed)

    if lisp_str and lisp_str[0] == ")":
        lisp_str = lisp_str[1:]
    return exp_list, lisp_str

def input_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[0] == "(":
        lisp_str = lisp_str[1:]
    else:
        return None
    parsed_lists = []
    while expression_parser(lisp_str):
        expression_parsed, lisp_str = expression_parser(lisp_str)
        parsed_lists.extend(expression_parsed)
    # print(parsed_lists, lisp_str)
    return parsed_lists, lisp_str

def lisp_interpreter(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    if lisp_str in ENV:
        print(ENV[lisp_str])
        return None
    if define_parser(lisp_str):
        lisp_str = define_parser(lisp_str)
    lisp_parsed = input_parser(lisp_str)
    if lisp_parsed and lisp_parsed[0]:
        parsed, _ = input_parser(lisp_str)
        return evaluator(parsed)  # evaluating
    return None

def evaluator(parsed_lists):
    procedure = parsed_lists.pop(0)
    pargs = []
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
            lisp_interpreter(repl())
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
        os.sys.exit()
        print("\nInput error\n")

if __name__ == '__main__':
    main()
