import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from .models import Car, Make, Model, Trim


class MakeNode(DjangoObjectType):

    class Meta:
        model = Make
        interfaces = (relay.Node, )
        fields = ['id', 'name', 'models']
        filter_fields = ['id', 'name', 'models']


class ModelNode(DjangoObjectType):

    class Meta:
        model = Model
        interfaces = (relay.Node, )
        fields = ['id', 'name', 'trims', 'make']
        filter_fields = ['id', 'name', 'trims', 'make']


class TrimNode(DjangoObjectType):

    class Meta:
        model = Trim
        interfaces = (relay.Node, )
        fields = ['id', 'name', 'cars', 'model']
        filter_fields = ['id', 'name', 'cars', 'model']


class CarNode(DjangoObjectType):

    class Meta:
        model = Car
        interfaces = (relay.Node, )
        fields = ['id', 'owner', 'color', 'year', 'trim']
        filter_fields = ['id', 'owner', 'color', 'year', 'trim']
