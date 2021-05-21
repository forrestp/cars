import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Trim
from .factories import CarFactory, ModelFactory, TrimFactory

faker = Factory.create()


class Trim_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        TrimFactory.create_batch(size=3)
        self.model = ModelFactory.create()

    def test_create_trim(self):
        """
        Ensure we can create a new trim object.
        """
        client = self.api_client
        trim_count = Trim.objects.count()
        trim_dict = factory.build(dict, FACTORY_CLASS=TrimFactory, model=self.model.id)
        response = client.post(reverse('trim-list'), trim_dict)
        created_trim_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Trim.objects.count() == trim_count + 1
        trim = Trim.objects.get(pk=created_trim_pk)

        assert trim_dict['name'] == trim.name

    def test_get_one(self):
        client = self.api_client
        trim_pk = Trim.objects.first().pk
        trim_detail_url = reverse('trim-detail', kwargs={'pk': trim_pk})
        response = client.get(trim_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('trim-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Trim.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        trim_qs = Trim.objects.all()
        trim_count = Trim.objects.count()

        for i, trim in enumerate(trim_qs, start=1):
            response = client.delete(reverse('trim-detail', kwargs={'pk': trim.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert trim_count - i == Trim.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        trim_pk = Trim.objects.first().pk
        trim_detail_url = reverse('trim-detail', kwargs={'pk': trim_pk})
        trim_dict = factory.build(dict, FACTORY_CLASS=TrimFactory, model=self.model.id)
        response = client.patch(trim_detail_url, data=trim_dict)
        assert response.status_code == status.HTTP_200_OK

        assert trim_dict['name'] == response.data['name']

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        trim = Trim.objects.first()
        trim_detail_url = reverse('trim-detail', kwargs={'pk': trim.pk})
        trim_name = trim.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(trim_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert trim_name == Trim.objects.first().name
