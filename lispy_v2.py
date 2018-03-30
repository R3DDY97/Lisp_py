#!/usr/bin/env python3

import os
from functools import reduce
from lisp_globals import lisp_env
from lisp_parsing import lisp_parser


# various sub environments
env, OP_ENV, MATH_ENV = lisp_env()
LAMBDAs = []
COMBINED_ENV = {}


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


def lisp_evaluator(parsed, env):
    if isinstance(parsed, str):
        return env.get(parsed, None)
    if isinstance(parsed, (int, float)):
        return parsed

    operation, *arguments = parsed
    if operation == 'lambda':
        parameters, body = arguments
        return Procedure(parameters, body, env)

    if operation == 'define':
        variable, exp = arguments
        print(arguments)
        if variable in env:
            print("\ncant define variable.. its standard.. Dont mess with standards\n ")
            return None
        env[variable] = lisp_evaluator(exp, env)
        LAMBDAs.append(variable)
        return "OK"

    if operation == 'if':
        condition, value, alt = arguments
        if lisp_evaluator(condition, env):
            return lisp_evaluator(value, env)
        return lisp_evaluator(alt, env)

    try:
        if operation in env:
            proc = lisp_evaluator(operation, env)
            arg_list = [lisp_evaluator(argument, env) for argument in arguments]
            return proc(*arg_list)
    except TypeError:
        return eval_comparision(operation, arguments, env) or eval_math(operation, arguments, env)
    return None

def Procedure(parameters, body, env):
    def callFunction(arg_list):
        return lisp_evaluator(body, localEnv(parameters, arg_list, env))
    return callFunction

def localEnv(parameters, arg_list, env):
    lambda_local = dict(zip(parameters, [arg_list]))
    COMBINED_ENV.update(lambda_local)
    COMBINED_ENV.update(env)
    return COMBINED_ENV


def lisp_interpreter(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    lisp_parsed = lisp_parser(lisp_str)
    if lisp_parsed and lisp_parsed[0]:
        parsed, _ = lisp_parsed
        return lisp_evaluator(parsed, env)
    return None

def main():
    try:
        os.system("clear||cls")
        while True:
            lisp_input = input("Lisp repl> ")
            output = lisp_interpreter(lisp_input)
            bools = {False:"#t", True:"#t"}
            if output in bools:
                print(bools[output])
            if output:
                print(output)
            # else:
            #     print("\nsyntax error\n")
    except KeyboardInterrupt:
        print("\n\tExiting Lisp interpreter..\n")
    # except:
    #     print("\nSyntax error\n")
    #     os.sys.exit()

if __name__ == '__main__':
    main()
