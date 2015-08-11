# -*- coding: utf-8 -*-
import logging

from django.conf import settings

from mock_api.http_utils import make_request

logger = logging.getLogger(__name__)


def run_api_endpoint_callbacks(api_endpoint):
    responses = []
    for api_callback in api_endpoint.callbacks.all():
        logger.debug("Make callback: %s", api_callback)
        response = make_request(method=api_callback.method, url=api_callback.url, params=api_callback.get_params(),
                                headers=api_callback.get_headers(), timeout=settings.DEFAULT_CALLBACK_REQUEST_TIMEOUT)
        if response:
            logger.debug("Callback response status code: %s", response.status_code)
            responses.append(response)
    return responses
