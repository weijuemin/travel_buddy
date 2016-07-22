from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Travel(models.Model):
	destination = models.CharField(max_length=255)
	plan_detail = models.TextField()
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class User_travel(models.Model):
	user = models.ForeignKey(User)
	travel = models.ForeignKey(Travel)


# Managing part
class Validator(object): # not using manager here cuz it's not dealing any table level management
	def __init__(self):
		self.error = False
		self.msg = {}
	def isShort(self, form, formInput):
		for key, val in formInput.iteritems():
			if len(form[key]) < val:
				self.error = True
				self.msg[key] = '{} should be at least {} characters'.format(key, val)
		return (self.msg, self.error)
	def emailInvalid(self, form):
		if not EMAIL_REGEX.match(form['email']):
			self.error = True
			self.msg['emailFormat'] = 'Oops! Invalid email'
		return (self.error, self.msg)

class UserManager(models.Manager): # still not table level, but straight forward
	def exist(self, form):
		testUser = User.objects.filter(email=form['email'])
		if testUser:
			return True
		return False			
	def logout(self, session):
		keyList = ['first_name','last_name','fname','lInit','email','user_id']
		for key in keyList:
			if key in session:
				session.pop(key)