import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import User

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		url = ''
		url_string = ''
		
		search_url = ''
		search_url_string = ''
		
		
		user = users.get_current_user()
		myuser = None
		
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			myuser =''
			myuser_key = ndb.Key('User',  user.user_id() )
			myuser = myuser_key.get()
			
			if  myuser == None:
				
				myuser = User(id = user.user_id(), email_address = user.email())
				myuser.put()
				
			

		else:

			url = users.create_login_url(self.request.uri)
			url_string = 'login'



        #passing to html page
		template_values = {
		    'url'  : url,
		    'url_string' : url_string,
		    'user': user,
		    'myuser' : myuser
		   
		    
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
	('/', MainPage,

	)
	
], debug=True)
	


			

