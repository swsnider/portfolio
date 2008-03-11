from turbogears import controllers, identity, expose, redirect, url
from model import Child, Assessment, Criterion, Score, EditHistory
from sqlobject import SQLObjectNotFound, AND
import cherrypy
import util
import csv, sys
import re
from cherrypy.lib import profiler

class AssessmentController(controllers.Controller, identity.SecureResource):
	require=identity.not_anonymous()
	
	category_list = ['Fine Motor','Gross Motor','Adaptive','Cognitive','Social-Communication','Social']
	
	def nextCategory(self):
		category = util.session('current_category', 'Fine Motor')
		for i in range(len(self.category_list)):
			if self.category_list[i] == category:
				return self.category_list[(i+1)%len(self.category_list)]
				
	def getEditor(self, id, category):
		eh = EditHistory.selectBy(assessmentID=id, category=category)
		if eh.count() > 0:
			return (eh[0].editor,eh[0].program)
		else:
			user = identity.current.user
			e = EditHistory(assessmentID=id, category=category, editor=user.firstlast(), program=user.program.name)
			return (e.editor, e.program)
	
	def persistCheck(self, name, val):
		if val == cherrypy.session[name]:
			return {'checked':'checked'}
		else:
			return {'checked':None}
	
	@expose()
	def index(self, id=None, category=None, osep="None", print_area="false"):
		if identity.current.user.basketmode:
			raise redirect(url("index2",id=id,category=category,osep=osep,print_area=print_area))
		else:
			raise redirect(url("index1",id=id,category=category,osep=osep,print_area=print_area))
	
	@expose(template="ecaeps.templates.assessment")
	def index1(self, id=None, category=None, osep='None', print_area='false'):
		if identity.current.user.basketmode:
			raise redirect(url("index2",id=id,category=category,osep=osep,print_area=print_area))
		
