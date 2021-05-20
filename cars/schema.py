from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .mutations.car import CreateCar, DeleteCar, UpdateCar
from .mutations.make import CreateMake, DeleteMake, UpdateMake
from .mutations.model import CreateModel, DeleteModel, UpdateModel
from .mutations.trim import CreateTrim, DeleteTrim, UpdateTrim
from .types import CarNode, MakeNode, ModelNode, TrimNode


class Query(ObjectType):
    make = relay.Node.Field(MakeNode)
    model = relay.Node.Field(ModelNode)
    trim = relay.Node.Field(TrimNode)
    car = relay.Node.Field(CarNode)

    all_make = DjangoFilterConnectionField(MakeNode)
    all_model = DjangoFilterConnectionField(ModelNode)
    all_trim = DjangoFilterConnectionField(TrimNode)
    all_car = DjangoFilterConnectionField(CarNode)


class Mutation(ObjectType):
    create_make = CreateMake.Field()
    create_model = CreateModel.Field()
    create_trim = CreateTrim.Field()
    create_car = CreateCar.Field()

    update_make = UpdateMake.Field()
    update_model = UpdateModel.Field()
    update_trim = UpdateTrim.Field()
    update_car = UpdateCar.Field()

    delete_make = DeleteMake.Field()
    delete_model = DeleteModel.Field()
    delete_trim = DeleteTrim.Field()
    delete_car = DeleteCar.Field()
