# -*- coding: utf-8 -*-
import json
from django import forms
from rest_framework import status
from mock_api.models import ApiEndpoint, ApiResponseRule, ApiResponse
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
        if content:
            try:
                json.loads(content)
            except ValueError as e:
                raise forms.ValidationError("content json structure is invalid: %s" % e)
        return content
