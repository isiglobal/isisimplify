from flask import Flask

from flask.ext.login import LoginManager, login_user, \
		logout_user, login_required, current_user, \
		AnonymousUser

import redis

"""
CONFIGURATION
"""

DEBUG = True
SECRET_KEY = 'not a secret'

"""
APPLICATION CREATION
"""

app = Flask(__name__)
app.config.from_object(__name__)

rds = redis.Redis()

"""
LOGIN/SESSIONS SYSTEM
"""

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.anonymous_user = AnonymousUser
