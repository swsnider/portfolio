from turbogears import controllers, identity, expose, redirect, url
from model import Program, User, Assessment, Group, Criterion, Child
from sqlobject import SQLObjectNotFound, dberrors
import cherrypy
import util
from random import Random
import string
import csv
import re

class UserProfileController(controllers.Controller, identity.SecureResource):
	require=identity.not_anonymous()
	
	def curProg(self, programid):
		user_id = int(util.session('current_user', identity.current.user.id))
		
		if int(user_id) == 0:
			return {'selected':None}
		
		if User.get(user_id).programID == int(programid):
			return {'selected':'selected'}
		return {'selected':None}
		
	def curGroup(self, name):
		id = util.session('current_user', identity.current.user.id)		
		user = User.get(id)
		groups = [g.group_name for g in user.groups]
		
		if name in groups:
			return {'checked':'checked'}
		else:
			return {'checked':None}
			
	@expose(template="ecaeps.templates.userprofile")
	def index(self, id=None, message=""):
		
		id = util.session('current_user', identity.current.user.id, id)
		if int(id) == 0:
			raise redirect('/userprofile/createUser?message=message')
		
		user = User.get(id)
		groups = [g.group_name for g in user.groups]
		programlist = Program.select()
		
		return dict(user=user, programlist=programlist, curProg=self.curProg, curGroup=self.curGroup, groups=groups, message=message)
	
	@expose(template="ecaeps.templates.createuser")
	def createUser(self, message=""):
		return dict(message=message)
	
	@expose()
	def validateUser(self, **kw):
		
		username = kw['username']
		password = kw['password']
		retype = kw['retype']
		
		program = util.session('current_program', identity.current.user.programID)
		
		if password != retype:
			raise redirect("/userprofile?id=0&message=Password+and+retype+do+not+match")
		
		try:
			user = User(user_name=username, password=password, programID=program)
		except:
			raise redirect("/userprofile?id=0&message=Username+already+taken")
		
		#return "SUCCESS"
		raise redirect("/userprofile?id=" + str(user.id))
		
	@expose()
	def userUpdate(self, **kw):
		field = str(kw['field'])
		type = kw['type']
		id = cherrypy.session['current_user']

		if type == 'string':
			value = str(kw['value'])
		elif type == 'int':
			value = int(kw['value'])
		elif type == 'date':
			value = str(kw['value'])

		User.get(id).__setattr__(field, value)

		return dict()
		
	@expose()
	def groupUpdate(self, **kw):
		user = User.get(int(cherrypy.session['current_user']))
		group = Group.selectBy(group_name=str(kw['name']))[0]
		if kw['value'] == 'true':
			user.addGroup(group.id)
		else:
			user.removeGroup(group.id)

		return dict()
		
	@expose()
	def programUpdate(self, **kw):
		user = User.get(int(cherrypy.session['current_user']))
		user.programID = int(kw['value'])
		return dict()

	@expose()
	@identity.require(identity.in_group("global_admin"))
	def changeUser(self):
		user = User.get(int(cherrypy.session['current_user']))
		identity.current.logout()
		temp = user.password
		user._set_password("jamesbond");

		ident = identity.current_provider.validate_identity(user.user_name,"jamesbond",cherrypy.request.tg_visit.key)
		if not ident:
			ident = tg.identity.current_provider.anonymous_identity()
			
		identity.set_current_identity(ident)
		user.set_password_raw(temp)
		raise redirect("/userprofile")
		
	@expose()
	def changePassword(self, **kw):
		user = User.get(int(cherrypy.session['current_user']))
		
		print kw
		
		old = kw['old']
		password = kw['new']
		retype = kw['retype']
		
		if identity.encrypt_password(old) != user.password:
			cherrypy.response.status = 412
			return "Old password incorrect"
			
		if password != retype:
			cherrypy.response.status = 412
			return "New password does not match retyped password"

		if password == '':
			cherrypy.response.status = 412
			return "Password cannot be blank"

		user.password = password
		return "Password changed!"
