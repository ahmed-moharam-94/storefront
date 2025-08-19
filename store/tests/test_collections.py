from http import client
from venv import create
from django.contrib.auth.models import User
from rest_framework import status
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self,  create_collection):
        # Arrange

        # Act
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_401(self, api_client, create_collection, authenticate_user):
        # Arrange

        # Act
        authenticate_user()
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_but_invalid_data_return_404(self, api_client, create_collection, authenticate_user):
        # Arrange
        # Act
        authenticate_user(is_staff=True)
        response = create_collection({'title': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # when the title is invalid then the there will be error in title
        assert response.data['title'] is not None

    def test_if_user_is_admin_but_valid_data_return_201(self, api_client, create_collection, authenticate_user, ):
        # Arrange
        # Act
        authenticate_user(is_staff=True)
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        # when the data is valid check the id of the created object
        assert response.data['id'] is not None
