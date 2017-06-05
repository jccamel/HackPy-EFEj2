#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket

import nmap

from core.httpreq import HttpReq


def grab_banner(ip_address, port):
    banner = "\tNo banner"
    try:
        s = socket.socket()
        s.connect(ip_address, port)
        banner = s.recv(2048)
        return banner
    except:
        return banner


class NmapHost:
    def __init__(self):
        self.host = None
        self.state = None
        self.reason = None
        self.openPorts = []
        self.closedFilteredPorts = []


class NmapPort:
    def __init__(self):
        self.id = None
        self.state = None
        self.reason = None
        self.port = None
        self.name = None
        self.version = None
        self.scriptOutput = None


def parseNmapScan(scan):
    nmapHosts = []
    for host in scan.all_hosts():
        nmapHost = NmapHost()
        nmapHost.host = host
        if scan[host].has_key('status'):
            nmapHost.state = scan[host]['status']['state']
            nmapHost.reason = scan[host]['status']['reason']
            for protocol in ["tcp", "udp", "icmp"]:
                if scan[host].has_key(protocol):
                    ports = scan[host][protocol].keys()
                    for port in ports:
                        nmapPort = NmapPort()
                        nmapPort.port = port
                        nmapPort.state = scan[host][protocol][port]['state']
                        if scan[host][protocol][port].has_key('script'):
                            nmapPort.scriptOutput = scan[host][protocol][port]['script']
                        if scan[host][protocol][port].has_key('reason'):
                            nmapPort.reason = scan[host][protocol][port]['reason']
                        if scan[host][protocol][port].has_key('name'):
                            nmapPort.name = scan[host][protocol][port]['name']
                        if scan[host][protocol][port].has_key('version'):
                            nmapPort.version = scan[host][protocol][port]['version']
                        if 'open' in (scan[host][protocol][port]['state']):
                            nmapHost.openPorts.append(nmapPort)
                        else:
                            nmapHost.closedFilteredPorts.append(nmapPort)
                    nmapHosts.append(nmapHost)
        else:
            print "[-] There's no match in the Nmap scan with the specified protocol %s" % (protocol)
    return nmapHosts


def nmap_analisis(domain, target, ports):
    print "\tNMAP Scan >>>>>>>>>>>>>>>>>>>"
    nm = nmap.PortScanner()
    nm.scan(target, ports, arguments="-sV -n -A -T1")
    structureNmap = parseNmapScan(nm)
    for host in structureNmap:
        # print "\tHost: " + host.host
        # print "\tState: " + host.state
        for openPort in host.openPorts:
            print "\t(%s) %s - State: %s - Version: %s" % (
                str(openPort.name), str(openPort.port), openPort.state, openPort.version)
            if str(openPort.port) == '22':
                print "\tBanner --------------------- "
                print grab_banner(host, int(openPort.port))
                print "\t------------------------------"
            if str(openPort.name) == 'http':
                h = HttpReq(domain, openPort.port)
                lreq = h.req()
                if len(lreq) != 0:
                    print "\t\tMethods allowed: %s" % str(lreq)
                else:
                    print "\t\tMethod OPTIONS not allowed!"
