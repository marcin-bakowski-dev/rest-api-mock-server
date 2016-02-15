# REST API mock ![Build status](https://img.shields.io/shippable/56c1ce381895ca4474740463.svg)

# Overview

REST API mock server is simple webapp based on Django framework. Django admin interface was used to setup mock api endpoints and view access logs.

# Requirements

* Python (2.7, 3.4)
* Django (1.8)
* Django REST framework (3.2)
* Django CORS headers (1.1)
* Requests (2.7)
* Mock (1.3)

# Installation

Install requirements using `pip`...

    pip install -r requirements.txt

Create database and admin user:

    cd mock_webapp
    python manage.py syncdb

Start server:

    python manage.py runserver

Login to admin web interface and start defining api endpoints:

    http://127.0.0.1:8000/admin/


# Setup API Endpoint

Api endpoint model attributes:

* api endpoint path (URI)
* request method to handle
* default response
* set of response rules to return different response than default one (optional)
* set of callback to make outgoing http request when api endpoint is used (optional)

Api response model attributes:

* name (internal usage only to identify response in admin interface)
* status code
* content (optional) - content if provided must be valid json structure. Content can be empty.

Api response rules are optional. Api response rules allows to define response which will be used when rule is matched.
Response rules give a possibility to defined multiple responses for single api endpoint.
Api response model attributes:

* name (internal use only)
* response object - response that will be used when rule is matched
* possible rules - in current version there are 3 simple rules defined (param exists, param contains value, param not contains value).
New rules can be added by extending BaseRuleMatcher class and registering it to rules provider.
* param name (optional)
* param value (optional)

Api callback model attributes:

* name (internal usage only)
* url
* method
* additional request params (optional)
* additional request headers (optional)


REST API mock logs all request&response which are handled by mock view. Admin interface allows to view the access logs
and re-run manually api endpoint callbacks from access log detailed view.

Response format
---------------

REST API mock supports different response content type (html/json).
To chose response content type format user can use query param 'format' or one of content negotiation http headers (ex. Accept).

Example:

    curl -vv http://127.0.0.1:8000/api/items/?format=json
    *   Trying 127.0.0.1...
    * Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
    > GET /api/items/?format=json HTTP/1.1
    > User-Agent: curl/7.35.0
    > Host: 127.0.0.1:8000
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Server: WSGIServer/0.1 Python/2.7.6
    < Vary: Accept
    < X-Frame-Options: SAMEORIGIN
    < Content-Type: application/json
    < Allow: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
    <
    * Closing connection 0
    {"status":"OK"}


Response rules example
----------------------

There is an API endpoint defined with one response rule:

    URI: /api/items/
    method: GET
    default response:
        status: 200
        content: {"status":"OK"}
    response rule:
       name: generic 404
       response:
            status: 404
            content: {"status": "not found"}
       rule:
            param_contants_value: test="%not_found%"


By default default response is returned:

    curl -vv http://127.0.0.1:8000/api/items/?format=json
    *   Trying 127.0.0.1...
    * Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
    > GET /api/items/?format=json HTTP/1.1
    > User-Agent: curl/7.35.0
    > Host: 127.0.0.1:8000
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Server: WSGIServer/0.1 Python/2.7.6
    < Vary: Accept
    < X-Frame-Options: SAMEORIGIN
    < Content-Type: application/json
    < Allow: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
    <
    * Closing connection 0
    {"status":"OK"}


But when test=not_found is used in query params, response for 'generic 404' rule is returned

    curl -vv "http://127.0.0.1:8000/api/items/?format=json&test=not_found"
    *   Trying 127.0.0.1...
    * Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
    > GET /api/items/?format=json&test=not_found HTTP/1.1
    > User-Agent: curl/7.35.0
    > Host: 127.0.0.1:8000
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 404 NOT FOUND
    < Server: WSGIServer/0.1 Python/2.7.6
    < Vary: Accept
    < X-Frame-Options: SAMEORIGIN
    < Content-Type: application/json
    < Allow: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
    <
    * Closing connection 0
    {"status":"not found"}


Response rules can be easily extended by providing new rule matcher classes.


# TODO

* Store api endpoint states after handling (POST, PUT, PATCH, DELETE) requests (by defining additional actions to apply on endpoint response)
* More complex response rules mechanism (join multiple rules with logic AND/OR/NOT)
* run callbacks in non-blocking/asynchronous way
* Validate callback urls to prevent callback loops
