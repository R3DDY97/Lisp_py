#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
from lisp_parsing import lisp_parser
from lisp_evaluation import lisp_evaluator

# class ENV(dict):
#     "An environment: a dict of {'var': val} pairs, with an outer Env."
#     def __init__(self, parms=(), args=(), genv=None):
#         self.update(zip(parms, args))
#         self.genv = genv
#     def find(self, var):
#         "Find the innermost Env where var appears."
#         return self if (var in self) else self.genv.find(var)


# class Procedure(object):
#     "A user-defined Scheme procedure."
#     def __init__(self, params, body):
#         self.params, self.body = params, body
#
#     def __call__(self, *args):
#         LAMBDA_ENV.update(zip(self.params, args))
#         return lisp_evaluator(lisp_evaluator(self.body))


def lisp_interpreter(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    lisp_parsed = lisp_parser(lisp_str)
    if lisp_parsed and lisp_parsed[0]:
        parsed, _ = lisp_parsed
        return lisp_evaluator(parsed)
        # print(parsed)
        # return parsed
    return None

def main():
    try:
        os.system("clear||cls")
        while True:
            lisp_input = input("Lisp repl> ")
            output = lisp_interpreter(lisp_input)
            # if output:
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
