#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import ConfigParser
import sys
from argparse import ArgumentParser
from utils.georeq import GeoLocate
# from utils.domaindatareq import domain_data
from utils.nmapreq import nmap_analisis
from utils.censys import CensysSubdomains
from utils.shodanreq import ShodanClass
from core.cloudflarereq import clouflare_test
from core.honeypot import honeypot_test
from core.createproject import dolinux


if __name__ == '__main__':

    config = ConfigParser.ConfigParser()
    config.read('core/CONFIG.cfg')
    # Descripción general del script
    argp = ArgumentParser(version='Versión del script: 1.1', description=' \
    Dada una dirección IP o un nombre de dominio, encontrar información \
    relacionada con el propietario de dicho dominio y los registros DNS \
    correspondientes.')
    # Opciones integradas en el script
    # Opción obligatoria -d dominio que será analizado:
    # python EFEj2.py -d www.nombredominio.extensiondominio
    argp.add_argument('-d', '--domin', action='store', required=True, help='Dominio a analizar')
    # Opción -g opcional con tres niveles excluyentes entre si de geolocalización. Se explican en el módulo utils/georeq.py
    argp.add_argument('-g', '--geoloc', choices=['insights', 'city', 'country', 'db'], required=False,
                      help='Geolocalización del dominio a analizar')
    # Oción -nm opcional donde se inicia el analisis del dominio con las erramientas:
    # Censys (se buscan subdominios del dominio analizado), Shodan (busca vulnerabilidades en el dominio
    # así como puertos abiertos) y finalmente un escaneo de puertos los puertos encontrados con Nmap.
    # Dentro de esta opción tambien se realizar una petición HTTP utilizando el método OPTIONS para 
    # determinar si efectivamente, el objetivo es un servidor web y extraer los métodos HTTP soportados.
    argp.add_argument('-nm', '--scannmap', action='store_true', required=False,
                      help='Escaneo con Nmap y completar informacion con Shodan')

    args = argp.parse_args()

    if args.domin:
        pathproject = dolinux(args.domin) # Se crea una carpeta de proyecto con el mismo nombre del dominio a analizar.
        
        test, realip = clouflare_test(config.get('CLOUDFLARE', 'CLOUDFLARE_PATH_RG'),
                                      config.get('CLOUDFLARE', 'CLOUDFLARE_PATH_IP'), args.domin)

        if not test:
            try:
                percent = honeypot_test(realip, config.get('SHODAN', 'SHODAN_API_KEY'))
            except:
                print "No data HoneyPoy <<<<<<"
                pass

            print '[*]-- %s (%s)\n' % (realip, args.domin)
            print "\nDOMAIN DATA ****************************************************************"
            # domain_data(args.domin)
            if args.geoloc:
                print "\nGEOLOCALIZACIÓN *************************************************"
                g = GeoLocate(realip, args.geoloc, config.get('MAXMIND', 'MAXMIND_USER_ID'),
                              config.get('MAXMIND', 'MAXMIND_API_KEY'), config.get('MAXMIND', 'MAXMIND_DB'))
                g.geolocate_doc()
                del g
            if args.scannmap:
                print "\nANALISIS CENSYS/SHODAN/NMAP ************************************************"
                cs = CensysSubdomains(realip, config.get('CENSYS', 'CENSYS_API_URL'), config.get('CENSYS', 'CENSYS_UID'),
                             config.get('CENSYS', 'CENSYS_API_KEY'))
                subdomainslist = cs.search()
                del cs
                print "Analisis Domain and Subdomains from CENSYS"
                count = 0
                for subdomain in subdomainslist:
                    sh = ShodanClass(subdomain, config.get('SHODAN', 'SHODAN_API_KEY'))
                    vul, listvul = sh.svulns()
                    if vul:
                        count = count + 1
                        print "[%s] IP: %s" % (str(count), subdomain)
                        for vuln in listvul:
                            print "\t[Shodan] Vulnerable to: %s" % (vuln)
                        for hname in sh.shostnames():
                            print "\t[Shodan] Host name: %s" % (hname)
                        listports = ", ".join(str(x) for x in sh.sopenports())
                        nmap_analisis(args.domin, subdomain, listports)
                    del sh

        else:
            sys.exit(0)
