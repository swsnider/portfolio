from turbogears import controllers, identity, expose, redirect, url
from model import Program, User, Assessment
from sqlobject import SQLObjectNotFound
import cherrypy
import util

class UserListController(controllers.Controller, identity.SecureResource):
	require=identity.in_any_group('admin','global_admin')
	
	def curProg(self, programid):
		if int(util.session('current_program', identity.current.user.programID)) == int(programid):
			return {'selected':'selected'}
		return {'selected':None}
	
	@expose(template="ecaeps.templates.userlist")
	@identity.require(identity.in_any_group("admin","global_admin"))
	def index(self, program=None):
		program = util.session('current_program', identity.current.user.programID, program)
		if identity.in_group('global_admin') and int(program) == 0:
			userlist = User.select()
			program = identity.current.user.programID
		elif int(program) == 0:
			program = identity.current.user.programID
			userlist = User.selectBy(programID=program)
		else:
			userlist = User.selectBy(programID=program)
		programlist = Program.select()

		return dict(program=Program.get(program), programlist=programlist, curProg=self.curProg, userlist=userlist, shaded=util.shaded)
		
	@expose()
	@identity.require(identity.in_group("global_admin"))
	def deleteUser(self, **kw):
		id = int(kw['id'])
		User.delete(id)
		return dict()