#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
from lisp_parsing import lisp_parser
from lisp_evaluation import lisp_evaluator
from lisp_globals import lisp_env
env, OP_ENV, MATH_ENV = lisp_env()


def lisp_interpreter(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    lisp_parsed = lisp_parser(lisp_str)
    if lisp_parsed and lisp_parsed[0]:
        parsed, _ = lisp_parsed
        return lisp_evaluator(parsed, env)
        # print(parsed)
        # return parsed
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
