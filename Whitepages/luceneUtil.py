import lucene
import sys, os

INDEX_DIR = "/var/lib/whitepages/"

try:
    lucene.initVM(lucene.CLASSPATH)
except:
    sys.stderr.write("Lucene already inited!\n")

def getAnalyzer():
    return lucene.StandardAnalyzer()

def getWriter(store, analyzer, create=False):
    return lucene.IndexWriter(store, analyzer, create)

def delLock():
    global INDEX_DIR
    try:
        path = INDEX_DIR
        os.remove(os.path.join(path, "write.lock"))
    except:
        pass

def getSearcher(store):
    return lucene.IndexSearcher(store)

def getStore():
    global INDEX_DIR
    path = INDEX_DIR
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
    rowset = tbl.select()
    acc = 0
    for row in rowset:
        acc += 1
        if acc == 100:
            acc = 0
            sys.stdout.write(".")
            sys.stdout.flush()
        #Begin Lucene copy section
        doc = lucene.Document()
        doc.add(lucene.Field("id", unicode(row.id), STORE, UN_TOKENIZED))
        doc.add(lucene.Field('data', unicode(row.data), COMPRESS, TOKENIZED))
        doc.add(lucene.Field('source', unicode(row.source), COMPRESS, TOKENIZED))
        #End Lucene copy section
        writer.addDocument(doc)
    print "|"
    writer.optimize(True)
    writer.close()


def reindex(row):
    if "id" not in row.__dict__:
        return
    lucene.getVMEnv().attachCurrentThread()
    try:
        writer = getWriter(getStore(), getAnalyzer())
        #print "got Writer"
        STORE = lucene.Field.Store.YES
        COMPRESS = lucene.Field.Store.COMPRESS
        TOKENIZED = lucene.Field.Index.TOKENIZED
        UN_TOKENIZED = lucene.Field.Index.UN_TOKENIZED
        #Begin Lucene copy section
        doc = lucene.Document()
        #print "created new document"
        doc.add(lucene.Field("id", unicode(row.id), STORE, UN_TOKENIZED))
        #print "added id field"
        doc.add(lucene.Field('data', unicode(row.data), COMPRESS, TOKENIZED))
        doc.add(lucene.Field('source', unicode(row.source), COMPRESS, TOKENIZED))
        #End Lucene copy section
        writer.deleteDocuments(lucene.Term("id", unicode(row.id)))
        #print "deleted existing document"
        writer.addDocument(doc)
        #print "added document"
        writer.optimize(True)
        #print "optimized index"
        writer.close()
        #print "closed writer"
    except:
        print "Failed in reindex of " + unicode(row.id) + "!"
        delLock()

def doSearch(queryS, field="id", defaultField="data"):
    lucene.getVMEnv().attachCurrentThread()
    store = getStore()
    searcher = getSearcher(store)
    analyzer = getAnalyzer()
    parser = lucene.QueryParser(defaultField, analyzer)
    query = parser.parse(queryS)
    query = query.rewrite(getReader(store))
    hits = searcher.search(query)
    
    results = []
    
    for i in range(0, hits.length()):
        results.append(hits.doc(i).get(field))
    
    searcher.close()
    store.close()
            
    return results

if __name__ == "__main__":
    from process import Entry
    initIndex(Entry)
