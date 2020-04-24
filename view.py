import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from user import User
from post import Post
from comment import Comment

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class View(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		template_values = {}

		if user != None:
			logedin_use_key = ndb.Key('User',  user.user_id() )
			logedin_user = logedin_use_key.get()
			url = users.create_logout_url(self.request.uri)
			url_string = "Log Out"
			post_key =  ndb.Key(urlsafe=(self.request.get('post_key')) )
			post_item = post_key.get()

			template_values = {
			'user':user,
			'logedin_use_key':logedin_use_key.urlsafe(),
			'logedin_user': logedin_user,
			'url':url,
			'url_string':url_string,
			'post_key':post_key.urlsafe(),
			'post_item':post_item
			}
			template = JINJA_ENVIRONMENT.get_template ('view.html')
			self.response.write (template.render (template_values))

		else:
			self.redirect('/')


	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		logedin_use_key = ndb.Key('User',  user.user_id() )
		logedin_user = logedin_use_key.get()
		

		if self.request.get('button') == 'Submit':
			if len(self.request.get('comment').strip()) > 0:
				comment_text = self.request.get('comment')
				post_id = ndb.Key('Post',  int(self.request.get('postid')))
				commented_post = post_id.get()

				comment = Comment()
				comment.comment_text = comment_text
				comment.owner_user = logedin_use_key
				comment_key = comment.put()
				commented_post.comments.insert(0,comment_key)
				commented_post.put()
			self.redirect('/view?post_key=' + str(post_id.urlsafe()))





