from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from cars.serializers import TrimSerializer

from .factories import (
    CarFactory,
    ModelFactory,
    TrimFactory,
    TrimWithForeignFactory,
)


class TrimSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.trim = TrimWithForeignFactory.create()

    def test_that_a_trim_is_correctly_serialized(self):
        trim = self.trim
        serializer = TrimSerializer
        serialized_trim = serializer(trim).data

        assert serialized_trim['id'] == trim.id
        assert serialized_trim['name'] == trim.name

        assert len(serialized_trim['cars']) == trim.cars.count()
