# -*- coding: utf-8 -*-
import json
from django import forms
from rest_framework import status
from mock_api.models import ApiEndpoint

HTTP_ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS')
HTTP_STATUS_CODES = ((getattr(status, c), c) for c in dir(status) if c.startswith("HTTP_"))


class ApiEndpointForm(forms.ModelForm):
    method = forms.ChoiceField(choices=tuple((m, m) for m in HTTP_ALLOWED_METHODS))
    status_code = forms.ChoiceField(choices=HTTP_STATUS_CODES)
    response = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = ApiEndpoint
        fields = ('path', 'method', 'status_code', 'response')

    def clean_response(self):
        response = self.cleaned_data.get('response')
        if response:
            try:
                json.loads(response)
            except ValueError as e:
                raise forms.ValidationError("response json structure is invalid: %s" % e)
        return response
