import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from cars.models import Make
from cars.types import MakeNode

from .validations import validate_mutation


class MakeCreateData(graphene.InputObjectType):
    name = graphene.String()


class MakeUpdateData(graphene.InputObjectType):
    name = graphene.String()


class CreateMake(relay.ClientIDMutation):
    class Input:
        data = MakeCreateData()

    make = graphene.Field(MakeNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        validate_dict = {
            'name': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        if data is None:
            raise GraphQLError(f'empty data')

        obj = Make.objects.create(**data)

        return CreateMake(make=obj)


class UpdateMake(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        data = MakeUpdateData()

    make = graphene.Field(MakeNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, data):
        validate_dict = {
            'name': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        obj, _ = Make.objects.update_or_create(pk=from_global_id(id)[1], defaults=data)

        return UpdateMake(make=obj)


class DeleteMake(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = Make.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteMake(ok=True)
