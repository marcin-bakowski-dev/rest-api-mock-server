# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from mock_api.models import ApiEndpoint
from mock_api.response_rules import response_rules_provider
from mock_api.response_rules.resolvers import ResponseResolver


class ResponseResolverTest(TestCase):

    fixtures = ('test_api.json',)
    PATH = "/api/items/"
    factory = APIRequestFactory()

    def setUp(self):
        self.api_endpoint = ApiEndpoint.objects.get(path=self.PATH, method="GET")
        self.resolver = ResponseResolver(self.api_endpoint, response_rules_provider)

    def test_default_response(self):
        request = Request(self.factory.get(self.PATH))

        response = self.resolver.resolve(request)

        self.assertEqual(response.pk, self.api_endpoint.response.pk)

    def test_alternative_response_from_response_rules(self):
        response_rule = self.api_endpoint.response_rules.first()
        request = Request(self.factory.get(self.PATH, data={response_rule.param_name: response_rule.param_value}))

        response = self.resolver.resolve(request)

        self.assertEqual(response.pk, response_rule.response.pk)
