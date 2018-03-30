#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
import re
from functools import reduce
# from collections import deque
from lisp_repl import repl
from lisp_globals import lisp_env
from lisp_evaluation import eval_comparision

GLOBAL_ENV, OP_ENV, MATH_ENV = lisp_env()
# LOCAL_ENV = {}
LAMBDA_ENV = {}

SPL_WORDS = ['define', 'if', 'set!', ]
SPL_METHODS = ['list', 'range', 'quote',  ]
KEYWORDS = SPL_WORDS + SPL_METHODS

# class ENV(dict):
#     "An environment: a dict of {'var': val} pairs, with an outer Env."
#     def __init__(self, parms=(), args=(), genv=None):
#         self.update(zip(parms, args))
#         self.genv = genv
#     def find(self, var):
#         "Find the innermost Env where var appears."
#         return self if (var in self) else self.genv.find(var)


class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, params, body):
        self.params, self.body = params, body

    def __call__(self, *args):
        LAMBDA_ENV.update(zip(self.params, args))
        return lisp_evaluator(lisp_evaluator(self.body))

def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t" or lisp_str[:2] == "#f":
        return lisp_str[:2], lisp_str[2:].strip()
    return None

def symbol_parser(lisp_str):
    re_symbol = re.match(r'[^ \t\n\r\f\v()]+', lisp_str)
    # re_symbol = re.match(r'^\s*[+-]?[\w-]+|[><+-/*%]?\s*', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group().strip(), lisp_str[re_symbol.end():].strip()
        return symbol, lisp_str
    return None

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
    # print(parsed_lists, lisp_str)
    return parsed_lists, lisp_str

def lisp_interpreter(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    lisp_parsed = input_parser(lisp_str)
    if lisp_parsed and lisp_parsed[0]:
        # parsed, _ = input_parser(lisp_str)
        parsed, _ = lisp_parsed
        # print(parsed)
        return parsed
    return None

def get_value(key):
    value = LAMBDA_ENV.get(key, False) or GLOBAL_ENV.get(key, False)
    return value

def lisp_evaluator(parsed):
    if isinstance(parsed, (int, float, str)):
        print(eval_atom(parsed))
        return eval_atom(parsed)

    operation, *arguments = parsed

    if operation == 'lambda':
        parameters, body = arguments
        # parameters = [lisp_evaluator(param) for param in parameters]
        return Procedure(parameters, body)

    for evaluator in (keyword_eval, eval_math, defined_function):
        evaluated = evaluator(operation, arguments)
        if evaluated == 0 or evaluated:
            return evaluated
    return None


def defined_function(operation, arguments):
    pass
    return "coding soon"


def eval_atom(parsed):
    try:
        parsed = int(parsed)
        return parsed
    except ValueError:
        pass
    try:
        parsed = float(parsed)
        return parsed
    except ValueError:
        return get_value(parsed)

def keyword_eval(operation, arguments):
    if not operation in KEYWORDS:
        return None
    arg_list = [lisp_evaluator(argument) for argument in arguments]

    keyword_dict = {"quote" : lambda args: args[0],
                    "list"  : list,
                    "range" : lambda args: list(reduce(range, args)),
                    "define": eval_define,
                    "if"    : eval_if,
                    "set!"  : eval_set,
                   }

    if operation in SPL_WORDS:
        return keyword_dict[operation](arguments)
    return keyword_dict[operation](arg_list)

def eval_define(arguments):
    variable, exp = arguments
    if variable in GLOBAL_ENV:
        print("\ncant define variable.. its standard.. Dont mess with standards\n ")
        return None
    GLOBAL_ENV[variable] = lisp_evaluator(exp)
    return "OK"

def eval_set(arguments):
    variable, exp = arguments
    if GLOBAL_ENV.get(variable, False):
        GLOBAL_ENV[variable] = lisp_evaluator(exp)
        return "OK"
    print("Error {} is not defined".format(variable))
    return None


def eval_if(arguments):
    condition, output, alt_output = arguments
    return lisp_evaluator(output if lisp_evaluator(condition) else alt_output)

def eval_lambda(arguments):
    # arg_list = [lisp_evaluator(argument) for argument in arguments]
    parameters, body = arguments
    # parameters = [lisp_evaluator(param) for param in parameters]
    return Procedure(parameters, body)


def eval_math(operation, arguments):
    if not operation in OP_ENV or not operation in  MATH_ENV:
        return None
    arg_list = [lisp_evaluator(argument) for argument in arguments]
    procedure = OP_ENV.get(operation, False) or MATH_ENV.get(operation, False)
    print(arg_list)

    if operation in ["<", ">", "<=", ">=",]:
        return OP_ENV[eval_comparision(procedure, arg_list)]

    if operation in OP_ENV:
        return reduce(procedure, arg_list)

    if len(arg_list) == 1:
        return procedure(arg_list[0])
    arg1, arg2 = arg_list
    return procedure(arg1, arg2)

def main():

    try:
        os.system("clear||cls")
        while True:
            output = lisp_evaluator(lisp_interpreter(repl()))
            if output:
                print(output)
            # else:
            #     print("\nsyntax error\n")
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
    # except:
    #     print("\nSyntax error\n")
    #     os.sys.exit()

if __name__ == '__main__':
    main()
