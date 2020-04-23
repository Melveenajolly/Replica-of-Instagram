from google.appengine.ext import ndb

class User (ndb.Model):
	email_address = ndb.StringProperty()
	username = ndb.StringProperty()
	following = ndb.KeyProperty(kind = "User", repeated=True)
	followers = ndb.KeyProperty(kind = "User", repeated=True)
	posts = ndb.KeyProperty(kind = "Post", repeated=True)