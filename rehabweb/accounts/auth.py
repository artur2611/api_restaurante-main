from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

from core import api_client


class ApiAuthBackend(BaseBackend):
    """Authenticate against the external Flask API and create a local User record.

    This backend returns a Django `User` object on successful authentication so
    that Django `login()` and `@login_required` can work. It stores the API
    token in the request session when available.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            data = api_client.login(username, password)
        except Exception:
            return None
        user_info = data.get('user', {})
        username = user_info.get('username') or username
        if not username:
            return None
        user, _ = User.objects.get_or_create(username=username)
        user.email = user_info.get('email', '')
        user.save()
        if request is not None:
            request.session['api_token'] = data.get('token') or data.get('access_token')
            request.session['api_user'] = user_info
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from core import api_client

class ApiAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            data = api_client.login(username, password)
        except Exception:
            return None
        user_info = data.get('user', {})
        user, _ = User.objects.get_or_create(username=user_info.get('username'))
        user.email = user_info.get('email', '')
        user.save()
        request.session['api_token'] = data.get('token')
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None