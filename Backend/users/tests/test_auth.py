import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_creates_user(api_client):
    resp = api_client.post('/auth/register/', {
        'email': 'a@test.com', 'username': 'alice', 'password': 'testpass123'
    })
    assert resp.status_code == 201
    assert User.objects.filter(email='a@test.com').exists()

@pytest.mark.django_db
def test_login_returns_tokens(api_client):
    User.objects.create_user(email='a@test.com', username='alice', password='testpass123')
    resp = api_client.post('/auth/login/', {'email': 'a@test.com', 'password': 'testpass123'})
    assert resp.status_code == 200
    assert 'access' in resp.data and 'refresh' in resp.data

@pytest.mark.django_db
def test_login_wrong_password_fails(api_client):
    User.objects.create_user(email='a@test.com', username='alice', password='testpass123')
    resp = api_client.post('/auth/login/', {'email': 'a@test.com', 'password': 'wrong'})
    assert resp.status_code == 401

@pytest.mark.django_db
def test_me_requires_auth(api_client):
    resp = api_client.get('/auth/me/')
    assert resp.status_code == 401

@pytest.mark.django_db
def test_me_returns_current_user(api_client):
    user = User.objects.create_user(email='a@test.com', username='alice', password='testpass123')
    api_client.force_authenticate(user=user)
    resp = api_client.get('/auth/me/')
    assert resp.status_code == 200
    assert resp.data['email'] == 'a@test.com'