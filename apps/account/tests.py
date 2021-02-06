import uuid

import pytest

from django.urls import reverse

from apps.school.models import School


@pytest.fixture
def password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, password):
    def mark_user(**kwargs):
        kwargs['password'] = password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        kwargs['first_name'] = 'Test'
        kwargs['last_name'] = 'User'
        return django_user_model.objects.create_user(**kwargs)

    return mark_user


@pytest.mark.django_db
def test_login_view(client, create_user, password):
    user = create_user()
    url = reverse('login')
    client.login(username=user.username, password=password)
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_duplicate_school_domain(client):
    url = reverse('account:register-school')
    data = {'domain': 'yes.com', 'institution': 'soko'}
    session = client.session
    session['ss1'] = {'email': 'blah@mail.com'}
    session.save()
    response = client.post(url, data)
    assert response.context['errors'] == "There's already a school with this domain registered"
    assert response.status_code == 400, 'Bad Request'
