from django.test import TestCase
from django.test import Client
from .models import Category, Dish
import json


class CategoryTest(TestCase):
    def setUp(self):
        pass

    def create_category(self):
        return Category.objects.create(name="Test", description="Test description")

    def test_category_creation(self):
        category = self.create_category()
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(str(category.name), category.name)


class GraphQLTestCase(TestCase):

    def setUp(self):
        self._client = Client()

    def query(self, query: str, op_name: str = None, input: dict = None):
        """
        Args:
            query (string) - GraphQL query to run
            op_name (string) - If the query is a mutation or named query, you must
                               supply the op_name.  For annon queries ("{ ... }"),
                               should be None (default).
            input (dict) - If provided, the $input variable in GraphQL will be set
                           to this value

        Returns:
            dict, response from graphql endpoint.  The response has the "data" key.
                  It will have the "error" key if any error happened.
        """
        body = {'query': query}
        if op_name:
            body['operation_name'] = op_name
        if input:
            body['variables'] = {'input': input}

        resp = self._client.post('/graphql/', json.dumps(body),
                                 content_type='application/json')
        jresp = json.loads(resp.content.decode())
        return jresp

    def assertResponseNoErrors(self, resp: dict, expected: dict):
        """
        Assert that the resp (as returned from query) has the data from
        expected
        """
        self.assertNotIn('errors', resp, 'Response had errors')
        self.assertEqual(resp['data'], expected, 'Response has correct data')

    def test_get_all_categories_empty(self):
        resp = self.query(' { allCategories { id, name, description } }')
        self.assertResponseNoErrors(resp, {'allCategories': []})
