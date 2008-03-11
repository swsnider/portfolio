from datetime import datetime
from turbogears.database import PackageHub
from sqlobject import *
from turbogears import identity
from luceneUtil import reindex

hub = PackageHub('ecaeps')
__connection__ = hub

# class YourDataClass(SQLObject):
#	  pass

# identity models.
class Visit(SQLObject):
	"""
	A visit to your site
	"""
	class sqlmeta:
		table = 'visit'

	visit_key = StringCol(length=40, alternateID=True,
						  alternateMethodName='by_visit_key')
	created = DateTimeCol(default=datetime.now)
	expiry = DateTimeCol()

	def lookup_visit(cls, visit_key):
		try:
			return cls.by_visit_key(visit_key)
		except SQLObjectNotFound:
			return None
	lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
	"""
	A Visit that is link to a User object
	"""
	visit_key = StringCol(length=40, alternateID=True,
						  alternateMethodName='by_visit_key')
	user_id = IntCol()


class Group(SQLObject):
	"""
	An ultra-simple group definition.
	"""
	# names like "Group", "Order" and "User" are reserved words in SQL
	# so we set the name to something safe for SQL
	class sqlmeta:
		table = 'tg_group'

	group_name = UnicodeCol(length=16, alternateID=True,
							alternateMethodName='by_group_name')
	display_name = UnicodeCol(length=255)
	created = DateTimeCol(default=datetime.now)

	# collection of all users belonging to this group
	users = RelatedJoin('User', intermediateTable='user_group',
						joinColumn='group_id', otherColumn='user_id')

	# collection of all permissions for this group
	permissions = RelatedJoin('Permission', joinColumn='group_id',
							  intermediateTable='group_permission',
							  otherColumn='permission_id')


class User(SQLObject):
	"""
	Reasonably basic User definition.
	Probably would want additional attributes.
	"""
	# names like "Group", "Order" and "User" are reserved words in SQL
	# so we set the name to something safe for SQL
	class sqlmeta:
		table = 'tg_user'

	user_name = UnicodeCol(length=16, alternateID=True,
						   alternateMethodName='by_user_name')
	email_address = UnicodeCol(default='', length=255)
	display_name = UnicodeCol(default='', length=255)
	fname = UnicodeCol(default='', length=100, notNone=True)
	lname = UnicodeCol(default='', length=100, notNone=True)
	phone = UnicodeCol(default='', length=100, notNone=True)
	program = ForeignKey("Program")
	password = UnicodeCol(length=40)
	created = DateTimeCol(default=datetime.now)
	isdirty = BoolCol(default=True)
	basketmode = BoolCol(default=False)
	assessments = MultipleJoin("Assessment", joinColumn="owner_id")
	childList = RelatedJoin("Child", intermediateTable="user_child", joinColumn="user_id", otherColumn="child_id")

	# groups this user belongs to
	groups = RelatedJoin('Group', intermediateTable='user_group',
						 joinColumn='user_id', otherColumn='group_id')

	def firstlast(self):
		return self.fname + " " + self.lname

	def _get_permissions(self):
		perms = set()
		for g in self.groups:
			perms = perms | set(g.permissions)
		return perms

	def _set_password(self, cleartext_password):
		"Runs cleartext_password through the hash algorithm before saving."
		password_hash = identity.encrypt_password(cleartext_password)
		self._SO_set_password(password_hash)

	def set_password_raw(self, password):
		"Saves the password as-is to the database."
		self._SO_set_password(password)


class Permission(SQLObject):
	"""
	A relationship that determines what each Group can do
	"""
	permission_name = UnicodeCol(length=16, alternateID=True,
								 alternateMethodName='by_permission_name')
	description = UnicodeCol(length=255)

	groups = RelatedJoin('Group',
						 intermediateTable='group_permission',
						 joinColumn='permission_id',
						 otherColumn='group_id')

class NoAssessment(object):
	@property
	def id(self):
		return 0
	@property
	def dateEntered(self):
		return "add 1st assessment"
	@property
	def display_dateEntered(self):
		return "add 1st assessment"

class Child(SQLObject):
	lname = UnicodeCol(default='', length=100, notNone=True)
	fname = UnicodeCol(default='', length=100, notNone=True)
	mname = UnicodeCol(default='', length=100, notNone=True)
	bdate = DateCol(default=None)
	ssid = UnicodeCol(default='', length=10, notNone=True)
	assessments = MultipleJoin("Assessment", joinColumn="child_id")
	listedOn = RelatedJoin("User", intermediateTable="user_child", joinColumn="child_id", otherColumn="user_id")
	
	def firstlast(self):
		return self.fname + " " + self.lname
	
	@property
	def display_bdate(self):
		if self.bdate is not None:
			return self.bdate.strftime("%m/%d/%y")
		else:
			return ""
	
	@property
	def lastAssessment(self):
		a = list(self.assessments)
		if len(a) == 0:
			return NoAssessment()
		a.sort(lambda x,y: cmp(y.dateEntered, x.dateEntered))
		return a[0]


class Assessment(SQLObject):
	level = EnumCol(enumValues=['I','II'], notNone=True)
	child = ForeignKey("Child")
	owner = ForeignKey("User")
	dateEntered = DateCol(notNone=True, default=datetime.now)
	scores = MultipleJoin("Score")
	edits = MultipleJoin("EditHistory", joinColumn="assessment_id")
	
	@property
	def display_dateEntered(self):
		if self.dateEntered is not None:
			return self.dateEntered.strftime("%m/%d/%y")
		else:
			return ""

class EditHistory(SQLObject):
	assessment = ForeignKey("Assessment")
	editor = UnicodeCol(default="None", length=100, notNone=True)
	program = UnicodeCol(default="", length=100, notNone=True)
	category = EnumCol(default='', enumValues=['','Fine Motor','Gross Motor', 'Adaptive','Cognitive','Social-Communication','Social'], title='Category')	

class Program(SQLObject):
	name = UnicodeCol(length=100, notNone=True)
	users = MultipleJoin("User", joinColumn="user_id")

class Score(SQLObject):
	criterion = ForeignKey("Criterion")
	assessment = ForeignKey("Assessment")
	value = UnicodeCol(length=2, notNone=True)
	type = EnumCol(default='score', enumValues=['score','subtotal','na','basket'], title="Type")
	def _set_value(self,v):
		if v == u'~' or v == u'`':
			v = u"0"
		if self.type in ['na','subtotal','basket'] or v in [u"0",u"1",u"2",u"#"]:
			self._SO_set_value(v)

class Criterion(SQLObject):
	level = EnumCol(enumValues=['I','II'], notNone=True)
	rank = EnumCol(default='3', enumValues=['1','2','3','4'])
	category = EnumCol(default='', enumValues=['','Fine Motor','Gross Motor', 'Adaptive','Cognitive','Social-Communication','Social'], title='Category')	
	osep = BoolCol(notNone=True, default=False)
	sort_order = IntCol(default=0, notNone=True)
	name = UnicodeCol(notNone=True)
	prefix = UnicodeCol(notNone=True)
	
	@property
	def display_name(self):
		return self.prefix + " " + self.name