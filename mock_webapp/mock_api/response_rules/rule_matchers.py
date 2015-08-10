# -*- coding: utf-8 -*-
from mock_api.response_rules.errors import MatchingResponseRuleNotFound


class BaseRuleMatcher(object):

    def __init__(self, rule, param_name, param_value):
        self.rule = rule
        self.param_name = param_name
        self.param_value = param_value

    def match(self, request):
        raise NotImplementedError

    @classmethod
    def get_rules(cls):
        raise NotImplementedError


class RequestParamMatcher(BaseRuleMatcher):
    COMPARATORS = {
        'PARAM_EXISTS': lambda data, name, value: name in data,
        'PARAM_CONTAINS_VALUE': lambda data, name, value: data.get(name) and value in data.get(name),
        'PARAM_NOT_CONTAINS_VALUE': lambda data, name, value: value not in data.get(name),
    }

    @classmethod
    def get_rules(cls):
        return cls.COMPARATORS.keys()

    def match(self, request):
        comparator = self.COMPARATORS.get(self.rule)
        if comparator:
            return comparator(data=request.query_params if request.method == 'GET' else request.data,
                              name=self.param_name,
                              value=self.param_value)
        else:
            raise MatchingResponseRuleNotFound("No ResponseRule class for rule: {}".format(self.rule))
