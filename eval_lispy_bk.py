#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
import re
from functools import reduce
# from collections import deque
from lisp_repl import repl
from lisp_globals import (lisp_env, eval_comparision)

OP_ENV, MATH_ENV = lisp_env()
LOCAL_ENV = {}
LAMBDA_ENV = {}
# KEY_WORDS = ['define', 'if', 'quote', 'set!', 'lambda']


def Procedure(params, body):
    "A user-defined Scheme procedure."
    def __init__(self, params, body):
        self.params, self.body = params, body
    def __call__(self, *args):
        LOCAL_ENV[self.params] = args
        return lisp_evaluator(self.body)

def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t" or lisp_str[:2] == "#f":
        return lisp_str[:2], lisp_str[2:].strip()

def symbol_parser(lisp_str):
    re_symbol = re.match(r'[^ \t\n\r\f\v()]+', lisp_str)
    # re_symbol = re.match(r'^\s*[+-]?[\w-]+|[><+-/*%]?\s*', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group().strip(), lisp_str[re_symbol.end():].strip()
    else:
        return None

    try:
        symbol = float(symbol)
    except ValueError:
        pass
    try:
        symbol = int(symbol)
    except ValueError:
        pass
    return symbol, lisp_str


def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    exp_list = []
    sub_parsers = [bool_parser, symbol_parser, ]
    while lisp_str and lisp_str.strip()[0] != ")":
        for sub_parser in sub_parsers:
            sub_parsed = sub_parser(lisp_str)
            if sub_parsed and sub_parsed[0]:
                parsed, lisp_str = sub_parsed
                exp_list.append(parsed)

        if lisp_str[0] == '(':
            nested_exp = expression_parser(lisp_str[1:])
            parsed, lisp_str = nested_exp[0], nested_exp[1].strip()
            exp_list.append(parsed)
    return exp_list, lisp_str[1:]


def input_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[0] == "(":
        lisp_str = lisp_str[1:]
    else:
        return None
    parsed_lists = []
    while expression_parser(lisp_str):
        expression_parsed, lisp_str = expression_parser(lisp_str)
        if expression_parsed:
            parsed_lists.extend(expression_parsed)
    print(parsed_lists, lisp_str)
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


def get_value(key):
    value = MATH_ENV.get(key, False) or OP_ENV.get(key, False) or LOCAL_ENV.get(key, False)
    return value

def lisp_evaluator(parsed):
    if not parsed:
        return None
    number = (int, float)
    if isinstance(parsed, number):
        return parsed

    if isinstance(parsed, str):
        return get_value(parsed)

    operation, *arguments = parsed
    if operation == 'define':
        variable, exp = arguments
        LOCAL_ENV[variable] = lisp_evaluator(exp)
        return "OK"

    print(arguments)
    if operation == 'if':
        print(arguments)
        condition, output, alt_output = arguments
        return lisp_evaluator(output if lisp_evaluator(condition) else alt_output)
    if operation == 'quote':
        return arguments[0]
    if operation == 'lambda':
        parameters, body = arguments
        return Procedure(parameters, body)
    if operation == "range":
        range_args = [int(i) for i in arguments]
        return list(reduce(range, range_args))

    proc = get_value(operation)
    if operation in ["<", ">", "<=", ">=",]:
        arg_list = [lisp_evaluator(argument) for argument in arguments]
        return OP_ENV[eval_comparision(proc, arg_list)]

    if operation in OP_ENV:
        arg_list = [lisp_evaluator(argument) for argument in arguments]
        print(arg_list)
        print(reduce(proc, arg_list))
        return reduce(proc, arg_list)
    if operation in MATH_ENV and len(arguments) == 1:
        # print(proc(lisp_evaluator(arguments[0])))
        return proc(lisp_evaluator(arguments[0]))
        # arg1, arg2 = [lisp_evaluator(argument) for argument in arguments]
        # print(proc(lisp_evaluator(arguments[0])))
        # return proc(lisp_evaluator(arg_list))
    return None


def main():
    try:
        os.system("clear||cls")
        while True:
            output = lisp_evaluator(lisp_interpreter(repl()))
            if output:
                print(output)
            else:
                print("\nsyntax error\n")
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
    # except:
    #     print("\nSyntax error\n")
    #     os.sys.exit()

if __name__ == '__main__':
    main()
