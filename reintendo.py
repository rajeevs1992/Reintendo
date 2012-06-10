#Reintendo
#Author:V
#Language:Python/app-engine

import cgi
import hashlib
import os
import random
import datetime

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

#User Config area
TemplatePath=os.path.join(os.path.dirname(__file__),'templates/')
salt="qyoASDXssedkFFGGan"
firstYearStart=2012
#User Config area ends

class users(db.Model):
	uname=db.StringProperty(required=True,indexed=True)
	email=db.EmailProperty(required=True)
	passwd=db.StringProperty(required=True,indexed=True)

class retest(db.Model):	
	subject=db.StringProperty(required=True)
	date=db.DateProperty(required=True,indexed=True)
	batch=db.StringProperty(required=True)
	number=db.StringProperty(required=True,indexed=True)
	passwd=db.StringProperty(required=True,indexed=True)
	Temail=db.EmailProperty(required=True)

class student(db.Model):
	number=db.StringProperty(required=True,indexed=True)
	name=db.StringProperty(required=True)
	rno=db.StringProperty(required=True,indexed=True)


class homepage(webapp.RequestHandler):
	def get(self):
		args=''
		get= self.request.get("s")
		if get=='test':		
			args={'message':
			"Retest registration successful.An announcement has been made at %s."%(self.request.get("email"))}
		elif get=='unauth':
			args={'message':'You are not authorized to view this page.'}
		elif get=='logout':
			args={'message':'Logged out successfully.'}
		self.response.out.write(template.render(TemplatePath+'homepage.html',args))

class login(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type']='text/html'
		self.response.headers.add_header("Set-Cookie",'sessid=''')
		e=self.request.get("e")
		args={'field1':'Username','destn':'/setCookieT','name':'uname'}
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
			saltedEmail=hashlib.sha1(reply.email+salt).hexdigest()
			args={'uname':uname}
			cookie=uname+'|'+saltedHash
			email=reply.email+'|'+saltedEmail
			self.response.headers['Content-Type']='text/html'
			self.response.headers.add_header("Set-Cookie",'sessid='+cookie)
			self.response.headers.add_header("Set-Cookie",'email='+email)
			self.redirect("/announce")
		else:
			self.redirect("/login?e=1")

class announce(webapp.RequestHandler):
	def get(self):
		cookie=self.request.cookies['sessid']
		j=0
		args={}
		for i in ['a','b','c','d']:
			args[i]=str(firstYearStart-j)+'-'+str(firstYearStart-j+4)
			j+=1
		if len(cookie)>0:
			cookie=cookie.split('|')
			if hashlib.sha1(cookie[0]+salt).hexdigest() == cookie[1]:			
				self.response.out.write(template.render(TemplatePath+'announce.html',args))
		else:
			self.redirect("/?s=unauth")
		
class signup(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render(TemplatePath+'signup.html',''))

class writeUser(webapp.RequestHandler):
	def post(self):
		uname=self.request.get('uname')
		passwd=self.request.get('passwd')
		email=self.request.get('email')
		if passwd!='none':
			passwd=hashlib.sha1(passwd).hexdigest()
		if uname and passwd and email:
			user=users(uname=uname,email=email,passwd=passwd)
			user.put()
			self.redirect("/admin/signup")
		else:
			args={'error':'All fields are mandatory!!'}
			self.response.out.write(template.render(TemplatePath+'signup.html',args))
			
class logout(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type']='text/html'
		self.response.headers.add_header("Set-Cookie",'sessid=''')
		self.response.headers.add_header("Set-Cookie",'dev_appserver_login=''')
		self.redirect("/?s=logout")

class createTest(webapp.RequestHandler):
	def post(self):
		cookie=self.request.cookies['sessid']
		email=self.request.cookies['email']
		if len(cookie)>0:
			cookie=cookie.split('|')
			email=email.split('|')
			if hashlib.sha1(cookie[0]+salt).hexdigest() == cookie[1] and hashlib.sha1(email[0]+salt).hexdigest() == email[1]:
				sub=self.request.get('subject')
				datestr=self.request.get('date')
				date=datestr.split('-')
				date=datetime.date(int(date[0]),int(date[1]),int(date[2]))
				time=self.request.get('time')
				batch=self.request.get('batch')
				number=str(random.randint(10000,99999))
				passwd=hashlib.sha1(str(random.randint(1000,9999))).hexdigest()[0:10]
				to=self.mail(sub,datestr,time,batch,number,passwd)
				test=retest(subject=sub,date=date,batch=batch,number=number,passwd=passwd,Temail=email[0])
				test.put()
				self.redirect("/?s=test&email=%s"%(to))
			else:
				self.redirect("/?s=unauth")
	def mail(self,sub,datestr,time,batch,number,passwd):
		query="SELECT * FROM users WHERE uname='%s' AND passwd ='%s'"%(batch,'none')
		reply=db.GqlQuery(query).get()
		to=reply.email
		announce_body='''
A retest for the subject %s is scheduled on %s at %s.Please register with the below link.

					Retest Number :%s
					Password      :%s

				   Register at:
				   reintendo.appspot.com/login?u=s'''%(sub,datestr,time,number,passwd)
		mail.send_mail(sender='Retest Announcement <rajeevs1992@gmail.com>',
						to=to,
						subject=sub+' Retest on '+datestr,
						body=announce_body)
		return to

class register(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render(TemplatePath+'register.html',''))

class writeToDb(webapp.RequestHandler):
	def post(self):
		number=self.request.get("number")
		passwd=self.request.get("passwd")
		name=self.request.get("name")
		rno=self.request.get("rno")
		query="SELECT * FROM retest WHERE number='%s' AND passwd ='%s'"%(number,passwd)
		reply=db.GqlQuery(query).get()
		if reply is not None:
			reply=db.GqlQuery("SELECT * FROM student WHERE rno='%s' AND number='%s'"%(rno,number)).get()
			if reply is None:
				s=student(number=number,name=name,rno=rno)
				s.put()
				self.redirect("/")	
			else:
				self.response.out.write(template.render(TemplatePath+'register.html',{'error':'Already Registerd'}))
		else:
			self.response.out.write(template.render(TemplatePath+'register.html',{'error':'Test doesnt exist!'}))
		

application=webapp.WSGIApplication(\
[('/',homepage),('/login',login),\
('/announce',announce),('/admin/signup',signup),\
('/logout',logout),('/setCookieT',setCookieT),('/admin/writeUser',writeUser),\
('/createTest',createTest),('/register',register),('/writeToDb',writeToDb)],debug=True)
run_wsgi_app(application)
