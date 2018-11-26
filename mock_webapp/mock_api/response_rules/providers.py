from mock_api.response_rules.errors import InvalidResponseRuleMatcher, MatchingResponseRuleNotFound
from mock_api.response_rules.rule_matchers import BaseRuleMatcher


class ResponseRuleProvider(object):

    def __init__(self):
        self.matcher_classes = {}

    def register_matcher_class(self, response_rule_matcher_cls):
        if not issubclass(response_rule_matcher_cls, BaseRuleMatcher):
            raise InvalidResponseRuleMatcher(
                "{} is not {} subclass".format(response_rule_matcher_cls, BaseRuleMatcher))
        self.matcher_classes[response_rule_matcher_cls.rule_name()] = response_rule_matcher_cls

    def allowed_matchers_rules_choices(self):
        return list((i, i) for i in sorted(self.matcher_classes.keys()))

    def get_matcher(self, rule, param_name, param_value):
        response_rule_cls = self.matcher_classes.get(rule)
        if response_rule_cls:
            return response_rule_cls(param_name, param_value)
        else:
            raise MatchingResponseRuleNotFound("No ResponseRule class for rule: {}".format(rule))
