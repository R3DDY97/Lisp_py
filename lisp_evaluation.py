#!/usr/bin/env python3


COMBINED_ENV = {}

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
        return "OK"

    if operation == 'if':
        condition, value, alt = arguments
        if lisp_evaluator(condition, env):
            return lisp_evaluator(value, env)
        return lisp_evaluator(alt, env)

    if operation  in  env:
        proc = lisp_evaluator(operation, env)
        arg_list = [lisp_evaluator(argument, env) for argument in arguments]
        return proc(*arg_list)

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
