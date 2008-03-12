#!/usr/bin/env python
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
