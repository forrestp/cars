import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from cars.models import Make, Model
from cars.types import ModelNode

from .validations import validate_mutation


class ModelCreateData(graphene.InputObjectType):
    name = graphene.String()
    make = graphene.ID(required=True)


class ModelUpdateData(graphene.InputObjectType):
    name = graphene.String()
    make = graphene.ID()


class CreateModel(relay.ClientIDMutation):
    class Input:
        data = ModelCreateData()

    model = graphene.Field(ModelNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        validate_dict = {
            'name': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        if data is None:
            raise GraphQLError(f'empty data')

        make = data.pop('make', None)

        if make is None:
            raise GraphQLError(f'Missing foreign key makeId')
        else:
            make = from_global_id(make)[1]

        obj = Model.objects.create(**data, make_id=make)

        return CreateModel(model=obj)


class UpdateModel(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        data = ModelUpdateData()

    model = graphene.Field(ModelNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, data):
        validate_dict = {
            'name': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        make = data.pop('make', None)
        if make is not None:
            data['make_id'] = from_global_id(make)[1]

        obj, _ = Model.objects.update_or_create(pk=from_global_id(id)[1], defaults=data)

        return UpdateModel(model=obj)


class DeleteModel(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = Model.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteModel(ok=True)
