import uuid

import pytest

from django.urls import reverse

from apps.school.models import AcademicYear


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
def test_academic_session_date_validation(client, create_user, password):
    user = create_user()
    client.login(username=user.username, password=password)
    url = reverse('school:academics')
    data = {'start': '2020-01-01', 'end': '2019-01-01'}
    response = client.post(url, data)

    assert response.context['errors'] ==  'Invalid date range'
    assert response.status_code == 400


# @pytest.mark.django_db
def test_academic_details(client, create_user, password):
    user = create_user()
    client.login(username=user.username, password=password)
    academic = AcademicYear.objects.create(start_date='2020-01-01', end_date='2021-01-01')
    url = reverse('school:academic-details', kwargs={'id': academic.id})
    get_res = client.get(url)
    data = {'description': 'First Term', 'start': '2020-01-01', 'end': '2020-03-31'}
    post_res = client.post(url, data)
    assert get_res.status_code == 200
    assert post_res.status_code == 302
