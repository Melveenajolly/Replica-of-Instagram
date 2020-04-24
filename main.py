import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from google.appengine.ext import blobstore
from user import User
from uploadHandler import UploadHandler
from downloadHandler import DownloadHandler
from profile import Profile
from search import Search
from post import Post
from display import Display
from comment import Comment
from view import View

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
		timeline_posts = []
		following_users = []
		
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'Log Out'
			myuser =''
			myuser_key = ndb.Key('User',  user.user_id())
			myuser = myuser_key.get()
			
			if  myuser == None:
				
				myuser = User(id = user.user_id(), email_address = user.email())
				myuser.username = user.email()
				myuser.put()

			else:
				for i in myuser.following:
					following_users.append(i)
				following_users.append(myuser.key)
				timeline_posts = Post.query(Post.owner_user.IN(following_users)).order(-Post.date).fetch()
		



		

			

			

		else:

			url = users.create_login_url(self.request.uri)
			url_string = 'Log In'



        #passing to html page
		template_values = {
		    'url'  : url,
		    'url_string' : url_string,
		    'user': user,
		    'myuser' : myuser,
		    'upload_url':  blobstore.create_upload_url('/upload'),
		    'timeline_posts': timeline_posts
		   
		    
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		myuser_key = ndb.Key('User',  user.user_id())

		if self.request.get('button') == 'Submit':
			if len(self.request.get('comment').strip()) > 0:
				comment_text = self.request.get('comment')
				post_id = ndb.Key('Post',  int(self.request.get('postid')))
				commented_post = post_id.get()

				comment = Comment()
				comment.comment_text = comment_text
				comment.owner_user = myuser_key
				comment_key = comment.put()
				commented_post.comments.insert(0,comment_key)
				commented_post.put()
			self.redirect('/')

		

# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
	('/', MainPage,),
	('/upload', UploadHandler),
	('/download', DownloadHandler),
	('/profile', Profile),
	('/search', Search),
	('/display', Display),
	('/view', View)
	
	
], debug=True)
	


			


