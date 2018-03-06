#!/usr/bin/env python3
'''Lisp repl using python3'''

import os

def repl():
    input_exp = input("Lisp repl> ")
    return input_exp

def main():
    try:
        os.system("clear||cls")
        while True:
            repl()
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
        os.sys.exit()


if __name__ == '__main__':
    main()
