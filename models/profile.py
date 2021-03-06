from __future__ import unicode_literals

import datetime
from mongoengine import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager

ROLES = {'admin': 'admin', 'operator': 'operator', 'visitor': 'visitor', }


class User(UserMixin, Document):
    username = StringField(max_length=255, required=True)
    password_hash = StringField(required=True)
    nick_name = StringField(max_length=255, default=str(username))
    email = EmailField(max_length=255)
    biography = StringField()
    url = URLField()
    date_created = DateTimeField(default=datetime.datetime.utcnow, required=True)
    last_login = DateTimeField(default=datetime.datetime.utcnow, required=True)
    role = StringField(max_length=32, default='admin', choices=ROLES)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def __unicode__(self):
        return self.username


@login_manager.user_loader
def load_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user
