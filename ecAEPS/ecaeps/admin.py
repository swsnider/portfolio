from turbogears import controllers, identity, expose, redirect, url
from model import Program, User, Assessment, Group, Criterion, Child
from sqlobject import SQLObjectNotFound, dberrors
import cherrypy
import util
from random import Random
import string
import csv
import re

class AdminController(controllers.Controller, identity.SecureResource):
	require=identity.in_group('global_admin')
			
	@expose(template="ecaeps.templates.admin")
	def index(self, message=None):
		return dict(message=message)
	
	@expose()
	def addProgram(self, name):
		p = Program.selectBy(name=name)
		if p.count() == 0:
			Program(name=name)
			raise redirect("/admin")
		else:
			raise redirect("/admin?message='A program with this name already exists'")
	
	@expose()
	def uploadCriteria(self, filename):	
		f = open(filename,"r")
		f_data = f.read()
		f.close()

		f_data = re.sub("\\r","\\n",f_data)

		f = open(filename,"w")
		f.write(f_data)
		f.close()	

		reader = csv.reader(open(filename,"r"))

		Criterion._connection.queryAll("TRUNCATE ecaeps.criterion")

		order = 0;
		for row in reader:
			print row
			osep = row[0]
			level = row[1]
			area = row[2]
			number = row[3]
			task = row[4]

			if osep == "1":
				osep=True
			else:
				osep=False

			if level == '1':
				level = 'I'
			else:
				level = 'II'

			if(re.match("[a-zA-Z]\.",number) is not None):
				rank = '1'
			elif(re.match("[0-9]\.[0-9]",number) is not None):
				rank = '3'
			else:
				rank = '2'

			order = order + 1
			Criterion(prefix=number.encode('utf-8'), name=task.encode('utf-8'), osep=osep, category=area, level=level, rank=rank, sort_order=order)

		for level in ['I','II']:
			for cat in ['Fine Motor','Gross Motor','Adaptive','Cognitive','Social-Communication','Social']:
				order=order+1
				Criterion(prefix="Z", name="Subtotal", osep=false, category=cat, level=level, rank=4, sort_order=order)
				order=order+1
				Criterion(prefix="Y", name="Subtotal", osep=false, category=cat, level=level, rank=4, sort_order=order)
			for b in ['B1','B2','B3']:
				order=order+1
				Criterion(prefix=b, name="Basket "+b[1], osep=false, level=level, rank=4, sort_order=order)

		raise redirect("/assessment")

	@expose()
	def uploadChildren(self, filename):	
		f = open(filename,"r")
		f_data = f.read()
		f.close()

		f_data = re.sub("\\r","\\n",f_data)

		f = open(filename,"w")
		f.write(f_data)
		f.close()	

		reader = csv.reader(open(filename,"r"))

		Criterion._connection.queryAll("TRUNCATE ecaeps.child")

		order = 0;
		for row in reader:
			print row
			ssid = row[0]
			bdate = row[1]
			lname = row[2]
			fname = row[3]
			mname = row[4]
			Child(ssid=ssid, lname=lname.decode('utf-8'), fname=fname.decode('utf-8'), mname=mname.decode('utf-8'), bdate=bdate)

		raise redirect(url("/search"))