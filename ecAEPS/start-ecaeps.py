#!/usr/bin/env python
import pkg_resources
pkg_resources.require("TurboGears")

from turbogears import config, update_config, start_server
import cherrypy
cherrypy.lowercase_api = True
from os.path import *
import sys

# first look on the command line for a desired config file,
# if it's not on the command line, then
# look for setup.py in this directory. If it's not there, this script is
# probably installed
if len(sys.argv) > 1:
    update_config(configfile=sys.argv[1],
        modulename="ecaeps.config")
elif exists(join(dirname(__file__), "setup.py")):
    update_config(configfile="dev.cfg",modulename="ecaeps.config")
else:
    update_config(configfile="prod.cfg",modulename="ecaeps.config")
config.update(dict(package="ecaeps"))

#Add listeners to SQLObject so that the Lucene index is automatically updated
import sqlobject.events as e
from ecaeps.model import Child
import ecaeps.luceneUtil as luceneUtil
e.listen(luceneUtil.rowDeleted, Child, e.RowDestroySignal)
e.listen(luceneUtil.rowAdded, Child, e.RowCreatedSignal)
e.listen(luceneUtil.rowUpdated, Child, e.RowUpdateSignal)

from ecaeps.controllers import Root

start_server(Root())
