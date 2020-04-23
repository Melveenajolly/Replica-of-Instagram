import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from google.appengine.ext import blobstore
from user import User
from uploadHandler import UploadHandler
from downloadHandler import DownloadHandler

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
		
		
		user = users.get_current_user()
		myuser = None
		
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'Log Out'
			myuser =''
			myuser_key = ndb.Key('User',  user.user_id() )
			myuser = myuser_key.get()
			
			if  myuser == None:
				
				myuser = User(id = user.user_id(), email_address = user.email())
				myuser.put()
			

			

		else:

			url = users.create_login_url(self.request.uri)
			url_string = 'Log In'



        #passing to html page
		template_values = {
		    'url'  : url,
		    'url_string' : url_string,
		    'user': user,
		    'myuser' : myuser,
		    'upload_url':  blobstore.create_upload_url('/upload')
		   
		    
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
	('/', MainPage,),
	('/upload', UploadHandler),
	('/download', DownloadHandler),
	
	
], debug=True)
	


			


