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
                     "#t" : True,
                     "#f" :False,
                     True:"#t",
                     False:"#f",
                    }

    math_dict = vars(math)
    return operator_dict, math_dict

def eval_comparision(proc, arg_list):
    # print(len(arg_list))
    # print(arg_list)
    if len(arg_list) < 2:
        print("\nSyntax Error\n")
        return None
    pre_index = 0
    post_index = 1
    while post_index < len(arg_list):
        status = proc(arg_list[pre_index], arg_list[post_index])
        if status:
            post_index += 1
        else:
            pre_index, post_index = post_index, post_index+1
    return status
