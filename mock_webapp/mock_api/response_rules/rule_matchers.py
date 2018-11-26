class BaseRuleMatcher(object):

    def __init__(self, param_name, param_value):
        self.param_name = param_name
        self.param_value = param_value

    def match(self, request):
        raise NotImplementedError

    @classmethod
    def rule_name(cls):
        raise NotImplementedError


class RequestParamExistsMatcher(BaseRuleMatcher):
    RULE = 'PARAM_EXISTS'

    @classmethod
    def rule_name(cls):
        return cls.RULE

    def match(self, request):
        data = _request_data(request)
        return self.param_name in data


class RequestParamContainsValueMatcher(BaseRuleMatcher):
    RULE = 'PARAM_CONTAINS_VALUE'

    @classmethod
    def rule_name(cls):
        return cls.RULE

    def match(self, request):
        data = _request_data(request)
        return _data_contains_value(data, self.param_name, self.param_value)


class RequestParamNotContainsValueMatcher(BaseRuleMatcher):
    RULE = 'PARAM_NOT_CONTAINS_VALUE'

    @classmethod
    def rule_name(cls):
        return cls.RULE

    def match(self, request):
        data = _request_data(request)
        return not _data_contains_value(data, self.param_name, self.param_value)


def _data_contains_value(data, key, value):
    return value in data.get(key) if data.get(key) else False


def _request_data(request):
    return request.query_params if request.method == 'GET' else request.data
