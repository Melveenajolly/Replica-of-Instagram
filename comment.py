from google.appengine.ext import ndb

class Comment (ndb.Model):
	comment_text =  ndb.StringProperty()
	owner_user = ndb.KeyProperty(kind ="User")
	