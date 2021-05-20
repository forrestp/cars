import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from cars.models import Make, Model
from cars.types import MakeNode, ModelNode, TrimNode

from .factories import (
    MakeFactory,
    ModelFactory,
    ModelWithForeignFactory,
    TrimFactory,
)

faker = Factory.create()


class Model_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        ModelFactory.create_batch(size=3)

    def test_create_model(self):
        """
        Ensure we can create a new model object.
        """
        make = MakeFactory.create()

        model_dict = camelize(factory.build(dict, FACTORY_CLASS=ModelFactory,
                                            make=to_global_id(MakeNode._meta.name, make.id)))

        response = self.query(
            """
            mutation($input: CreateModelInput!) {
                createModel(input: $input) {
                    clientMutationId,
                    model {
                        id
                        name
                        make {
                          id
                        }
                    }
                }
            }
            """,
            input_data={'data': model_dict}
        )
        content = json.loads(response.content)
        generated_model = content['data']['createModel']['model']
        self.assertResponseNoErrors(response)
        self.assertEquals(model_dict['name'], generated_model['name'])
        self.assertEquals(model_dict['make'], generated_model['make']['id'])

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allModel query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allModel{
                    edges{
                        node{
                            id
                            name
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        model_list = content['data']['allModel']['edges']
        model_list_qs = Model.objects.all()
        for i, edge in enumerate(model_list):
            model = edge['node']
            self.assertEquals(model['id'], to_global_id(ModelNode._meta.name, model_list_qs[i].id))
            self.assertEquals(model['name'], model_list_qs[i].name)

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allModel query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allModel{
                    edges{
                        node{
                            id
                        }
                    }
                }
            }
            """
        response = self.query(list_query)
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        model_list = content['data']['allModel']['edges']
        model_count = len(model_list)
        for i, edge in enumerate(model_list, start=1):
            model = edge['node']
            model_id = model['id']
            response = self.query(
                """
                mutation($input:DeleteModelInput!) {
                   deleteModel(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': model_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            model_list = content['data']['allModel']['edges']
            new_len = len(model_list)
            assert model_count - i == new_len

    def test_update_mutation_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        model = ModelFactory.create()
        model_id = to_global_id(ModelNode._meta.name, model.pk)
        model_dict = factory.build(dict, FACTORY_CLASS=ModelFactory)
        response = self.query(
            """
            mutation($input: UpdateModelInput!){
                updateModel(input: $input) {
                    model{
                        name
                    }
                }
            }
            """,
            input_data={
                'id': model_id,
                'data': {
                    'name': model_dict['name'],
                }
            }
        )
        self.assertResponseNoErrors(response)
        parsed_response = json.loads(response.content)
        updated_model_data = parsed_response['data']['updateModel']['model']
        self.assertEquals(updated_model_data['name'], model_dict['name'])

    def test_update_mutation_name_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        model = ModelFactory.create()
        model_id = to_global_id(ModelNode._meta.name, model.pk)
        random_int = faker.pyint()
        response = self.query(
            """
            mutation{
                updateModel(input: {
                    id: "%s",
                    data:{
                        name: %s
                    }
                }) {
                    model{
                        name
                    }
                }
            }
            """
            % (model_id, random_int)
        )
        self.assertResponseHasErrors(response)

    def test_create_mutation_name_violates_unique_together_with_make(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        make = MakeFactory.create()
        model_dict = camelize(factory.build(dict, FACTORY_CLASS=ModelFactory,
                                            make=to_global_id(MakeNode._meta.name, make.id)))

        response = self.query(
            """
            mutation($input: CreateModelInput!) {
                createModel(input: $input) {
                    clientMutationId,
                    model {
                        id
                        name
                        make {
                          id
                        }
                    }
                }
            }
            """,
            input_data={'data': model_dict}
        )
        content = json.loads(response.content)
        generated_model = content['data']['createModel']['model']
        self.assertResponseNoErrors(response)
        self.assertEquals(model_dict['name'], generated_model['name'])
        self.assertEquals(model_dict['make'], generated_model['make']['id'])

        response = self.query(
            """
            mutation($input: CreateModelInput!) {
                createModel(input: $input) {
                    clientMutationId,
                    model {
                        id
                        name
                        make {
                          id
                        }
                    }
                }
            }
            """,
            input_data={'data': model_dict}
        )
        self.assertResponseHasErrors(response)
