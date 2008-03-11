from turbogears import controllers, expose, flash
from model import Child
from turbogears import identity, redirect, url
from cherrypy import request, response
from child import ChildController
from assessment import AssessmentController
from userlist import UserListController
from search import SearchController
from userprofile import UserProfileController
from admin import AdminController
import cherrypy
import os, sys
import util

# from ecaeps import json
# import logging
# log = logging.getLogger("ecaeps.controllers")

class Root(controllers.RootController):
	
	child = ChildController()
	assessment = AssessmentController()
	userlist = UserListController()
	search = SearchController()
	userprofile = UserProfileController()
	admin = AdminController()
	
	@expose()
	@identity.require(identity.in_group('global_admin'))
	def updateSVN(self, rev="HEAD"):
		os.system("bash updateme.sh %s %s" % (os.getpid(),rev))
		cherrypy.server.stop()
		raise redirect("/")
	
	@expose()
	@identity.require(identity.in_group('global_admin'))
	def shutdown(self):
		cherrypy.server.stop()
		raise redirect("/")
	
	@expose(template="ecaeps.templates.unimplemented")
	@identity.require(identity.not_anonymous())
	def unimplemented(self):
		return dict()
	
	@expose(template="ecaeps.templates.welcome")
	@identity.require(identity.not_anonymous())
	def index(self):
		return dict(childList=identity.current.user.childList, shaded=util.shaded)

	@expose()
	@identity.require(identity.not_anonymous())
	def removeChild(self,**kw):
		id = int(kw['id'])
		try:
			Child.get(id).removeUser(identity.current.user)
		except:
			pass
		if identity.current.user.childList.count() == 0:
			cherrypy.status = 500
		return dict()
	
	@expose()
	@identity.require(identity.not_anonymous())
	def amode(self):
		identity.current.user.basketmode = False
		raise redirect(url(request.headers.get("Referer", "/")))
	
	@expose()
	@identity.require(identity.not_anonymous())
	def bmode(self):
		identity.current.user.basketmode = True
		raise redirect(url(request.headers.get("Referer", "/")))
	
	@expose(template="ecaeps.templates.login")
	def login(self, forward_url=None, previous_url=None, *args, **kw):

		if not identity.current.anonymous \
			and identity.was_login_attempted() \
			and not identity.get_identity_errors():
			raise redirect(forward_url)

		forward_url=None
		previous_url= request.path

		if identity.was_login_attempted():
			msg=_("The credentials you supplied were not correct or "
				   "did not grant access to this resource.")
		elif identity.get_identity_errors():
			msg=_("For assistance, please contact your program administrator.")
		else:
			msg=_("Please log in.")
			forward_url= request.headers.get("Referer", "/")
			
		response.status=403
		return dict(message=msg, previous_url=previous_url, logging_in=True,
					original_parameters=request.params,
					forward_url=forward_url)

	@expose()
	def logout(self):
		keys = cherrypy.session.keys()
		for key in keys:
			del cherrypy.session[key]

		identity.current.logout()
		raise redirect("/")
