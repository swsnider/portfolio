from turbogears import controllers, identity, expose, redirect, url
from model import Child, Assessment, User
import luceneUtil
import cherrypy
import util
from sqlobject import IN

class SearchController(controllers.Controller, identity.SecureResource):
	require=identity.not_anonymous()
	
	def sort_strip(self, slist):
		for s in slist:
			if s[0] == '-':
				s[0] == s[0][1:]
		return slist

	def get_symbol(self, name):
		sort = cherrypy.session['sort'][0]
		if sort == '-' + name:
			return u"\u25B2"
		if sort == name:
			return u"\u25BC"
		return u"\u25BD"

	@expose(template="ecaeps.templates.search")
	def index(self, sort=None):
		resort = False
		if sort is not None:
			resort = True
			sort = sort.split(',')
		
		ssort = util.session('sort',['lname','fname'])
		if sort == self.sort_strip(ssort):
			if ssort[0][0] != '-':
				sort[0] = "-" + ssort[0]
			cherrypy.session['sort'] = sort
		else:
			sort = util.session('sort',['lname','fname'],sort)
		
		sort = [s.encode('ascii') for s in sort] # sqlobject selectResults.orderBy() can't handle unicode strings
		
		if 'results' in cherrypy.session:
			childlist = [child.id for child in identity.current.user.childList]
			results = cherrypy.session['results']
			if resort:
				results = results.orderBy(sort)
				cherrypy.session['results'] = results
			return dict(results=results, childlist=childlist, size=results.count(), shaded=util.shaded, sym=self.get_symbol)
		return dict(results=[], size=-1, shaded=util.shaded, sym=self.get_symbol)
	
	@expose()
	def deleteChild(self, id):
		child = Child.get(id)
		for a in child.assessments:
			Assessment.delete(a.id)
		Child.delete(id)
		
	@expose()
	def addChild(self, id):
		user = User.get(util.session('current_user', identity.current.user.id))
		user.addChild(id)
		return dict()
		
	@expose()
	def removeChild(self, id):
		user = User.get(util.session('current_user', identity.current.user.id))
		user.removeChild(id)
		return dict()
		
	@expose(template="ecaeps.templates.search")
	def search(self, **kw):
		sort = util.session('sort',['lname','fname'])
		stripchars = "*?"
		
		# Get values from the form
		ssid = str(kw['search_ssid']).strip(stripchars)
		name = str(kw['search_name']).strip(stripchars)
		bdate = str(kw['search_birthdate']).strip(stripchars)
		
		childlist = [child.id for child in identity.current.user.childList]
		
		if "".join([ssid,name,bdate]) == "":
			results = Child.select(orderBy=sort)
			cherrypy.session['results'] = results
			return dict(results=results, childlist=childlist, size=results.count(), shaded=util.shaded, sym=self.get_symbol)
		
		# DO LUCENE STUFF		
		
		query=[]
		
		fields = {'ssid':ssid, 'name':name, 'bdate':bdate}	
		for f in fields.keys():
		 	field = fields[f]
			flist = field.split(' ')
			for item in flist:
				if len(item) > 0:
					query.append("(" + f + ":" + item + "*)")
		
		print " AND ".join(query)
		
		#this is a list of (string) database ids that matched
		listOfIds = luceneUtil.doSearch(" AND ".join(query))
		
		print listOfIds
		
		if len(listOfIds) == 0:
			results = []
		else:
			results = Child.select(IN(Child.q.id,[int(i) for i in listOfIds]), orderBy=sort)
			cherrypy.session['results'] = results
		
		return dict(results=results, childlist=childlist, size=len(listOfIds), shaded=util.shaded, sym=self.get_symbol)
