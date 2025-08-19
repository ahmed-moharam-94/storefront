from http import client
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self):
        # Arrange

        # Act
        client = APIClient()
        response = client.post('/store/collections/', {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_401(self):
        # Arrange

        # Act
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post('/store/collections/', {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_but_invalid_data_return_404(self):
        # Arrange
        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # when the title is invalid then the there will be error in title
        assert response.data['title'] is not None

    def test_if_user_is_admin_but_valid_data_return_201(self):
        # Arrange
        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        # when the data is valid check the id of the created object
        assert response.data['id'] is not None
