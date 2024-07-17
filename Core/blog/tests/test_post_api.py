from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import CustomUser as User


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="admin@admin.com", password="a/@1234567", is_verified=True
    )
    return user


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestPostApi:

    client = APIClient()

    @pytest.fixture
    def test_get_post_response_200_status(self):
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    # authentication is forbidden
    def test_create_post_response_401_status(self):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_403_status(self):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        self.client.force_authenticate(user={})
        response = self.client.post(url, data)
        assert response.status_code == 403

    # user is allowed to create post
    def test_create_post_response_400_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400
