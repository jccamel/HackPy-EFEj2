#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket
import mmap
from ipaddress import IPv4Address, IPv4Network

"""
MODULO CLOUDFLARE

"""

def clouflare_test(path_range, path_ipout, domaintest):
    response_test = False
    test1 = False
    test2 = False
    real_ip = '0.0.0.0'
    try:
        iptest = socket.gethostbyname(domaintest)
    except:
        response_test = True
        print ">>> Somthing wrong with domain Script finish here sorry!! <<<"
        return response_test, real_ip

    file_rage = file(path_range, "r")
    ranges = file_rage.read().splitlines()
    file_rage.close()
    del file_rage

    for range in ranges:
        if IPv4Address(iptest.decode("utf-8")) in IPv4Network(range.decode("utf-8")):
            test1 = True

    file_ipout = open(path_ipout)
    s = mmap.mmap(file_ipout.fileno(), 0, access=mmap.ACCESS_READ)
    if s.find(domaintest) != -1:
        s.seek(s.find(domaintest))
        real_ip = s.readline().split()[1]
        test2 = True
    s.close()

    if test1 and test2:
        print "\n*****************************************"
        print "%s is in range of Cloudflare" % iptest
        print "And %s is in database" % domaintest
        print "The real IP for %s is: %s" % (domaintest, real_ip)
        print "*****************************************"
        return response_test, real_ip  # True, real_ip
    elif test1 and not test2:
        response_test = True
        print "\n*****************************************"
        print "%s is in range of Cloudflare" % iptest
        print "And %s is not in database" % domaintest
        print "The finally result will be wrong\n"
        print "       Script finish here sorry!!"
        print "*****************************************\n"
        return response_test, iptest  # True, 0.0.0.0
    elif not test1 and test2:
        print "\n*****************************************"
        print "%s is not in range of Cloudflare" % iptest
        print "And %s is in database" % domaintest
        print "The real IP for %s is: %s" % (domaintest, real_ip)
        print "*****************************************"
        return response_test, real_ip  # True, real_ip
    else:
        print "CLOUDFLARE Test - Maybe all ok!"
        return response_test, iptest  # False, domaintest
