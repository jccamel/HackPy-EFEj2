#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

struc = ['/project', '/pdf_downloads', '/photo_downloads']


def dolinux(nameproject):
    path = os.getcwd()
    nameproject = '/' + nameproject
    if not os.path.exists(path + struc[0]):
        print 'Crate folder (%s) in %s' % (struc[0], path)
        os.mkdir(path + struc[0])
    path = path + struc[0] + nameproject
    if not os.path.exists(path):
        print 'Crate project folder (%s) in %s' % (nameproject, path)
        os.mkdir(path)
    for s in struc[1:len(struc)]:
        if not os.path.exists(path + s):
            print 'Create folder %s in %s' % (s, path)
            os.mkdir(path + s)
        else:
            pass
    return path


def dowindows(nameproject):
    pass
