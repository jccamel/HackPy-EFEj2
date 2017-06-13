# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

"""
MODULO CENSYS
Con éste modulo se obtienen los subdominios asociados al dominio a investigar.
Se utiliza la API de https://censys.io/
Los límites de velocidad de Censys se aplican usando tokens, las tarifas asociadas con una cuenta gratuita son:
* query 0.0 tokens/second (0.0 per 5 minute bucket)
* search 0.2 tokens/second (60.0 per 5 minute bucket)
* api 0.4 tokens/second (120.0 per 5 minute bucket)
Las credenciales necesarias para acceder a la API son:
- API ID
- Secret
- URL de la API: https://www.censys.io/api/v1/
Ejemplo:
    API_URL = "https://www.censys.io/api/v1"
	UID = "c9dbba47-9aa7-48ab-abe1-6e756102f338"
	SECRET = "77PjEDT2fuBmItLRu4eZkkFdOYdmxFWe"
"""

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

