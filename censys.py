# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class CensysSubdomains(object):
    def __init__(self, ip, api_url, uid, api_key):

        self.API_URL = api_url
        self.UID = uid
        self.SECRET = api_key
        self.ip = ip
        self.subdomain = []

    def __del__(self):
        pass

    def search(self):

        pages = float('inf')
        page = 1

        while page <= pages:

            params = {'query': self.ip, 'page': page}
            res = requests.post(self.API_URL + "/search/ipv4", json=params, auth=(self.UID, self.SECRET))
            payload = res.json()

            for r in payload['results']:
                ip = r["ip"]
                self.subdomain.append(ip)
            pages = payload['metadata']['pages']
            page += 1

        return self.subdomain

