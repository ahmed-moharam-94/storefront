from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate(is_staff=False):
        # you have to use the same api_client as the one that will make the request
        # because this api_client that will be authenticated
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate