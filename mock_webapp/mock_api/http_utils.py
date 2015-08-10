# -*- coding: utf-8 -*-
import json
import logging

import re
import requests
from requests.exceptions import RequestException

from mock_api.models import AccessLog

logger = logging.getLogger(__name__)

REGEX_HTTP = re.compile(r'^HTTP_.+$')
REGEX_CONTENT_TYPE = re.compile(r'^CONTENT_TYPE$')
REGEX_CONTENT_LENGTH = re.compile(r'^CONTENT_LENGTH$')
REGEX_REMOTE = re.compile(r'^REMOTE_.+$')

REGEX_HEADERS = (REGEX_HTTP, REGEX_CONTENT_TYPE, REGEX_CONTENT_LENGTH, REGEX_REMOTE)


def get_request_headers(request):
    http_headers = {}
    for header, value in request.META.items():
        if any(re.match(pattern, header) for pattern in REGEX_HEADERS):
            http_headers[header] = value
    return http_headers


def get_response_headers(response):
    data = dict(response.items())
    data["Status code"] = response.status_code
    return data


def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')


def get_query_string(request):
    return request.META.get('QUERY_STRING', '')


def log_request_and_response(request, response):
        return AccessLog.objects.create(path=request.path_info,
                                        user_agent=get_user_agent(request),
                                        request_method=request.method,
                                        request_headers=json.dumps(get_request_headers(request)),
                                        request_query_string=get_query_string(request),
                                        request_data=json.dumps(request.data),
                                        response_status_code=response.status_code,
                                        response_headers=json.dumps(get_response_headers(response)),
                                        response_content=json.dumps(response.data))


def make_request(method, url, params=None, headers=None):
    try:
        return requests.request(method, url, params=params, headers=headers)
    except RequestException as e:
        logger.exception(e)
