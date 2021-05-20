import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from cars.models import Car, Trim
from cars.types import CarNode

from .validations import validate_mutation

colorType = graphene.Enum('carcolor', Car.COLOR_CHOICES)


class CarCreateData(graphene.InputObjectType):
    owner = graphene.String()
    color = graphene.InputField(colorType)
    year = graphene.Int()
    trim = graphene.ID(required=True)


class CarUpdateData(graphene.InputObjectType):
    owner = graphene.String()
    color = graphene.InputField(colorType)
    year = graphene.Int()
    trim = graphene.ID()


class CreateCar(relay.ClientIDMutation):
    class Input:
        data = CarCreateData()

    car = graphene.Field(CarNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        validate_dict = {
            'owner': {'max': 255, },
            'color': {'max': 255, },
            'year': {'max': 2100, 'min': 1900, },
        }

        validate_mutation(validate_dict, data)

        if data is None:
            raise GraphQLError(f'empty data')

        trim = data.pop('trim', None)

        if trim is None:
            raise GraphQLError(f'Missing foreign key trimId')
        else:
            trim = from_global_id(trim)[1]

        obj = Car.objects.create(**data, trim_id=trim)

        return CreateCar(car=obj)


class UpdateCar(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        data = CarUpdateData()

    car = graphene.Field(CarNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, data):
        validate_dict = {
            'owner': {'max': 255, },
            'color': {'max': 255, },
            'year': {'max': 2100, 'min': 1900, },
        }

        validate_mutation(validate_dict, data)

        trim = data.pop('trim', None)
        if trim is not None:
            data['trim_id'] = from_global_id(trim)[1]

        obj, _ = Car.objects.update_or_create(pk=from_global_id(id)[1], defaults=data)

        return UpdateCar(car=obj)


class DeleteCar(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = Car.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteCar(ok=True)
