#!/usr/bin/env python3

from functools import reduce
from lisp_globals import lisp_env

# various sub environments
GLOBAL_ENV, OP_ENV, MATH_ENV = lisp_env()
LOCAL_ENV = {}
# LAMBDA_ENV = {}


def get_value(key):
    value = LOCAL_ENV.get(key, False) or GLOBAL_ENV.get(key, False)
    return value

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
    spl_words, spl_methods = ['define', 'if', 'set!'], ['list', 'range', 'quote']
    keywords = spl_words + spl_methods
    if not operation in keywords:
        return None
    arg_list = [lisp_evaluator(argument) for argument in arguments]
    keyword_dict = {"quote" : lambda args: args[0],
                    "list"  : list,
                    "range" : lambda args: list(reduce(range, args)),
                    "define": eval_define,
                    "if"    : eval_if,
                    "set!"  : eval_set,
                   }
    if operation in spl_words:
        return keyword_dict[operation](arguments)
    return keyword_dict[operation](arg_list)

def eval_define(arguments):
    variable, exp = arguments
    if variable in GLOBAL_ENV:
        print("\ncant define variable.. its standard.. Dont mess with standards\n ")
        return None
    LOCAL_ENV[variable] = lisp_evaluator(exp)
    return "OK"

def eval_set(arguments):
    variable, exp = arguments
    if GLOBAL_ENV.get(variable, False):
        GLOBAL_ENV[variable] = lisp_evaluator(exp)
        return "OK"
    print("Error {} is not defined".format(variable))
    return None

def eval_if(arguments):
    condition, value, alt = arguments
    # return lisp_evaluator(value if lisp_evaluator(condition) else alt)
    if lisp_evaluator(condition):
        return lisp_evaluator(value)
    return lisp_evaluator(alt)

def eval_comparision(operation, arguments):
    arg_list = [lisp_evaluator(argument) for argument in arguments]
    if operation in ["<", ">", "<=", ">=",] and  len(arg_list) > 1:
        procedure = OP_ENV.get(operation)
        bool_dict = {True: "#t", False: "#f"}
    else:
        return None

    pre_index, post_index = 0, 1

    while post_index < len(arg_list):
        status = procedure(arg_list[pre_index], arg_list[post_index])
        if status:
            post_index += 1
        else:
            pre_index, post_index = post_index, post_index+1
    return bool_dict[status]


def eval_math(operation, arguments):
    if not operation in OP_ENV or not operation in  MATH_ENV:
        return None
    arg_list = [lisp_evaluator(argument) for argument in arguments]
    procedure = OP_ENV.get(operation, False) or MATH_ENV.get(operation, False)

    if operation in OP_ENV:
        return reduce(procedure, arg_list)

    if len(arg_list) == 1:
        return procedure(arg_list[0])
    arg1, arg2 = arg_list
    return procedure(arg1, arg2)

def lisp_evaluator(parsed):
    if isinstance(parsed, (int, float, str)):
        return eval_atom(parsed)

    operation, *arguments = parsed

    if operation == 'lambda':
        parameters, body = arguments
        # parameters = [lisp_evaluator(param) for param in parameters]
        return Procedure(parameters, body)

    # order of evaluation loop is not to be changed eval_comparision comes b4 eval_math
    for evaluator in (keyword_eval, eval_comparision, eval_math, defined_function):
        evaluated = evaluator(operation, arguments)
        if evaluated != None:
            return evaluated
    return None



def defined_function(operation, arguments):
    pass



class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, params, body):
        self.params, self.body = params, body

    def __call__(self, *args):
        LOCAL_ENV.update(zip(self.params, args))
        output = lisp_evaluator(self.body)
        return output
        # return lisp_evaluator(self.body)


# if __name__  == '__main__':
#     lisp_evaluator(parsed)
