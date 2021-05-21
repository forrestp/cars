from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from cars.serializers import CarSerializer

from .factories import CarFactory


class CarSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.car = CarFactory.create()

    def test_that_a_car_is_correctly_serialized(self):
        car = self.car
        serializer = CarSerializer
        serialized_car = serializer(car).data

        assert serialized_car['id'] == car.id
        assert serialized_car['owner'] == car.owner
        assert serialized_car['color'] == car.color
        assert serialized_car['year'] == car.year
