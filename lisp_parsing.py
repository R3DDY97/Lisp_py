#!/usr/bin/env python3

import re

def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t" or lisp_str[:2] == "#f":
        return lisp_str[:2], lisp_str[2:].strip()
    return None

def symbol_parser(lisp_str):
    re_symbol = re.match(r'[^ \t\n\r\f\v()]+', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group().strip(), lisp_str[re_symbol.end():].strip()
        # return symbol, lisp_str
        try:
            symbol = int(symbol)
            return symbol, lisp_str
        except ValueError:
            pass
        try:
            symbol = float(symbol)
            return symbol, lisp_str
        except ValueError:
            pass
        return symbol, lisp_str
    return None


def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    exp_list = []
    sub_parsers = [bool_parser, symbol_parser, ]
    while lisp_str and lisp_str.strip()[0] != ")":
        for sub_parser in sub_parsers:
            sub_parsed = sub_parser(lisp_str)
            if sub_parsed and sub_parsed[0]:
                parsed, lisp_str = sub_parsed
                exp_list.append(parsed)

        if lisp_str[0] == '(':
            nested_exp = expression_parser(lisp_str[1:])
            parsed, lisp_str = nested_exp[0], nested_exp[1].strip()
            exp_list.append(parsed)
    return exp_list, lisp_str[1:]

def lisp_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[0] == "(":
        lisp_str = lisp_str[1:]
    else:
        return None
    parsed_lists = []
    while expression_parser(lisp_str):
        expression_parsed, lisp_str = expression_parser(lisp_str)
        if expression_parsed:
            parsed_lists.extend(expression_parsed)
    # print(parsed_lists, lisp_str)
    return parsed_lists, lisp_str
