from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from datetime import datetime

from user import User
from post import Post

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		
		new_post = Post()
		if len(self.request.get('caption').strip()) > 0:
			new_post.text_caption = self.request.get('caption')
		try:
			upload = self.get_uploads()[0]
			new_post.image_blob = upload.key()
		except:
			pass
		user = users.get_current_user()
		myuser_key = ndb.Key('User',  user.user_id() )
		myuser = myuser_key.get()
		new_post.owner_user = myuser_key
		new_post.date = datetime.now()
		new_key = new_post.put()
		myuser.posts.insert(0,new_key)
		myuser.put()

		self.redirect('/')




