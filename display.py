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

class Display(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		template_values = {}
		user = users.get_current_user()

		if user != None:
			url = users.create_logout_url(self.request.uri)
			url_string = "Log Out"

			logedin_use_key = ndb.Key('User',  user.user_id() )
			logedin_user = logedin_use_key.get()

			user_key = ndb.Key (urlsafe=self.request.get('user_key'))
			current_user = user_key.get()

			temp_list = None
			follow_string = ''

			if self.request.get('temp') == 'followers':
				temp_list = ndb.get_multi (current_user.followers)
				follow_string = 'Followers'
				
			elif self.request.get('temp') == 'following':
				temp_list = ndb.get_multi (current_user.following)
				follow_string = 'Following'




			template_values = {
				'logedin_use_key': logedin_use_key.urlsafe(),
				'logedin_user':logedin_user,
				'user_key':user_key.urlsafe(),
				'current_user': current_user,
				'user':user,
				'url':url,
				'url_string':url_string,
				'temp_list': temp_list,
				'follow_string':follow_string		
				}


			template = JINJA_ENVIRONMENT.get_template ('display.html')
			self.response.write (template.render (template_values))
		else:
			self.redirect('/')
