"""
This is a very simple logger. It might evolve over time and add file support and stuff.
"""

import datetime

debugmode = False

separator = '::'


def printf(label, basestring, *args, **kw):
    print(label, separator, datetime.datetime.now(), separator, basestring.format(*args, **kw))


def info(basestring, *args, **kw):
    printf('INFO ', basestring, *args, **kw)


def warn(basestring, *args, **kw):
    printf('WARN ', basestring, *args, **kw)


def debug(basestring, *args, **kw):
    if debugmode:
        printf('DEBUG', basestring, *args, **kw)

