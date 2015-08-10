# -*- coding: utf-8 -*-
from mock_api.response_rules.providers import ResponseRuleProvider
from mock_api.response_rules.rule_matchers import RequestParamMatcher


response_rules_provider = ResponseRuleProvider()
response_rules_provider.register_matcher_class(RequestParamMatcher)
