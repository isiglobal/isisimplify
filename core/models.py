"""
ISIS: A Server-Sent Events Chat App.
Copyright 2013 Brand Thomas <bt@brand.io>
"""
import datetime
import hashlib
import random
import string

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Table, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# XXX: 'Base' configured in 'database' module
from database import Base

from flask.ext.login import UserMixin, AnonymousUser

class Anonymous(AnonymousUser):
	def __init__(self, **kwargs):
		super(Anonymous, self).__init__(**kwargs)
		self.id = -1
		self.username = 'Anonymous'
		self.email = 'none@example.com'
		self.dtime_create = datetime.datetime.now()

	def get_url(self, username=True):
		if username:
			return '/user/view/%s' % self.username
		return '/user/viewid/%d' % self.id

class User(Base, UserMixin):
	"""
	User Model *AND* Flask.ext.Login Session Manager.
	"""
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)

	username = Column(String, nullable=False)
	email = Column(String)

	passhash = Column(String, nullable=False)
	passsalt = Column(String, nullable=False)

	dtime_create = Column(DateTime, nullable=False,
			default=datetime.datetime.now)

	dtime_llogin = Column(DateTime)

	chats = relationship('Participant')
	lines = relationship('Chatline', backref='user')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)

		if 'passsalt' not in kwargs:
			self.passsalt = self.generate_salt()

	def get_url(self, username=True):
		if username:
			return '/user/view/%s' % self.username
		return '/user/viewid/%d' % self.id

	def check_password(self, password):
		"""
		Check to see if the user has supplied the correct
		password to login.
		"""
		return self.hash_password(password, self.passsalt) == \
				self.passhash

	def set_new_password(self, password):
		salt = self.generate_salt()
		self.passsalt = salt
		self.passhash = self.hash_password(password, salt)
		return self

	@staticmethod
	def hash_password(password, salt=None):
		if salt:
			password += salt
		return hashlib.sha256(password).hexdigest()

	@staticmethod
	def generate_salt(size=10):
		return ''.join([random.choice(string.printable) \
			for i in range(size)])

