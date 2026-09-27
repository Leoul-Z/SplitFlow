import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from groups.models import Group, Membership

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_and_group(db):
    payer = User.objects.create_user(email='payer@test.com', username='payer', password='testpass123')
    friend = User.objects.create_user(email='friend@test.com', username='friend', password='testpass123')
    group = Group.objects.create(name='Trip', created_by=payer)
    Membership.objects.create(user=payer, group=group, role='admin', status='accepted')
    Membership.objects.create(user=friend, group=group, role='member', status='accepted')
    return payer, friend, group


@pytest.mark.django_db
def test_exact_split_matching_total_succeeds(api_client, user_and_group):
    payer, friend, group = user_and_group
    api_client.force_authenticate(user=payer)

    resp = api_client.post('/api/expenses/', {
        'amount': '90.00',
        'description': 'Dinner',
        'group': group.id,
        'split_type': 'exact',
        'splits': [
            {'user': payer.id, 'share': '30.00'},
            {'user': friend.id, 'share': '60.00'},
        ]
    }, format='json')

    assert resp.status_code == 201


@pytest.mark.django_db
def test_exact_split_not_matching_total_returns_400(api_client, user_and_group):
    payer, friend, group = user_and_group
    api_client.force_authenticate(user=payer)

    resp = api_client.post('/api/expenses/', {
        'amount': '90.00',
        'description': 'Dinner',
        'group': group.id,
        'split_type': 'exact',
        'splits': [
            {'user': payer.id, 'share': '30.00'},
            {'user': friend.id, 'share': '50.00'},  # doesn't sum to 90
        ]
    }, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_percentage_split_not_summing_to_100_returns_400(api_client, user_and_group):
    payer, friend, group = user_and_group
    api_client.force_authenticate(user=payer)

    resp = api_client.post('/api/expenses/', {
        'amount': '90.00',
        'description': 'Dinner',
        'group': group.id,
        'split_type': 'percentage',
        'splits': [
            {'user': payer.id, 'share': '40.00'},
            {'user': friend.id, 'share': '50.00'},  # sums to 90, not 100
        ]
    }, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_equal_split_auto_calculates_share(api_client, user_and_group):
    payer, friend, group = user_and_group
    api_client.force_authenticate(user=payer)

    resp = api_client.post('/api/expenses/', {
        'amount': '100.00',
        'description': 'Groceries',
        'group': group.id,
        'split_type': 'equal',
        'splits': [
            {'user': payer.id},
            {'user': friend.id},
        ]
    }, format='json')

    assert resp.status_code == 201