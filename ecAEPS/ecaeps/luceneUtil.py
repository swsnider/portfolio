import lucene
import turbogears
import sys

# To use this library:
#
# Add rowDeleted, rowAdded, and rowUpdated as deleted, added, and updated listeners to the correct SQLObject model
# 
# Initialize the index by calling initIndex with the SQLObject table class that you want to index
# 
# To search the index, call doSearch with a lucene query string. The optional field parameter is the field in each lucene document that contains the database id for the document.

try:
	lucene.initVM(lucene.CLASSPATH)
except:
	sys.stderr.write("Lucene already inited!\n")


class LuceneFileCache(object):
	instance = None
	struct = None
	def __new__(cls, *args, **kwargs):
		print "new called"
		if cls.instance is None:
			cls.instance = object.__new__(cls, *args, **kwargs)
		return cls.instance
	def get_field_struct(self, redo=False):
		if redo or self.struct is None:
			f = open("lucene.gen", "r")
			var = f.read()
			f.close()
			var = eval(var)
			self.struct = var
		return self.struct
	@classmethod
	def getValue(cls, l_field,baseObj="c"):
		if l_field["value"] == "":
			return baseObj + "." + l_field['name']
		else:
			return l_field['value']

def getAnalyzer():
	return lucene.StandardAnalyzer()

def getWriter(store, analyzer, create=False):
	return lucene.IndexWriter(store, analyzer, create)

def delLock():
	import os
	path = turbogears.config.get("lucene.indexdir")
	os.remove(path + "/write.lock")

def getSearcher(store):
	return lucene.IndexSearcher(store)

def getStore():
	path = turbogears.config.get("lucene.indexdir")
	return lucene.FSDirectory.getDirectory(path)

def getReader(store):
	return lucene.IndexReader.open(store)

def initIndex(tbl):
	lucene.getVMEnv().attachCurrentThread()
	writer = getWriter(getStore(), getAnalyzer(), True)
	STORE = lucene.Field.Store.YES
	COMPRESS = lucene.Field.Store.COMPRESS
	TOKENIZED = lucene.Field.Index.TOKENIZED
	UN_TOKENIZED = lucene.Field.Index.UN_TOKENIZED
	children = tbl.select()
	lfc = LuceneFileCache().get_field_struct()
	if len(lfc['modules']) != 0:
		modules = map(__import__, lfc['modules'])
	acc = 0
	for c in children:
		acc += 1
		if acc % 100 == 0:
			print acc
		doc = lucene.Document()
		doc.add(lucene.Field("id", unicode(c.id), STORE, UN_TOKENIZED))
		for i in lfc['fields']:
			doc.add(lucene.Field(i['name'], unicode(eval(LuceneFileCache.getValue(i))), COMPRESS, TOKENIZED))
		writer.addDocument(doc)
	writer.optimize(True)
	writer.close()


def reindex(c):
	if "id" not in c.__dict__:
		return
	lucene.getVMEnv().attachCurrentThread()
	try:
		writer = getWriter(getStore(), getAnalyzer())
		STORE = lucene.Field.Store.YES
		COMPRESS = lucene.Field.Store.COMPRESS
		TOKENIZED = lucene.Field.Index.TOKENIZED
		UN_TOKENIZED = lucene.Field.Index.UN_TOKENIZED
		doc = lucene.Document()
		doc.add(lucene.Field("id", unicode(c.id), STORE, UN_TOKENIZED))
		lfc = LuceneFileCache().get_field_struct()
		if len(lfc['modules']) != 0:
			modules = map(__import__, lfc['modules'])
		for i in lfc['fields']:
			doc.add(lucene.Field(i['name'], unicode(eval(LuceneFileCache.getValue(i))), COMPRESS, TOKENIZED))
		writer.deleteDocuments(lucene.Term("id", unicode(c.id)))
		writer.addDocument(doc)
		writer.optimize(True)
		writer.close()
	except:
		print "Failed in reindex of " + unicode(c.id) + "!"
		delLock()

def doSearch(queryS, field="id"):
	lucene.getVMEnv().attachCurrentThread()
	lucene.BooleanQuery.setMaxClauseCount(sys.maxint)
	store = getStore()
	searcher = getSearcher(store)
	analyzer = getAnalyzer()
	parser = lucene.QueryParser("ssid", analyzer)
	query = parser.parse(queryS)
	query = query.rewrite(getReader(store))
	hits = searcher.search(query)
	
	results = []
	
	for i in range(0, hits.length()):
		results.append(hits.doc(i).get(field))
	
	searcher.close()
	store.close()
			
	return results

def rowDeleted(*args, **kw):
	print "id: " + str(args[0].id) + " is scheduled for termintation"
	lucene.getVMEnv().attachCurrentThread()
	try:
		writer = getWriter(getStore(), getAnalyzer())
		writer.deleteDocuments(lucene.Term("id", unicode(args[0].id)))
		writer.optimize(True)
		writer.close()
	except:
		print "Failed in deletion of " + unicode(args[0].id) + " from lucene"
		delLock()


def rowAdded(*args, **kw):
	print "Row added!"
	args[1].append(reindex)

def rowUpdated(*args, **kw):
	if "isDirty" in args[0].__dict__ and  args[0].isDirty:
		args[0].isDirty = False
		return
	print "id: " + str(args[0].id) + " is scheduled for updating"
	reindex(args[0])
