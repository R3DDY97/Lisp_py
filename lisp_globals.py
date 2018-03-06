#!/usr/bin/env python3
'''Lisp global environment variables and keywords as python dict'''

import math
import operator

def lisp_env():
    env_dict = {"+": operator.add,
                "-": operator.sub,
                "*": operator.mul,
                "//": operator.floordiv,
                "/": operator.truediv,
                "%": operator.mod,
               }
    env_dict.update(vars(math))
    return env_dict
