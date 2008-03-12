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

