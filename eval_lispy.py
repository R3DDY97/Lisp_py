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
# LAMBDA_ENV = {}
# KEY_WORDS = ['define', 'if', 'quote', 'set!', 'lambda']

Symbol = str              # A Scheme Symbol is implemented as a Python str
Number = (int, float)     # A Scheme Number is implemented as a Python int or float
Atom = (Symbol, Number) # A Scheme Atom is a Symbol or Number
List = list             # A Scheme List is implemented as a Python list
Exp = (Atom, List)     # A Scheme expression is an Atom or List
# ENV = dict             # A Scheme environment (defined below)
                          # is a mapping of {variable: value}

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body):
        self.parms, self.body = parms, body
    def __call__(self, *args):
        LOCAL_ENV[self.parms] = args
        return lisp_evaluator(self.body)



def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t":
        return True, lisp_str[2:]
    if lisp_str[:2] == "#f":
        return False, lisp_str[2:]
    return None


def symbol_parser(lisp_str):
    re_symbol = re.match(r'^\s*\w+|[><+-/*%]?\s*', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group().strip(), lisp_str[re_symbol.end():]
        # return re_symbol.group().strip(), lisp_str[re_symbol.end():].strip()
    else:
        return None
    try:
        symbol = float(symbol)
    except ValueError:
        pass
    return symbol, lisp_str


def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    exp_list = []
    sub_parsers = [bool_parser, symbol_parser, ]
    # sub_parsers = [bool_parser, number_parser, symbol_parser, ]
    for sub_parser in sub_parsers:
        sub_parsed = sub_parser(lisp_str)
        if sub_parsed and sub_parsed[0]:
            parsed, lisp_str = sub_parsed
            # parsed, lisp_str = sub_parser(lisp_str)
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
    lisp_parsed = input_parser(lisp_str)
    if lisp_parsed and lisp_parsed[0]:
        parsed, _ = input_parser(lisp_str)
        # print(parsed)
        return parsed
    return None


def get_value(key):
    try:
        if key in ENV:
            return ENV[key]
    except KeyError:
        return LOCAL_ENV[key]
        # pass

def lisp_evaluator(parsed):
    if not parsed:
        return None
    # for parsed in parsed_lists:
    if isinstance(parsed, Number):
        # print(parsed)
        return parsed
    # if parsed in LOCAL_ENV:
    #     return LOCAL_ENV[parsed]
    if isinstance(parsed, str):
        return get_value(parsed)
        # return None
    # if isinstance(parsed, list):

    #     return lisp_evaluator(parsed)
    if len(parsed) == 1:
        return lisp_evaluator(parsed[0])

    operation, *arguments = parsed
    if operation == 'define':
        variable, exp = arguments
        print(arguments)
        LOCAL_ENV[variable] = lisp_evaluator(exp)
    if operation == 'if':
        test, conseq, alt = arguments
        return lisp_evaluator(conseq if lisp_evaluator(test) else alt)
    if operation == 'quote':
        return arguments[0]
    if operation == 'lambda':
        parameters, body = arguments
        return Procedure(parameters, body)

    proc = get_value(operation)
    if proc:
        vals = [lisp_evaluator(argument) for argument in arguments]
        # if len(vals) > 2:
        print(reduce(proc, vals))
        return reduce(proc, vals)
    return None
    # print(proc(*vals))
    # return proc(*vals)


def main():
    try:
        os.system("clear||cls")
        while True:
            lisp_evaluator(lisp_interpreter(repl()))
            # lisp_interpreter(repl())
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
        os.sys.exit()
        print("\nInput error\n")

if __name__ == '__main__':
    main()
