from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

from user import User
from post import Post

class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
    	post = ndb.Key(urlsafe=self.request.get('key')).get()
      
        self.send_blob( post.image_blob)
