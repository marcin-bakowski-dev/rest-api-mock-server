# -*- coding: utf-8 -*-
from rest_framework.response import Response

from mock_api.response_rules.providers import ResponseRuleProvider


class ResponseResolver(object):

    def __init__(self, api_endpoint, response_rule_provider):
        self.api_endpoint = api_endpoint
        self.response_rules_provider = response_rule_provider

    def resolve(self, request):
        for response_rule in self.api_endpoint.response_rules.all():
            matcher = self.response_rules_provider.get_matcher(response_rule.rule, response_rule.param_name,
                                                               response_rule.param_value)
            if matcher.match(request):
                return response_rule.response
        return self.api_endpoint.response
