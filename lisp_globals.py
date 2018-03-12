#!/usr/bin/env python3
'''Lisp global environment variables and keywords as python dict'''

import math
import operator

def lisp_env():
    operator_dict = {"+": operator.add,
                     "-": operator.sub,
                     "*": operator.mul,
                     "//": operator.floordiv,
                     "/": operator.truediv,
                     "%": operator.mod,
                     "<": operator.lt,
                     ">": operator.gt,
                     ">=": operator.ge,
                     "<=": operator.le,
                     "^" : operator.pow,
                     "pow":operator.pow,
                     "expt":operator.pow,
                     'range': range,
                     "list": list,
                     "#t" : True,
                     "#f" :False,
                     True:"#t",
                     False:"#f",
                    }

    lisp_globals = {'begin': lambda *x: x[-1],
                    'car':   lambda x: x[0],
                    'cdr':   lambda x: x[1:],
                    'cons':  lambda x, y: [x] + y,
                    'list':  lambda *x: list(x),
                    'print':  print,
                    'range': lambda x, y: tuple(range(x, y)),
                   }

    math_dict, both_dict = vars(math), vars(math)
    both_dict.update(operator_dict)
    both_dict.update(lisp_globals)
    # return operator_dict, math_dict
    return both_dict, operator_dict, math_dict
