import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Model
from .factories import MakeFactory, ModelFactory, TrimFactory

faker = Factory.create()


class Model_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ModelFactory.create_batch(size=3)
        self.make = MakeFactory.create()

    def test_create_model(self):
        """
        Ensure we can create a new model object.
        """
        client = self.api_client
        model_count = Model.objects.count()
        model_dict = factory.build(dict, FACTORY_CLASS=ModelFactory, make=self.make.id)
        response = client.post(reverse('model-list'), model_dict)
        created_model_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Model.objects.count() == model_count + 1
        model = Model.objects.get(pk=created_model_pk)

        assert model_dict['name'] == model.name

    def test_get_one(self):
        client = self.api_client
        model_pk = Model.objects.first().pk
        model_detail_url = reverse('model-detail', kwargs={'pk': model_pk})
        response = client.get(model_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('model-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Model.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        model_qs = Model.objects.all()
        model_count = Model.objects.count()

        for i, model in enumerate(model_qs, start=1):
            response = client.delete(reverse('model-detail', kwargs={'pk': model.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert model_count - i == Model.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        model_pk = Model.objects.first().pk
        model_detail_url = reverse('model-detail', kwargs={'pk': model_pk})
        model_dict = factory.build(dict, FACTORY_CLASS=ModelFactory, make=self.make.id)
        response = client.patch(model_detail_url, data=model_dict)
        assert response.status_code == status.HTTP_200_OK

        assert model_dict['name'] == response.data['name']

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        model = Model.objects.first()
        model_detail_url = reverse('model-detail', kwargs={'pk': model.pk})
        model_name = model.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(model_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert model_name == Model.objects.first().name
