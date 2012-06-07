import cgi
import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
path=os.path.join(os.path.dirname(__file__),'templates/')

class users(db.Model):
	name=db.TextProperty(required=True)
	email=db.EmailProperty(required=True)
	level=db.IntegerProperty(required=True)
	semester=db.IntegerProperty()

class homepage(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render(path+'homepage.html',''))

class regLogin(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render(path+'regLogin.html',''))

application=webapp.WSGIApplication([('/',homepage),('/regLogin',regLogin)],debug=True)
run_wsgi_app(application)
