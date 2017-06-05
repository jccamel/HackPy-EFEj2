#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests


class HttpReq(object):

    def __init__(self, domain, port):
        self.domain = domain
        self.port = port
        self.furl = ""
        self.allow = []

    def __del__(self):
        pass

    def req(self):
        if self.port == 443:
            self.furl = 'https://%s:%s' % (self.domain, self.port)
        else:
            self.furl = 'http://%s:%s' % (self.domain, self.port)
        r = requests.options(self.furl)
        try:
            self.allow = r.headers['Allow'].split(', ')
        except:
            pass
        return self.allow
