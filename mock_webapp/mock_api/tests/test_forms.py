from django.test import TestCase

from mock_api.forms import ApiResponseForm, ApiEndpointForm, ApiResponseRuleForm


# noinspection PyCallingNonCallable
class BaseFormTest(TestCase):
    form_cls = None
    DATA = {}

    def data(self, **kwargs):
        form_data = {}
        form_data.update(self.DATA, **kwargs)
        return form_data

    def assert_form_is_not_valid(self, data, error_field):
        form = self.form_cls(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn(error_field, form.errors)

    def assert_form_is_valid(self, data):
        form = self.form_cls(data=data)

        self.assertTrue(form.is_valid())


class ApiResponseFormTest(BaseFormTest):

    DATA = {"name": "Default OK",
            "status_code": 200,
            "response": '{"test": "case"}'}
    form_cls = ApiResponseForm

    def test_empty_status_code(self):
        self.assert_form_is_not_valid(self.data(status_code=""), "status_code")

    def test_invalid_status_code(self):
        self.assert_form_is_not_valid(self.data(status_code="INVALID"), "status_code")

    def test_invalid_response(self):
        self.assert_form_is_not_valid(self.data(content="{INVALID"), "content")

    def test_valid_form(self):
        self.assert_form_is_valid(self.data())


class ApiEndpointFormTest(BaseFormTest):

    DATA = {"path": "/api/test",
            "method": "GET",
            "response": 1,
            "response_rules": [1]}
    form_cls = ApiEndpointForm
    fixtures = ('test_api.json',)

    def test_empty_path(self):
        self.assert_form_is_not_valid(self.data(path=""), "path")

    def test_empty_method(self):
        self.assert_form_is_not_valid(self.data(method=""), "method")

    def test_invalid_method(self):
        self.assert_form_is_not_valid(self.data(method="INVALID"), "method")

    def test_valid_form(self):
        self.assert_form_is_valid(self.data())


class ApiResponseRuleFormTest(BaseFormTest):

    DATA = {"name": "response rule name",
            "response": "1",
            "rule": "PARAM_CONTAINS_VALUE",
            "param_name": "test",
            "param_value": "not_found"}
    form_cls = ApiResponseRuleForm
    fixtures = ('test_api.json',)

    def test_form_invalid_rule(self):
        self.assert_form_is_not_valid(self.data(rule="INVALID"), "rule")

    def test_form_is_valid(self):
        self.assert_form_is_valid(self.data())
