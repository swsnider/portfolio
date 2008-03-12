#!/usr/bin/env python
"""
Copyright (c) 2008 Silas Snider

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import cgi, cgitb
cgitb.enable()
import imaplib
j = cgi.FieldStorage()
result = {}
for i in j.keys():
	result[i] = j[i].value
import openid.server.server as serv
import sys
from openid.store.filestore import FileOpenIDStore
from util import checkCookie, showLogin

oserver = serv.Server(FileOpenIDStore("dat.dat"), "http://hopper.uoregon.edu/oi.cgi")
request = oserver.decodeRequest(result)
if request.mode in ['checkid_immediate', 'checkid_setup']:
   request.claimed_id = None
   f = open("out.out", "a")
   f.write("\n\n" + `request.identity` + ":" + `request.claimed_id` + ":" + `request.mode` + "\n\n")
   f.close()
   if checkCookie(request):
       response = request.answer(True)
   elif request.immediate:
       response = request.answer(False)
   else:
       showLogin(request, result)
       sys.exit(0)
else:
   response = oserver.handleRequest(request)




print "Content-Type: text/html"
webresponse = oserver.encodeResponse(response)
for i in webresponse.headers.keys():
	print i + ": " + webresponse.headers[i]
print
print webresponse.body
