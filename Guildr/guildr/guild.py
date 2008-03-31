import turbogears as tg
from turbogears import controllers, expose, flash
# from guildr import model
from turbogears import identity, redirect
from cherrypy import request, response
from model import Guild

class GuildController(controllers.Controller):
    @expose()
    def default(self, *args):
        if len(args) != 1:
            raise redirect("/")
        return ""