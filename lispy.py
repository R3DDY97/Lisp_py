#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
# import re
# from functools import reduce
# from collections import deque
from lisp_repl import repl
from lisp_globals import lisp_env

ENV = lisp_env()
LOCAL_ENV = {}


def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t" or lisp_str[:2] == "#t":
        return lisp_str[:2], lisp_str[2:]
    return None

def number_parser(lisp_str):
    pass

def string_parser(lisp_str):
    pass

def input_parser(lisp_str):
    pass



def main():
    try:
        os.system("clear||cls")
        while True:
            input_parser(repl())
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
        os.sys.exit()
        print("\nInput error\n")

if __name__ == '__main__':
    main()
