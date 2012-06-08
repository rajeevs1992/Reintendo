import cgi
import hashlib
import os
import hmac

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
TemplatePath=os.path.join(os.path.dirname(__file__),'templates/')
salt="qyoASDXssedkFFGGan"

class users(db.Model):
	uname=db.TextProperty(required=True,indexed=True)
	email=db.EmailProperty(required=True)
	passwd=db.TextProperty(required=True)

class homepage(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render(TemplatePath+'homepage.html',''))

class login(webapp.RequestHandler):
	'''Login page for students to register for a retest	
	and teachers to announce retest
	e for error,means password wrong,e=1 ---->error
	u for user,s--->student,t--->teacher'''
	def get(self):
		e=self.request.get("e")
		u=self.request.get("u")
		if u=='t':
			args={'field1':'Username','destn':'/announce','name':'uname'}
		elif u=='s':
			args={'field1':'Retest number','destn':'/register','name':'retest'}
		if e=='1':
			args['error']="Invalid password"
		self.response.out.write(template.render(TemplatePath+'login.html',args))

class announce(webapp.RequestHandler):
	def post(self):
		uname=self.request.get("uname")
		passwd=self.request.get("passwd")
		args=''
		self.response.out.write(str(users.all().count()))
		query="SELECT * FROM users WHERE uname='%s' AND passwd ='%s'"%(uname,hashlib.sha1(passwd).hexdigest())
		query="SELECT * FROM users WHERE uname = 'rajeev'"
		reply=db.GqlQuery(query).get()
		self.response.out.write(reply.uname)
		reply=True
		if reply is not 0:
			saltedHash=hashlib.sha1(uname+salt).hexdigest()
			args={'uname':uname}
			cookie=uname+'|'+saltedHash
			self.response.headers['Content-Type']='text/html'
			self.response.headers.add_header("Set-Cookie",'sessid='+cookie)
			self.response.out.write(template.render(TemplatePath+'announce.html',args))
		else:
			self.redirect("/login?u=t&e=1")
class signup(webapp.RequestHandler):
	def get(self):
		user=users(uname="rajeev",email="rajeevs1992@gmail.com",passwd=hashlib.sha1("password").hexdigest())
		user.put()
		self.redirect("/")
	
application=webapp.WSGIApplication(\
[('/',homepage),('/login',login),('/announce',announce),('/signup',signup)],debug=True)
run_wsgi_app(application)
