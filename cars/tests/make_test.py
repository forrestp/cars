import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from cars.models import Make
from cars.types import MakeNode, ModelNode

from .factories import MakeFactory, MakeWithForeignFactory, ModelFactory

faker = Factory.create()


class Make_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        MakeFactory.create_batch(size=3)

    def test_create_make(self):
        """
        Ensure we can create a new make object.
        """

        make_dict = camelize(factory.build(dict, FACTORY_CLASS=MakeFactory))

        response = self.query(
            """
            mutation($input: CreateMakeInput!) {
                createMake(input: $input) {
                    clientMutationId,
                    make {
                        id
                        name
                    }
                }
            }
            """,
            input_data={'data': make_dict}
        )
        content = json.loads(response.content)
        generated_make = content['data']['createMake']['make']
        self.assertResponseNoErrors(response)
        self.assertEquals(make_dict['name'], generated_make['name'])

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allMake query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allMake{
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
        make_list = content['data']['allMake']['edges']
        make_list_qs = Make.objects.all()
        for i, edge in enumerate(make_list):
            make = edge['node']
            self.assertEquals(make['id'], to_global_id(MakeNode._meta.name, make_list_qs[i].id))
            self.assertEquals(make['name'], make_list_qs[i].name)

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allMake query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allMake{
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
        make_list = content['data']['allMake']['edges']
        make_count = len(make_list)
        for i, edge in enumerate(make_list, start=1):
            make = edge['node']
            make_id = make['id']
            response = self.query(
                """
                mutation($input:DeleteMakeInput!) {
                   deleteMake(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': make_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            make_list = content['data']['allMake']['edges']
            new_len = len(make_list)
            assert make_count - i == new_len

    def test_update_mutation_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        make = MakeFactory.create()
        make_id = to_global_id(MakeNode._meta.name, make.pk)
        make_dict = factory.build(dict, FACTORY_CLASS=MakeFactory)
        response = self.query(
            """
            mutation($input: UpdateMakeInput!){
                updateMake(input: $input) {
                    make{
                        name
                    }
                }
            }
            """,
            input_data={
                'id': make_id,
                'data': {
                    'name': make_dict['name'],
                }
            }
        )
        self.assertResponseNoErrors(response)
        parsed_response = json.loads(response.content)
        updated_make_data = parsed_response['data']['updateMake']['make']
        self.assertEquals(updated_make_data['name'], make_dict['name'])

    def test_update_mutation_name_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        make = MakeFactory.create()
        make_id = to_global_id(MakeNode._meta.name, make.pk)
        random_int = faker.pyint()
        response = self.query(
            """
            mutation{
                updateMake(input: {
                    id: "%s",
                    data:{
                        name: %s
                    }
                }) {
                    make{
                        name
                    }
                }
            }
            """
            % (make_id, random_int)
        )
        self.assertResponseHasErrors(response)
