#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import shodan


class ShodanClass(object):

        def __init__(self, ip, api_key):
            self.ip = ip
            self.shconn = False
            try:
                self.conn = shodan.Shodan(api_key)
                self.shconn = True  # Connection with Shodan OK
            except shodan.exception.APIError, e:
                print "\tWarning: %s" % str(e)

        def __del__(self):
            pass

        def svulns(self):
            if self.shconn:
                try:
                    if len(self.conn.host(self.ip)['vulns']) > 0:
                        return True, self.conn.host(self.ip)['vulns']
                except:
                    return False

        def shostnames(self):
            if self.shconn:
                try:
                    return self.conn.host(self.ip)['hostnames']
                except:
                    return ["No Host Names"]

        def sopenports(self):
            if self.shconn:
                try:
                    return self.conn.host(self.ip)['ports']
                except:
                    return ["No ports"]

        def sdata(self):
            if self.shconn:
                try:
                    return self.conn.host(self.ip)['data']
                except:
                    return ["No data"]
