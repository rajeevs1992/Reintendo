#Reintendo
#Author:V
#Language:Python/app-engine

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
	uname=db.StringProperty(required=True,indexed=True)
	email=db.EmailProperty(required=True)
	passwd=db.StringProperty(required=True,indexed=True)

class homepage(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render(TemplatePath+'homepage.html',''))

class login(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type']='text/html'
		self.response.headers.add_header("Set-Cookie",'sessid=''')
		e=self.request.get("e")
		u=self.request.get("u")
		if u=='t':
			args={'field1':'Username','destn':'/setCookieT','name':'uname'}
		elif u=='s':
			args={'field1':'Retest number','destn':'/register','name':'retest'}
		if e=='1':
			args['error']="Invalid password"
		self.response.out.write(template.render(TemplatePath+'login.html',args))

class setCookieT(webapp.RequestHandler):
	def post(self):
		uname=self.request.get("uname")
		passwd=self.request.get("passwd")
		args=''
		query="SELECT * FROM users WHERE uname='%s' AND passwd ='%s'"%(uname,hashlib.sha1(passwd).hexdigest())
		reply=db.GqlQuery(query).get()
		if reply is not None:
			saltedHash=hashlib.sha1(uname+salt).hexdigest()
			args={'uname':uname}
			cookie=uname+'|'+saltedHash
			self.response.headers['Content-Type']='text/html'
			self.response.headers.add_header("Set-Cookie",'sessid='+cookie)
			self.redirect("/announce")
		else:
			self.redirect("/login?u=t&e=1")

class announce(webapp.RequestHandler):
	def get(self):
		cookie=self.request.cookies['sessid']
		if len(cookie)>0:
			cookie=cookie.split('|')
			if hashlib.sha1(cookie[0]+salt).hexdigest() == cookie[1]:			
				self.response.headers.add_header("Pragmae",'no-cache')
				self.response.headers.add_header("Cache-control",'no-cache')
				self.response.headers.add_header("expires",'0')
				self.response.out.write(template.render(TemplatePath+'announce.html',''))
		else:
			self.redirect("/")
		

class signup(webapp.RequestHandler):
	def get(self):
		user=users(uname="rajeev",email="rajeevs1992@gmail.com",passwd=hashlib.sha1("password").hexdigest())
		user.put()
		self.redirect("/")

class logout(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type']='text/html'
		self.response.headers.add_header("Set-Cookie",'sessid=''')
		self.redirect("/")

application=webapp.WSGIApplication(\
[('/',homepage),('/login',login),('/announce',announce),('/signup',signup),('/logout',logout),('/setCookieT',setCookieT)],debug=True)
run_wsgi_app(application)
