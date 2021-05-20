import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from cars.models import Model, Trim
from cars.types import TrimNode

from .validations import validate_mutation


class TrimCreateData(graphene.InputObjectType):
    name = graphene.String()
    model = graphene.ID(required=True)


class TrimUpdateData(graphene.InputObjectType):
    name = graphene.String()
    model = graphene.ID()


class CreateTrim(relay.ClientIDMutation):
    class Input:
        data = TrimCreateData()

    trim = graphene.Field(TrimNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        validate_dict = {
            'name': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        if data is None:
            raise GraphQLError(f'empty data')

        model = data.pop('model', None)

        if model is None:
            raise GraphQLError(f'Missing foreign key modelId')
        else:
            model = from_global_id(model)[1]

        obj = Trim.objects.create(**data, model_id=model)

        return CreateTrim(trim=obj)


class UpdateTrim(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        data = TrimUpdateData()

    trim = graphene.Field(TrimNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, data):
        validate_dict = {
            'name': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        model = data.pop('model', None)
        if model is not None:
            data['model_id'] = from_global_id(model)[1]

        obj, _ = Trim.objects.update_or_create(pk=from_global_id(id)[1], defaults=data)

        return UpdateTrim(trim=obj)


class DeleteTrim(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = Trim.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteTrim(ok=True)
