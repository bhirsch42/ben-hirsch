import webapp2
import cgi
import os
import jinja2
import logging
import hashlib
from google.appengine.ext import ndb

salt = "NO PASSWORD FOR YOU"
cookie_secret = "fight_club"

def saltHash(val):
	return str(hashlib.sha256(val+salt).hexdigest())

def myHash(val):
	return str(hashlib.sha256(val).hexdigest())

def makeSecureVal(val):
	return "%s|%s" % (val, myHash(val + cookie_secret))

def checkSecureVal(secure_val):
	val = secure_val.split('|')[0]
	if secure_val == makeSecureVal(val):
		return val

