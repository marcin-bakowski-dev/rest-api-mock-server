# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mock_api.authentication import MockNoAuthentication
from mock_api.http_utils import log_request_and_response
from mock_api.models import ApiEndpoint
from mock_api.response_rules import response_rules_provider
from mock_api.response_rules.errors import MatchingResponseNotFound
from mock_api.response_rules.resolvers import ResponseResolver


class MockApiView(APIView):
    authentication_classes = (MockNoAuthentication,)
    response_resolver_class = ResponseResolver
    response_rule_provider = response_rules_provider

    def get(self, request, *args, **kwargs):
        try:
            api_endpoint = ApiEndpoint.objects.get(path=request.path_info, method=request.method)
            response = self.response_resolver_class(api_endpoint, self.response_rule_provider).resolve(request)
            return Response(status=response.status_code, data=response.get_content())
        except (ApiEndpoint.DoesNotExist, MatchingResponseNotFound):
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(MockApiView, self).finalize_response(request, response, *args, **kwargs)
        log_request_and_response(request, response)
        return response

    post = get
    patch = get
    delete = get
    put = get
    options = get
