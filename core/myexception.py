#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Ejemplo: raise FuzzException(FuzzException.FATAL, "Explicacion del error: %s" % str(e))


class MyException(Exception):

    FATAL, SIGCANCEL = range(2)

    def __init__(self, etype, msg):
        self.etype = etype
        self.msg = msg
        Exception.__init__(self, msg)
