import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from cars.models import Model, Trim
from cars.types import CarNode, ModelNode, TrimNode

from .factories import (
    CarFactory,
    ModelFactory,
    TrimFactory,
    TrimWithForeignFactory,
)

faker = Factory.create()


class Trim_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        TrimFactory.create_batch(size=3)

    def test_create_trim(self):
        """
        Ensure we can create a new trim object.
        """
        model = ModelFactory.create()

        trim_dict = camelize(factory.build(dict, FACTORY_CLASS=TrimFactory,
                                           model=to_global_id(ModelNode._meta.name, model.id)))

        response = self.query(
            """
            mutation($input: CreateTrimInput!) {
                createTrim(input: $input) {
                    clientMutationId,
                    trim {
                        id
                        name
                        model {
                          id
                        }
                    }
                }
            }
            """,
            input_data={'data': trim_dict}
        )
        content = json.loads(response.content)
        generated_trim = content['data']['createTrim']['trim']
        self.assertResponseNoErrors(response)
        self.assertEquals(trim_dict['name'], generated_trim['name'])
        self.assertEquals(trim_dict['model'], generated_trim['model']['id'])

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allTrim query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allTrim{
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
        trim_list = content['data']['allTrim']['edges']
        trim_list_qs = Trim.objects.all()
        for i, edge in enumerate(trim_list):
            trim = edge['node']
            self.assertEquals(trim['id'], to_global_id(TrimNode._meta.name, trim_list_qs[i].id))
            self.assertEquals(trim['name'], trim_list_qs[i].name)

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allTrim query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allTrim{
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
        trim_list = content['data']['allTrim']['edges']
        trim_count = len(trim_list)
        for i, edge in enumerate(trim_list, start=1):
            trim = edge['node']
            trim_id = trim['id']
            response = self.query(
                """
                mutation($input:DeleteTrimInput!) {
                   deleteTrim(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': trim_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            trim_list = content['data']['allTrim']['edges']
            new_len = len(trim_list)
            assert trim_count - i == new_len

    def test_update_mutation_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        trim = TrimFactory.create()
        trim_id = to_global_id(TrimNode._meta.name, trim.pk)
        trim_dict = factory.build(dict, FACTORY_CLASS=TrimFactory)
        response = self.query(
            """
            mutation($input: UpdateTrimInput!){
                updateTrim(input: $input) {
                    trim{
                        name
                    }
                }
            }
            """,
            input_data={
                'id': trim_id,
                'data': {
                    'name': trim_dict['name'],
                }
            }
        )
        self.assertResponseNoErrors(response)
        parsed_response = json.loads(response.content)
        updated_trim_data = parsed_response['data']['updateTrim']['trim']
        self.assertEquals(updated_trim_data['name'], trim_dict['name'])

    def test_update_mutation_name_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        trim = TrimFactory.create()
        trim_id = to_global_id(TrimNode._meta.name, trim.pk)
        random_int = faker.pyint()
        response = self.query(
            """
            mutation{
                updateTrim(input: {
                    id: "%s",
                    data:{
                        name: %s
                    }
                }) {
                    trim{
                        name
                    }
                }
            }
            """
            % (trim_id, random_int)
        )
        self.assertResponseHasErrors(response)
