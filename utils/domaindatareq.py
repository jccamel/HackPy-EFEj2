#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import whois
from core.myexception import MyException


def domain_data(domain):
    """
    Dada una dirección IP o un nombre de dominio, encontrar información
    relacionada con el propietario de dicho dominio y sus registros DNS.
    """
    whois_data = {'updated_date': 'Data Update:', 'name': 'Name:\t', 'dnssec': 'DNSsec\t',
                  'city': 'City:\t', 'expiration_date': 'Date Exp.:\t', 'zipcode': 'Zip Code:\t',
                  'domain_name': 'Domain Name', 'country': 'Country:\t', 'whois_server': 'Whois Server:',
                  'state': 'State:\t', 'registrar': 'Registrar:\t', 'referral_url': 'Referral URL:',
                  'address': 'Address:\t', 'name_servers': 'Name Servers:', 'org': 'Organization:',
                  'creation_date': 'Data Creation:', 'emails': 'Emails:\t', 'status': 'Status:\t'}

    try:
        datos = whois.whois(domain)
        for c, v in datos.iteritems():
            print "     {}\t{}".format(whois_data[c], v)
    except Exception, e:
        raise MyException(MyException.FATAL, ">>> Error in Whois: %s <<<" % str(e))

