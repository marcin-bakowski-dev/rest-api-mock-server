# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mock_api.authentication import MockNoAuthentication
from mock_api.http_utils import log_request_and_response
from mock_api.models import ApiEndpoint


class MockApiView(APIView):
    authentication_classes = (MockNoAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            api_endpoint = ApiEndpoint.objects.get(path=request.path_info, method=request.method)
            return Response(status=api_endpoint.status_code, data=api_endpoint.get_response())
        except ApiEndpoint.DoesNotExist:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED, data="NOT IMPLEMENTED")

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(MockApiView, self).finalize_response(request, response, *args, **kwargs)
        log_request_and_response(request, response)
        return response

    post = get
    patch = get
    delete = get
    put = get
    options = get
