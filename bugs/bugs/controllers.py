from turbogears import controllers, expose, flash
# from bugs import model
import pkg_resources
try:
    pkg_resources.require("SQLObject>=0.8,<=0.10.0")
except pkg_resources.DistributionNotFound:
    import sys
    print >> sys.stderr, """You are required to install SQLObject but appear not to have done so.
Please run your projects setup.py or run `easy_install SQLObject`.

"""
    sys.exit(1)
from turbogears import identity, redirect
from cherrypy import request, response
# from bugs import json
# import logging
# log = logging.getLogger("bugs.controllers")

class Root(controllers.RootController):
    @expose(template="bugs.templates.welcome")
    # @identity.require(identity.in_group("admin"))
    def index(self):
        import time
        # log.debug("Happy TurboGears Controller Responding For Duty")
        flash("Your application is now running")
        return dict(now=time.ctime())
    @expose()
    @identity.require(identity.not_anonymous())
    def ajaxLogin(self):
        return "success!"

    @expose(template="bugs.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")

        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")
