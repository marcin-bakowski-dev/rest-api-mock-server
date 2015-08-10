# -*- coding: utf-8 -*-
from mock_api.response_rules import response_rules_provider


class ResponseResolver(object):
    rules_provider = response_rules_provider

    def __init__(self, api_endpoint, response_rule_provider=None):
        self.api_endpoint = api_endpoint
        if response_rule_provider:
            self.rules_provider = response_rule_provider

    def resolve(self, request):
        for response_rule in self.api_endpoint.response_rules.all():
            matcher = self.rules_provider.get_matcher(response_rule.rule, response_rule.param_name,
                                                      response_rule.param_value)
            if matcher.match(request):
                return response_rule.response
        return self.api_endpoint.response
