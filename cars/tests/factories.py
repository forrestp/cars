from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from cars.models import Car, Make, Model, Trim

faker = Factory.create()


class MakeFactory(DjangoModelFactory):
    class Meta:
        model = Make

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class MakeWithForeignFactory(MakeFactory):
    @factory.post_generation
    def models(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ModelFactory(make=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                ModelFactory(make=obj)


class ModelFactory(DjangoModelFactory):
    class Meta:
        model = Model

    make = factory.SubFactory('cars.tests.factories.MakeFactory')
    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class ModelWithForeignFactory(ModelFactory):
    @factory.post_generation
    def trims(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                TrimFactory(model=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                TrimFactory(model=obj)


class TrimFactory(DjangoModelFactory):
    class Meta:
        model = Trim

    model = factory.SubFactory('cars.tests.factories.ModelFactory')
    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class TrimWithForeignFactory(TrimFactory):
    @factory.post_generation
    def cars(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                CarFactory(trim=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                CarFactory(trim=obj)


class CarFactory(DjangoModelFactory):
    class Meta:
        model = Car

    trim = factory.SubFactory('cars.tests.factories.TrimFactory')
    owner = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    color = fuzzy.FuzzyChoice(Car.COLOR_CHOICES, getter=lambda c: c[0])
    year = LazyAttribute(lambda o: randint(1900, 2100))
