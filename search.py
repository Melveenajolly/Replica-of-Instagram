import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from google.appengine.ext import blobstore
from user import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Search(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		template_values = {}
		logedin_user= None
		user = users.get_current_user() 
		search_output = None


		if user != None:

			logedin_use_key = ndb.Key('User',  user.user_id() )
			logedin_user = logedin_use_key.get()
			
			url = users.create_logout_url(self.request.uri)
			url_string = "Log Out"

			if len(self.request.get('search').strip()) > 0:
				search_input = self.request.get('search')
				search_username = search_input.lower()
				limit = search_username[:-1] + chr(ord(search_username[-1]) + 1)
				search_output =User.query(User.username >= search_username, User.username < limit).fetch()
			
			template_values = {
				'user':user,
				'logedin_user':logedin_user,
				'logedin_use_key':logedin_use_key.urlsafe(),
				'search_output': search_output,
				'url': url,
				'url_string':url_string


			}
			
			
			template = JINJA_ENVIRONMENT.get_template('search.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')

			
				

				


					
					
		
				









