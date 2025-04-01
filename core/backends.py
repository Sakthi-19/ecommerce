from mongoengine import DoesNotExist
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend
from .models import User

class MongoAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except DoesNotExist:
            return None