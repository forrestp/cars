import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Make
from .factories import MakeFactory, ModelFactory

faker = Factory.create()


class Make_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        MakeFactory.create_batch(size=3)

    def test_create_make(self):
        """
        Ensure we can create a new make object.
        """
        client = self.api_client
        make_count = Make.objects.count()
        make_dict = factory.build(dict, FACTORY_CLASS=MakeFactory)
        response = client.post(reverse('make-list'), make_dict)
        created_make_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Make.objects.count() == make_count + 1
        make = Make.objects.get(pk=created_make_pk)

        assert make_dict['name'] == make.name

    def test_get_one(self):
        client = self.api_client
        make_pk = Make.objects.first().pk
        make_detail_url = reverse('make-detail', kwargs={'pk': make_pk})
        response = client.get(make_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('make-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Make.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        make_qs = Make.objects.all()
        make_count = Make.objects.count()

        for i, make in enumerate(make_qs, start=1):
            response = client.delete(reverse('make-detail', kwargs={'pk': make.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert make_count - i == Make.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        make_pk = Make.objects.first().pk
        make_detail_url = reverse('make-detail', kwargs={'pk': make_pk})
        make_dict = factory.build(dict, FACTORY_CLASS=MakeFactory)
        response = client.patch(make_detail_url, data=make_dict)
        assert response.status_code == status.HTTP_200_OK

        assert make_dict['name'] == response.data['name']

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        make = Make.objects.first()
        make_detail_url = reverse('make-detail', kwargs={'pk': make.pk})
        make_name = make.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(make_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert make_name == Make.objects.first().name
