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
			following_list = ndb.get_multi (logedin_user.following)


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
	    		'logedin_user':logedin_user,
	    		'following_list':following_list

	    	}
			template = JINJA_ENVIRONMENT.get_template ('profile.html')
			self.response.write (template.render (template_values))
		else:
			self.redirect('/')

	def post(self):

		self.response.headers['Content-Type'] = 'text/html'
		user_key = ndb.Key (urlsafe=self.request.get('user_key'))
		current_user = user_key.get()

		logedin_use_key = ndb.Key(urlsafe=self.request.get('logedin_use_key') )
		logedin_user = logedin_use_key.get()

		if self.request.get('button') == 'Follow':
			logedin_user.following.append(user_key)
			current_user.followers.append(logedin_use_key)
			current_user.put()
			logedin_user.put()
			self.redirect('/profile?user_key=' + str(user_key.urlsafe()))

		elif self.request.get('button') == 'Unfollow':
			logedin_user.following.remove(user_key)
			current_user.followers.remove(logedin_use_key)
			current_user.put()
			logedin_user.put()
			self.redirect('/profile?user_key=' + str(user_key.urlsafe()))
			



