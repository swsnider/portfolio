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

from Cookie import SimpleCookie
import os
import sys
from sqlobject import *
connection_string = "mysql://username:password@server/database"
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

if __name__ == "__main__":
	print "Content-Type:text/plain\n"
	print "WTF?"

class Session(SQLObject):
	identifier = StringCol(notNone=True)
	sid = StringCol(length=250, notNone=True, alternateID=True)

def isValidSession(request, sid):
	try:
		s = Session.bySid(sid)
		return s.identifier == request.identity
	except:
		return False

def checkCookie(request):
	if os.environ.has_key('HTTP_COOKIE'):
		cookieStr = os.environ.get('HTTP_COOKIE')
		if not cookieStr:
			return False
		cookie = SimpleCookie()
		cookie.load(cookieStr)
		if not cookie.has_key('hopper_oid_sid'):
			return False
		sid = cookie['hopper_oid_sid'].value
		return isValidSession(request, sid)
	else:
		return False

def showLogin(request, query):
	import kid, urllib
	template = kid.Template(file='login.kid', request=request, query=urllib.urlencode(query))
	print "Content-Type:text/html\n"
	print template.serialize()

def auth(user, passw):
	import imaplib
	try:
		M = imaplib.IMAP4_SSL("imap.uoregon.edu")
		M.login(user, passw)
		M.logout()
		del M
		return True
	except:
		return False

#following generate_id code thanks in part to CherryPy
try:
	import time, sha
	os.urandom(20)
except (AttributeError, NotImplementedError):
	# os.urandom not available until Python 2.4. Fall back to random.random.
	def generate_id():
		"""Return a new session id."""
		return sha.new('%s-%s' % (random.random(),time.ctime())).hexdigest()
else:
	def generate_id():
		"""Return a new session id."""
		return sha.new(os.urandom(20).encode('hex') + time.ctime()).hexdigest()

def setSession(request):
	sid = generate_id()
	newS = Session(identifier = request.identity, sid = sid)
	c = SimpleCookie()
	c['hopper_oid_sid'] = sid
	print c

def doOpenID(result, user, fail=False):
	for i in result.keys():
		result[i] = result[i][0]
	import openid.server.server as serv
	import sys
	from openid.store.filestore import FileOpenIDStore
	from util import checkCookie, showLogin

	oserver = serv.Server(FileOpenIDStore("dat.dat"), "http://hopper.uoregon.edu/oi.cgi")
	request = oserver.decodeRequest(result)
	if request.mode in ['checkid_immediate', 'checkid_setup']:
		if not fail and (request.identity.endswith(user+"/") or request.identity.endswith(user)):
			response = request.answer(True)
		else:
			response = request.answer(False)
	else:
		response = oserver.handleRequest(request)

	nResponse = "Content-Type: text/html\n"
	webresponse = oserver.encodeResponse(response)
	for i in webresponse.headers.keys():
			nResponse += i + ": " + webresponse.headers[i]
	nResponse += "\n"
	nResponse += webresponse.body
	return request, nResponse

def doOpenIDFail(result, user):
	req, resp = doOpenID(result, user, True)
	return resp

