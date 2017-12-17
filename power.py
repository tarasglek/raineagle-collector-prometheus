#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import RainEagle
from RainEagle import to_epoch_1970
import time

def calc_instantdemand(idemand) :
    multiplier = int(idemand['Multiplier'], 16)
    divisor = int(idemand['Divisor'], 16)

#    demand = twos_comp(int(idemand['Demand'], 16))

    demand = int(idemand['Demand'], 16)

    if demand > 0x7FFFFFFF:
        demand -= 0x100000000

    if multiplier == 0 :
        multiplier = 1

    if divisor == 0 :
        divisor = 1

    reading = (demand * multiplier) / float (divisor)
    return reading
    # print "\tDemand    = {0:10.3f} Kw".format(reading)
    # print "\tAmps      = {0:10.3f}".format( ((reading * 1000) / 240))

import SimpleHTTPServer
raineagle = None

class Handler(BaseHTTPRequestHandler):
    def write_kw(self):
        demand = raineagle.get_instantaneous_demand()
        demand = demand['InstantaneousDemand']
        timestamp = (to_epoch_1970(demand['TimeStamp'])) * 1000
        kw = calc_instantdemand(demand)
        self.wfile.write("kw %f %d\n" % (kw, timestamp))

    def write_price(self):
        price_params = raineagle.get_price()
        timestamp = (int(price_params["price_timestamp"])+time.timezone)*1000
        self.wfile.write("price %s %d\n" % (price_params["price"], timestamp))
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        query = self.path[1:]
        if query == "kw":
            self.write_kw()
        elif query == 'price':
            self.write_price()
        elif query == 'metrics':
            self.write_price()
            self.write_kw()

def run(address='0.0.0.0', port=8080):
    print 'Listening on %s:%d' % (address, port)
    global raineagle
    raineagle = RainEagle.Eagle(debug=0, addr=os.environ['RAINFOREST'], username=None, password=None)
    httpd = HTTPServer((address, port), Handler)
    httpd.serve_forever()
    

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

