from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from cars.serializers import MakeSerializer

from .factories import MakeFactory, MakeWithForeignFactory, ModelFactory


class MakeSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.make = MakeWithForeignFactory.create()

    def test_that_a_make_is_correctly_serialized(self):
        make = self.make
        serializer = MakeSerializer
        serialized_make = serializer(make).data

        assert serialized_make['id'] == make.id
        assert serialized_make['name'] == make.name

        assert len(serialized_make['models']) == make.models.count()
