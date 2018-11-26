import json

from django import forms
from rest_framework import status

from mock_api.models import ApiEndpoint, ApiResponseRule, ApiResponse, ApiCallback
from mock_api.response_rules import response_rules_provider

HTTP_ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS')
HTTP_STATUS_CODES = ((getattr(status, c), c) for c in dir(status) if c.startswith("HTTP_"))


class ApiResponseRuleForm(forms.ModelForm):
    rule = forms.ChoiceField(choices=response_rules_provider.allowed_matchers_rules_choices())

    class Meta:
        model = ApiResponseRule
        fields = ("name", "response", "rule", "param_name", "param_value")


class ApiEndpointForm(forms.ModelForm):
    method = forms.ChoiceField(choices=tuple((m, m) for m in HTTP_ALLOWED_METHODS))

    class Meta:
        model = ApiEndpoint
        fields = ("path", "method", "response", "response_rules", "callbacks")


class ApiResponseForm(forms.ModelForm):
    status_code = forms.ChoiceField(choices=HTTP_STATUS_CODES)
    content = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = ApiResponse
        fields = ("name", "status_code", "content")

    def clean_content(self):
        content = self.cleaned_data.get('content')
        _validate_json(content)
        return content


class ApiCallbackForm(forms.ModelForm):
    method = forms.ChoiceField(choices=tuple((m, m) for m in HTTP_ALLOWED_METHODS))
    params = forms.CharField(required=False, widget=forms.Textarea)
    headers = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = ApiCallback
        fields = ("name", "url", "method", "params", "headers")

    def clean_params(self):
        params = self.cleaned_data.get('params')
        _validate_json(params)
        return params

    def clean_headers(self):
        headers = self.cleaned_data.get('headers')
        _validate_json(headers)
        return headers


def _validate_json(string_data):
    if string_data:
        try:
            json.loads(string_data)
        except ValueError as e:
            raise forms.ValidationError("JSON structure is invalid: %s" % e)
