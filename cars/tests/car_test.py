import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Car
from .factories import CarFactory, TrimFactory

faker = Factory.create()


class Car_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        CarFactory.create_batch(size=3)
        self.trim = TrimFactory.create()

    def test_create_car(self):
        """
        Ensure we can create a new car object.
        """
        client = self.api_client
        car_count = Car.objects.count()
        car_dict = factory.build(dict, FACTORY_CLASS=CarFactory, trim=self.trim.id)
        response = client.post(reverse('car-list'), car_dict)
        created_car_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Car.objects.count() == car_count + 1
        car = Car.objects.get(pk=created_car_pk)

        assert car_dict['owner'] == car.owner
        assert car_dict['color'] == car.color
        assert car_dict['year'] == car.year

    def test_get_one(self):
        client = self.api_client
        car_pk = Car.objects.first().pk
        car_detail_url = reverse('car-detail', kwargs={'pk': car_pk})
        response = client.get(car_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('car-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Car.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        car_qs = Car.objects.all()
        car_count = Car.objects.count()

        for i, car in enumerate(car_qs, start=1):
            response = client.delete(reverse('car-detail', kwargs={'pk': car.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert car_count - i == Car.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        car_pk = Car.objects.first().pk
        car_detail_url = reverse('car-detail', kwargs={'pk': car_pk})
        car_dict = factory.build(dict, FACTORY_CLASS=CarFactory, trim=self.trim.id)
        response = client.patch(car_detail_url, data=car_dict)
        assert response.status_code == status.HTTP_200_OK

        assert car_dict['owner'] == response.data['owner']
        assert car_dict['color'] == response.data['color']
        assert car_dict['year'] == response.data['year']

    def test_update_year_with_incorrect_value_data_type(self):
        client = self.api_client
        car = Car.objects.first()
        car_detail_url = reverse('car-detail', kwargs={'pk': car.pk})
        car_year = car.year
        data = {
            'year': faker.pystr(),
        }
        response = client.patch(car_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert car_year == Car.objects.first().year

    def test_update_owner_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        car = Car.objects.first()
        car_detail_url = reverse('car-detail', kwargs={'pk': car.pk})
        car_owner = car.owner
        data = {
            'owner': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(car_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert car_owner == Car.objects.first().owner

    def test_update_color_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        car = Car.objects.first()
        car_detail_url = reverse('car-detail', kwargs={'pk': car.pk})
        car_color = car.color
        data = {
            'color': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(car_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert car_color == Car.objects.first().color
