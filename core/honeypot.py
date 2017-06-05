#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from core.myexception import MyException


def honeypot_test(domain, numkey):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    payload = {'key': numkey}
    try:
        r = requests.get('https://api.shodan.io/labs/honeyscore/' + domain, params=payload, verify=False, timeout=5)
        if r.status_code == requests.codes.ok:
            honeyxcent = float(str(r.text)) * 100
            print 'Probability of being a honeypot: %s percent\n' % str(honeyxcent)
            return honeyxcent
        else:
            print 'UUUps!! Something is not right\n'
    except Exception, e:
        raise MyException(MyException.FATAL, ">>> Error in HoneyPot: %s <<<" % str(e))
