from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore

from user import User
from post import Post

class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, image_key):
        if not blobstore.get(image_key):
            self.error(404)
        else:
            self.send_blob(image_key)
