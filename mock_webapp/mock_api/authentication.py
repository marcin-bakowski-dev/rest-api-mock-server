# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication


class MockNoAuthentication(BaseAuthentication):

    def authenticate(self, request):
        return User(username="mocker"), None
