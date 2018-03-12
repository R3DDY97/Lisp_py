#!/usr/bin/env python3

from functools import reduce
from lisp_globals import lisp_env

# various sub environments
GLOBAL_ENV, OP_ENV, MATH_ENV = lisp_env()
COMBINED_ENV = {}



def get_value(key):
    value = COMBINED_ENV.get(key)
    # value = env.get(key, False) or COMBINED_ENV.get(key, False)
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
        # return get_value(parsed)
        return COMBINED_ENV.get(parsed)

def keyword_eval(operation, arguments,env):
    spl_words, spl_methods = ['define', 'if', 'set!'], ['list', 'range', 'quote']
    keywords = spl_words + spl_methods
    if not operation in keywords:
        return None
    arg_list = [lisp_evaluator(argument, env) for argument in arguments]
    keyword_dict = {"quote" : lambda args: args[0],
                    "list"  : list,
                    "range" : lambda args: list(reduce(range, args)),
                    "define": eval_define,
                    "if"    : eval_if,
                    "set!"  : eval_set,
                   }
    if operation in spl_words:
        return keyword_dict[operation](arguments, env)
    return keyword_dict[operation](arg_list, env)

def eval_define(arguments, env):
    variable, exp = arguments
    if variable in env:
        print("\ncant define variable.. its standard.. Dont mess with standards\n ")
        return None
    env[variable] = lisp_evaluator(exp, env)
    return "OK"

def eval_set(arguments, env):
    variable, exp = arguments
    if env.get(variable, False):
        env[variable] = lisp_evaluator(exp, env)
        return "OK"
    print("Error {} is not defined".format(variable))
    return None

def eval_if(arguments, env):
    condition, value, alt = arguments
    # return lisp_evaluator(value if lisp_evaluator(condition) else alt)
    if lisp_evaluator(condition, env):
        return lisp_evaluator(value, env)
    return lisp_evaluator(alt, env)

def eval_comparision(operation, arguments, env):
    arg_list = [lisp_evaluator(argument, env) for argument in arguments]
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


def eval_math(operation, arguments, env):
    if not operation in OP_ENV or not operation in  MATH_ENV:
        return None
    arg_list = [lisp_evaluator(argument, env) for argument in arguments]
    procedure = OP_ENV.get(operation, False) or MATH_ENV.get(operation, False)

    if operation in OP_ENV:
        return reduce(procedure, arg_list)

    if len(arg_list) == 1:
        return procedure(arg_list[0])
    arg1, arg2 = arg_list
    return procedure(arg1, arg2)

def lisp_evaluator(parsed, env=GLOBAL_ENV):
    if isinstance(parsed, (int, float, str)):
        return eval_atom(parsed)
    # print(parsed)

    operation, *arguments = parsed

    if operation == 'lambda':
        parameters, body = arguments
        # parameters = [lisp_evaluator(param) for param in parameters]
        return Procedure(parameters, body, env)

    # order of evaluation loop is not to be changed eval_comparision comes b4 eval_math
    for evaluator in (keyword_eval, eval_comparision, eval_math):
        evaluated = evaluator(operation, arguments, env)
        if evaluated != None:
            return evaluated

    proc = env[parsed[0]]
    arg_list = [lisp_evaluator(argument, env) for argument in parsed[1:]]
    # args = [lisp_evaluator(arg, env) for exp in x[1 : ]]
    return proc(arg_list)


def Procedure(parameters, body, env):
    def callFunction(arg_list):
        # arg_list = [i for i in args]
        # print(body, arg_list, parameters)
        return lisp_evaluator(body, localEnv(parameters, arg_list, env))
    return callFunction


def localEnv(parameters, arg_list, env):
    COMBINED_ENV.update(dict(zip(parameters, arg_list)))
    COMBINED_ENV.update(env)
    return COMBINED_ENV
