# -*- coding: UTF-8 -*-
# Author  : Liushuai
# Time    : 2020/2/23 19:17
# File    : utils.py


def print_error(msg):
    print("\033[31;1mError:\033[0m%s" % msg)


def print_warning(msg):
    print("\033[33;1mWarning:\033[0m%s" % msg)


def print_info(msg):
    print("\033[32;1mInfo:\033[0m%s" % msg)
