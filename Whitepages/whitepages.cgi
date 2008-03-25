#!/usr/bin/env python
import cgitb
cgitb.enable()
import kid, process, cgi, luceneUtil,sys
from sqlobject import *

fields = cgi.FieldStorage()
entries = None
extras = None
flash = None

if fields.has_key("q"):
    # we must be searching
    try:
        entriesID = luceneUtil.doSearch(fields['q'].value)
        entries = process.Entry.select(IN(process.Entry.q.id, entriesID)).orderBy("data")
    except:
        entries = []
        flash = "Couldn't find a thing!"

if fields.has_key("letter"):
    try:
#        extras = fields['letter'].value
        entries = process.Entry.select(IN(process.Entry.q.source, process.revAlphas[fields['letter'].value]))
#        extras = entries[1].source
    except:
#        import traceback
#        extras = "\n".join(traceback.format_stack())
        entries = []
        flash = "Error finding letter!"

if not entries:
    entries = []

template = kid.Template(file='address.kid', entries=entries, extras=extras, flash=flash)
print "Content-Type:text/html\n"
print template.serialize()