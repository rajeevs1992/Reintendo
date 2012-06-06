import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
br='<br>'
class homepage(webapp.RequestHandler):
	def get(self):
		html='''
		<html>
			<title>Welcome!!</title>
			<head>
			 <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
			 </head>
			<body>
				<h1>Welcome to Reintendo!!!!</h1>
				<h6>There is always a second chance......</h6>

				A single point to announce and register for the retests.
				Login with your Gmail account!!
				<form action=/login method=get>
					<input class=.submit type=submit value=Login>
				</form>

			</body>
		</html>
		'''
		self.response.out.write(html)
class login(webapp.RequestHandler):
	def get(self):
		user=users.get_current_user()
		flag=auth(user)
		if not user:
			self.redirect(users.create_login_url(self.request.uri))

application=webapp.WSGIApplication([('/',homepage),('/login',login)],debug=True)
run_wsgi_app(application)
