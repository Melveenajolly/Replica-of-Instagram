import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from user import User
from post import Post


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Profile(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		template_values = {}
    	
		if user != None:
			logedin_use_key = ndb.Key('User',  user.user_id() )
			logedin_user = logedin_use_key.get()
	    	
			user_key = ndb.Key (urlsafe=self.request.get('user_key'))
			current_user = user_key.get()
			url = users.create_logout_url(self.request.uri)
			url_string = "Log Out"
			followers_count = len(current_user.followers)
			following_count = len(current_user.following)
			current_user_post = ndb.get_multi (current_user.posts)


			template_values={
	    		'user_key': user_key.urlsafe(),
	    		'current_user':current_user,
	    		'url': url,
	    		'url_string': url_string,
	    		'user':user,
	    		'followers_count':followers_count,
	    		'following_count':following_count,
	    		'current_user_post': current_user_post,
	    		'logedin_use_key':logedin_use_key.urlsafe(),
	    		'logedin_user':logedin_user

	    	}
			template = JINJA_ENVIRONMENT.get_template ('profile.html')
			self.response.write (template.render (template_values))
	    

		else:
			self.redirect('/')