import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from cars.models import Car, Trim
from cars.types import CarNode, TrimNode

from .factories import CarFactory, TrimFactory

faker = Factory.create()


class Car_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        CarFactory.create_batch(size=3)

    def test_create_car(self):
        """
        Ensure we can create a new car object.
        """
        trim = TrimFactory.create()

        car_dict = camelize(factory.build(dict, FACTORY_CLASS=CarFactory,
                            trim=to_global_id(TrimNode._meta.name, trim.id)))

        response = self.query(
            """
            mutation($input: CreateCarInput!) {
                createCar(input: $input) {
                    clientMutationId,
                    car {
                        id
                        owner
                        color
                        year
                        trim {
                          id
                        }
                    }
                }
            }
            """,
            input_data={'data': car_dict}
        )
        content = json.loads(response.content)
        generated_car = content['data']['createCar']['car']
        self.assertResponseNoErrors(response)
        self.assertEquals(car_dict['owner'], generated_car['owner'])
        self.assertEquals(car_dict['color'], generated_car['color'])
        self.assertEquals(car_dict['year'], generated_car['year'])
        self.assertEquals(car_dict['trim'], generated_car['trim']['id'])

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allCar query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allCar{
                    edges{
                        node{
                            id
                            owner
                            color
                            year
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        car_list = content['data']['allCar']['edges']
        car_list_qs = Car.objects.all()
        for i, edge in enumerate(car_list):
            car = edge['node']
            self.assertEquals(car['id'], to_global_id(CarNode._meta.name, car_list_qs[i].id))
            self.assertEquals(car['owner'], car_list_qs[i].owner)
            self.assertEquals(car['color'], car_list_qs[i].color)
            self.assertEquals(car['year'], car_list_qs[i].year)

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allCar query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allCar{
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
        car_list = content['data']['allCar']['edges']
        car_count = len(car_list)
        for i, edge in enumerate(car_list, start=1):
            car = edge['node']
            car_id = car['id']
            response = self.query(
                """
                mutation($input:DeleteCarInput!) {
                   deleteCar(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': car_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            car_list = content['data']['allCar']['edges']
            new_len = len(car_list)
            assert car_count - i == new_len

    def test_update_mutation_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        car = CarFactory.create()
        car_id = to_global_id(CarNode._meta.name, car.pk)
        car_dict = factory.build(dict, FACTORY_CLASS=CarFactory)
        response = self.query(
            """
            mutation($input: UpdateCarInput!){
                updateCar(input: $input) {
                    car{
                        owner
                        color
                        year
                    }
                }
            }
            """,
            input_data={
                'id': car_id,
                'data': {
                    'owner': car_dict['owner'],
                    'color': car_dict['color'],
                    'year': car_dict['year'],
                }
            }
        )
        self.assertResponseNoErrors(response)
        parsed_response = json.loads(response.content)
        updated_car_data = parsed_response['data']['updateCar']['car']
        self.assertEquals(updated_car_data['owner'], car_dict['owner'])
        self.assertEquals(updated_car_data['color'], car_dict['color'])
        self.assertEquals(updated_car_data['year'], car_dict['year'])

    def test_update_mutation_owner_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        car = CarFactory.create()
        car_id = to_global_id(CarNode._meta.name, car.pk)
        random_int = faker.pyint()
        response = self.query(
            """
            mutation{
                updateCar(input: {
                    id: "%s",
                    data:{
                        owner: %s
                    }
                }) {
                    car{
                        owner
                    }
                }
            }
            """
            % (car_id, random_int)
        )
        self.assertResponseHasErrors(response)

    def test_update_mutation_color_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        car = CarFactory.create()
        car_id = to_global_id(CarNode._meta.name, car.pk)
        random_str = faker.pystr()
        response = self.query(
            """
            mutation{
                updateCar(input: {
                    id: "%s",
                    data:{
                        color: %s
                    }
                }) {
                    car{
                        color
                    }
                }
            }
            """
            % (car_id, random_str)
        )
        self.assertResponseHasErrors(response)

    def test_update_mutation_year_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        car = CarFactory.create()
        car_id = to_global_id(CarNode._meta.name, car.pk)
        random_str = faker.pystr()
        response = self.query(
            """
            mutation{
                updateCar(input: {
                    id: "%s",
                    data:{
                        year: %s
                    }
                }) {
                    car{
                        year
                    }
                }
            }
            """
            % (car_id, random_str)
        )
        self.assertResponseHasErrors(response)
