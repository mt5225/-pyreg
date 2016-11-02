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
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
import SocketServer
from WXBizMsgCrypt import WXBizMsgCrypt
import urllib


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        sToken = "uniroom"
        sEncodingAESKey = "4Qd2dafqbSONP1tYNyJluzApCIg9Ct49anmeQ66HrSJ"
        sCorpID = "wx4a5123f6bcee9967"
        wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
        self._set_headers()
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        sVerifyMsgSig=query_components["msg_signature"]
        sVerifyTimeStamp=query_components["timestamp"]
        sVerifyNonce=query_components["nonce"]
        sVerifyEchoStr=urllib.unquote(urllib.unquote(query_components["echostr"]))
        print '---------'
        print sVerifyEchoStr
        print '---------'
        ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
        print sEchoStr
        if(ret!=0):
            print ret
            exit(1)
        self.wfile.write(sEchoStr)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