#		if osep is not None:
#			if osep == 'True':
#				osep = True
#			else:
#				osep = False
		osep = True
	
		if print_area == 'true':
			print_area = True
		else:
			print_area = False
		
		id = util.session('current_assessment', 0, id)
		category = util.session('current_category', 'Fine Motor', category)
		osep = util.session('osep', False, osep)
		child = util.session('current_child', 0)
		
		if id == 0:		# no id given
			raise redirect("/")
		
		try:
			current_assessment = Assessment.get(id)
		except SQLObjectNotFound:	# Child with given id does not exist
			raise redirect("/")

		current_child = current_assessment.child
		all_assessments = current_child.assessments
		
		sorted_assessments = Assessment.select(AND(Assessment.q.childID==current_assessment.childID,
												   Assessment.q.id!=id,
												   Assessment.q.level==current_assessment.level), orderBy='-dateEntered')
		old = list(sorted_assessments[:7])
		
		if osep:
			criteria = Criterion.selectBy(category=category, level=current_assessment.level, osep=True)
		else:
			criteria = Criterion.selectBy(category=category, level=current_assessment.level)
			
		criteria = criteria.orderBy('sort_order')
		
		crit_ids = [c.id for c in criteria]
		sums = {}
		
		for t in old:
			sum = 0;
			for s in t.scores:
				if s.criterionID in crit_ids and s.criterion.rank != "1":
					try:
						sum += int(s.value)
					except:
						pass
			sums[t.id] = sum
		sum = 0;
		for s in current_assessment.scores:
			if s.criterionID in crit_ids and s.criterion.rank != "1":
				try:
					sum += int(s.value)
				except:
					pass
		sums[current_assessment.id] = sum
		
		util.session('fill', 'missing')
		if len(old) == 0:
			temp = util.session('values', 'zeros')
			if temp == 'previous':
				cherrypy.session['values'] = 'zeros'
		else:
			util.session('values', 'previous')
		
		subtotal = Criterion.selectBy(category=category, level=current_assessment.level, prefix='Z')[0]
		_na = Criterion.selectBy(category=category, level=current_assessment.level, prefix='Y')[0]
		
		oldtotals = {}
		oldna = {}
		percents = {}
		for t in old:
			stscore = Score.selectBy(assessmentID=t.id, criterionID=subtotal.id)
			if stscore.count() > 0:
				stscore = stscore[0]
			else:
				stscore = Score(assessmentID=t.id, criterionID=subtotal.id, value="0", type='subtotal')
			oldtotals[t.id] = stscore.value
			
			nascore = Score.selectBy(assessmentID=t.id, criterionID=_na.id)
			if nascore.count() > 0:
				nascore = nascore[0]
			else:
				nascore = Score(assessmentID=t.id, criterionID=_na.id, value="0", type='na')
			oldna[t.id] = nascore.value
		
			percents[t.id] = util.percent(stscore.value, util.scorePossible(category, current_assessment.level), nascore.value)
			
		
		stscore = Score.selectBy(assessmentID=id, criterionID=subtotal.id)
		nascore = Score.selectBy(assessmentID=id, criterionID=_na.id)
		if stscore.count() > 0:
			stscore = stscore[0]
		else:
			stscore = Score(assessmentID=id, criterionID=subtotal.id, value="0", type='subtotal')
		
		if nascore.count() > 0:
			nascore = nascore[0]
		else:
			nascore = Score(assessmentID=id, criterionID=_na.id, value="0", type='na')
			
		percent = util.percent(stscore.value, util.scorePossible(category, current_assessment.level), nascore.value)
		
		return dict(child=current_child, id=id, a=current_assessment, old=old, oldtotals=oldtotals, \
					stc=subtotal, subtotal=stscore, criteria=criteria, osep=osep, sums=sums, \
					catlist=self.category_list, category=category, nextCategory=self.nextCategory, \
					print_area=print_area, getEditor=self.getEditor, pcheck=self.persistCheck, \
					shaded=util.shaded, scoreclass=util.color, scorePossible=util.scorePossible, \
					nac=_na, na=nascore, oldna=oldna, percents=percents, percent=percent)
	
	@expose()
	def newAssessment(self, level, childid = 0):
		if childid != 0:
			cherrypy.session['current_child'] = int(childid)
		if 'current_child' in cherrypy.session:		
			a = Assessment(childID=cherrypy.session['current_child'], ownerID=identity.current.user.id, level=level)
			raise redirect("/assessment?id=" + str(a.id))			
		raise redirect("/")
	
	@expose()
	def assessmentUpdate(self, **kw):
		field = str(kw['field'])
		type = kw['type']
		id = cherrypy.session['current_assessment']

		if type == 'string':
			value = str(kw['value'])
		elif type == 'int':
			value = int(kw['value'])
		elif type == 'date':
			value = str(kw['value'])

		display = value

		if field == 'dateEntered':
			try:
				value = util.valiDate(value)
			except:
				cherrypy.response.status = 412
				return Assessment.get(id).dateEntered.strftime("%m/%d/%y")
			
			if value is None:
				cherrypy.response.status = 412
				return Assessment.get(id).dateEntered.strftime("%m/%d/%y")
			display = value.strftime("%m/%d/%y")

		Assessment.get(id).__setattr__(field, value)
		
		category = cherrypy.session['current_category']
		user = identity.current.user
		
		eh = EditHistory.selectBy(assessmentID=id, category=category)
		if eh.count() > 0:
			eh[0].editor = user.firstlast()
			eh[0].program = user.program.name
		else:
			EditHistory(assessmentID=id, category=category, editor=user.firstlast(), program=user.program.name)
		
		return display
	
	@expose()
	def fillUpdate(self, **kw):
		
		assessment = Assessment.get(cherrypy.session['current_assessment'])
		category = cherrypy.session['current_category']
		
		fill = kw['fill']
		value = kw['values']

		cherrypy.session['fill'] = fill
		cherrypy.session['values'] = value

		scores = assessment.scores
		criteria = Criterion.selectBy(category=category, level=assessment.level)
		
		if value == 'previous':
			sorted_assessments = Assessment.select(AND(Assessment.q.childID==assessment.childID,
													   Assessment.q.id!=assessment.id), orderBy='-dateEntered')
			previous = sorted_assessments[0]
		
		for c in criteria:
			score = Score.selectBy(criterionID=c.id, assessmentID=assessment.id, type='score')
			if score.count() == 0:
				if value == 'previous':
					temp = Score.selectBy(criterionID=c.id, assessmentID=previous.id, type='score')
					if temp.count() > 0:
						Score(value=temp[0].value, criterionID=c.id, assessmentID=assessment.id, type='score')
				elif value == 'zeros':
					Score(value="0", criterionID=c.id, assessmentID=assessment.id, type='score')
				elif value == 'twos':
					Score(value="2", criterionID=c.id, assessmentID=assessment.id, type='score')
			elif score[0].value not in ['0','1','2','#'] or fill == 'all':
				if value == 'previous':
					temp = Score.selectBy(criterionID=c.id, assessmentID=previous.id, type='score')
					if temp.count() > 0:
						score[0].value = temp[0].value
				elif value == 'zeros':
					score[0].value = "0"
				elif value == 'twos':
					score[0].value = "2"
			
		user = identity.current.user
		eh = EditHistory.selectBy(assessmentID=assessment.id, category=category)
		if eh.count() > 0:
			eh[0].editor = user.firstlast()
			eh[0].program = user.program.name
		else:
			EditHistory(assessmentID=assessment.id, category=category, editor=user.firstlast(), program=user.program.name)
		
		raise redirect("/assessment")
	
	
	@expose()
	def scoreUpdate(self, **kw):
		print "-------------"
		print kw
		id = kw['id']
		value = kw['value']
				
		score = Score.get(int(id))
		crit = score.criterion
		assessment = score.assessment
		category = crit.category
		
		score.value = value
			
		user = identity.current.user		
		eh = EditHistory.selectBy(assessmentID=assessment.id, category=category)
		if eh.count() > 0:
			eh[0].editor = user.firstlast()
			eh[0].program = user.program.name
		else:
			EditHistory(assessmentID=assessment.id, category=category, editor=user.firstlast(), program=user.program.name)
		
		if crit.prefix in ['Y','Z']:
			st_crit = Criterion.selectBy(level=assessment.level, category=category, prefix="Z")[0]
			na_crit = Criterion.selectBy(level=assessment.level, category=category, prefix="Y")[0]
			
			possible = util.scorePossible(category, assessment.level)
			subtotal = Score.selectBy(criterionID=st_crit.id, assessmentID=assessment.id)[0].value
			na = Score.selectBy(criterionID=na_crit.id, assessmentID=assessment.id)[0].value
			
			return str(util.percent(subtotal,possible,na))
			
		return dict()

	@expose()
	def quit(self):
		sys.exit(0)
		
	@expose(template="ecaeps.templates.assessment2")
	def index2(self, id=None, category=None, osep='None', print_area='false'):
		if not identity.current.user.basketmode:
			raise redirect(url("index1",id=id,category=category,osep=osep,print_area=print_area))
		
		osep = True

		if print_area == 'true':
			print_area = True
		else:
			print_area = False

		id = util.session('current_assessment', 0, id)
		child = util.session('current_child', 0)

		if id == 0:		# no id given
			raise redirect("/")

		try:
			current_assessment = Assessment.get(id)
		except SQLObjectNotFound:	# Child with given id does not exist
			raise redirect("/")

		current_child = current_assessment.child
		all_assessments = current_child.assessments
		sorted_assessments = Assessment.select(AND(Assessment.q.childID==current_assessment.childID,
												   Assessment.q.id!=id,
												   Assessment.q.level==current_assessment.level), orderBy='-dateEntered')
		old = list(sorted_assessments[:7])


		categories = self.category_list
		data = {}

		for c in categories:
			cdata = {}
			
			subtotal = Criterion.selectBy(category=c, level=current_assessment.level, prefix='Z')[0]
			_na = Criterion.selectBy(category=c, level=current_assessment.level, prefix='Y')[0]

			cdata['subtotal'] = subtotal
			cdata['na'] = _na

			oldtotals = {}
			oldna = {}
			percents = {}
			for t in old:
				stscore = Score.selectBy(assessmentID=t.id, criterionID=subtotal.id)
				if stscore.count() > 0:
					stscore = stscore[0]
				else:
					stscore = Score(assessmentID=t.id, criterionID=subtotal.id, value="0", type='subtotal')
				oldtotals[t.id] = stscore.value

				nascore = Score.selectBy(assessmentID=t.id, criterionID=_na.id)
				if nascore.count() > 0:
					nascore = nascore[0]
				else:
					nascore = Score(assessmentID=t.id, criterionID=_na.id, value="0", type='na')
				oldna[t.id] = nascore.value

				percents[t.id] = util.percent(stscore.value, util.scorePossible(c, current_assessment.level), nascore.value)
			
			cdata['oldtotals'] = oldtotals
			cdata['oldna'] = oldna
			cdata['percents'] = percents

			stscore = Score.selectBy(assessmentID=id, criterionID=subtotal.id)
			nascore = Score.selectBy(assessmentID=id, criterionID=_na.id)
			if stscore.count() > 0:
				stscore = stscore[0]
			else:
				stscore = Score(assessmentID=id, criterionID=subtotal.id, value="0", type='subtotal')

			if nascore.count() > 0:
				nascore = nascore[0]
			else:
				nascore = Score(assessmentID=id, criterionID=_na.id, value="0", type='na')

			percent = util.percent(stscore.value, util.scorePossible(c, current_assessment.level), nascore.value)
			
			cdata['stscore'] = stscore
			cdata['nascore'] = nascore
			cdata['percent'] = percent
			
			data[c] = cdata
			
		baskets = []
		for i in [1,2,3]:
			
			bdata = {}
			
			prefix = "B" + str(i)
			b = Criterion.selectBy(level=current_assessment.level, prefix=prefix)[0]
			
			oldb = {}
			for t in old:
				bscore = Score.selectBy(assessmentID=t.id, criterionID=b.id)
				if bscore.count() > 0:
					bscore = bscore[0]
				else:
					bscore = Score(assessmentID=t.id, criterionID=b.id, value="0", type='basket')
				oldb[t.id] = bscore
			bdata['old'] = oldb
			
			bscore = Score.selectBy(assessmentID=id, criterionID=b.id)
			if bscore.count() > 0:
				bscore = bscore[0]
			else:
				bscore = Score(assessmentID=id, criterionID=b.id, value="0", type='basket')
			bdata['val'] = bscore
			baskets.append(bdata)

		return dict(child=current_child, id=id, a=current_assessment, old=old, categories=categories, \
					print_area=print_area, getEditor=self.getEditor, pcheck=self.persistCheck, \
					shaded=util.shaded, scoreclass=util.color, scorePossible=util.scorePossible, \
					data=data, baskets=baskets)
	