from google.appengine.ext import ndb

class Post (ndb.Model):
	image_blob = ndb.BlobKeyProperty()
	text_caption = ndb.StringProperty()
	owner_user = ndb.KeyProperty(kind ="User")
	date = ndb.DateTimeProperty()
	comments =  ndb.KeyProperty(kind ="Comment", repeated = True)
