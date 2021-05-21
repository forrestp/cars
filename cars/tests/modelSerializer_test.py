from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from cars.serializers import ModelSerializer

from .factories import (
    MakeFactory,
    ModelFactory,
    ModelWithForeignFactory,
    TrimFactory,
)


class ModelSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.model = ModelWithForeignFactory.create()

    def test_that_a_model_is_correctly_serialized(self):
        model = self.model
        serializer = ModelSerializer
        serialized_model = serializer(model).data

        assert serialized_model['id'] == model.id
        assert serialized_model['name'] == model.name

        assert len(serialized_model['trims']) == model.trims.count()
