import json

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ApiResponse(models.Model):
    name = models.CharField(max_length=100)
    status_code = models.IntegerField()
    content = models.TextField(blank=True, default="")

    ordering = ('name', 'status_code')

    def __str__(self):
        return u"ApiResponse: {}[{}]".format(self.name, self.status_code)

    def get_content(self):
        return _deserialize_or_none(self.content)


@python_2_unicode_compatible
class ApiResponseRule(models.Model):
    name = models.CharField(max_length=100)
    response = models.ForeignKey(ApiResponse, on_delete=models.CASCADE)
    rule = models.CharField(max_length=50)
    param_name = models.CharField(max_length=100, blank=True, default="")
    param_value = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return u"ApiResponseRule: {}[{},{}]".format(self.rule, self.param_name, self.param_value)


@python_2_unicode_compatible
class ApiCallback(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    method = models.CharField(max_length=10)
    params = models.TextField(blank=True, default="")
    headers = models.TextField(blank=True, default="")

    def __str__(self):
        return u"ApiCallback: {}: {} {}".format(self.name, self.method, self.url)

    def get_params(self):
        return _deserialize_or_none(self.params)

    def get_headers(self):
        return _deserialize_or_none(self.headers)


@python_2_unicode_compatible
class ApiEndpoint(models.Model):
    path = models.CharField(max_length=254)
    method = models.CharField(max_length=10)
    response = models.ForeignKey(ApiResponse, on_delete=models.CASCADE)
    response_rules = models.ManyToManyField(ApiResponseRule, blank=True)
    callbacks = models.ManyToManyField(ApiCallback, blank=True)

    ordering = ('path', 'method')
    unique_together = (('path', 'method'),)

    def __str__(self):
        return u"{}: {}".format(self.method, self.path)


@python_2_unicode_compatible
class AccessLog(models.Model):
    request_time = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=254, blank=True, default="")
    path = models.CharField(max_length=254)
    request_method = models.CharField(max_length=10)
    request_headers = models.TextField(blank=True, default="")
    request_query_string = models.TextField(blank=True, default="")
    request_data = models.TextField(blank=True, default="")
    response_status_code = models.IntegerField()
    response_headers = models.TextField(blank=True, default="")
    response_content = models.TextField(blank=True, default="")
    api_endpoint = models.ForeignKey(ApiEndpoint, on_delete=models.CASCADE, blank=True, null=True)

    ordering = ('-request_time',)

    def __str__(self):
        return u"[{}]: {} [{}] {}".format(self.request_time, self.request_method, self.response_status_code, self.path)


def _deserialize_or_none(value):
    return json.loads(value) if value else None
