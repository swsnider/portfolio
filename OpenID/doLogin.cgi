#!/usr/bin/env python
import cgi, cgitb, sys
cgitb.enable()

from util import setSession, auth, doOpenIDFail, doOpenID
import imaplib

f = cgi.FieldStorage()
fields = {}
for i in f.keys():
	fields[i] = f[i].value
del f

if not (fields.has_key('user_name') and fields.has_key('password') and fields.has_key('request')):
	print "Content-Type: text/plain\n"
	print "Please, no tricks!"
	sys.exit(0)

if auth(fields['user_name'], fields['password']):
	request, response = doOpenID(cgi.parse_qs(fields['request']), fields['user_name'])
	setSession(request)
	print response
else:
	response = doOpenIDFail(cgi.parse_qs(fields['request']), fields['user_name'])
	print response

