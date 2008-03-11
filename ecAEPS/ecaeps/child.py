from turbogears import controllers, identity, expose, redirect, url
from model import Child, Assessment, Score
from sqlobject import SQLObjectNotFound
import cherrypy
import util

class ChildController(controllers.Controller, identity.SecureResource):
	require=identity.not_anonymous()
	
	@expose(template="ecaeps.templates.child")
	def index(self, id=None):
		
		id = util.session('current_child', 0, id)
		
		if id == 0:		# no id given
			raise redirect("/")
		
		try:
			current_child = Child.get(id)
		except SQLObjectNotFound:	# Child with given id does not exist
			raise redirect("/")
		
		return dict(child=current_child, shaded=util.shaded)
			
	@expose()
	def childUpdate(self, **kw):
		field = str(kw['field'])
		type = kw['type']
		id = cherrypy.session['current_child']
		
		if type == 'string':
			value = str(kw['value'])
		elif type == 'int':
			value = int(kw['value'])
		elif type == 'date':
			value = str(kw['value'])
		
		display = value
		
		if field == 'ssid':
			if not value.isdigit():
				cherrypy.response.status = 412
				return "SSID must be all digits"
			if len(value) < 8 or len(value) > 10:
				cherrypy.response.status = 412
				return "SSID must be between 8 and 10 digits"
			if Child.selectBy(ssid=value).count() > 0:
				cherrypy.response.status = 412
				return "SSID already exists"
		
		if field == 'bdate':
			try:
				value = util.valiDate(value)
			except:
				cherrypy.response.status = 412
				return "Invalid date entered"
			
			if value is None:
				cherrypy.response.status = 412
				return "Invalid date entered"
			display = value.strftime("%m/%d/%y")
			 
		Child.get(id).__setattr__(field, value)
		
		return display
		
	@expose()
	def deleteAssessment(self, **kw):
		id = int(kw['id'])
		
		try:
			scores = Assessment.get(id).scores
			for s in scores:
				Score.delete(s.id)
			Assessment.delete(id)
		except SQLObjectNotFound:
			pass

		if len(Child.get(cherrypy.session['current_child']).assessments) == 0:
			print "*****"
			print len(Child.get(cherrypy.session['current_child']).assessments)
			cherrypy.response.status = 500

		return dict()
		
	@expose()
	def createNewChild(self):
		child = Child()
		raise redirect('/child',id=child.id)
		