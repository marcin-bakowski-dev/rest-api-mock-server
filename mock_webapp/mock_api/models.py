import json

from django.db import models


class ApiResponse(models.Model):
    name = models.CharField(max_length=100)
    status_code = models.IntegerField()
    content = models.TextField(blank=True, default="")

    ordering = ('name', 'status_code')

    def __unicode__(self):
        return u"ApiResponse: {}[{}]".format(self.name, self.status_code)

    def get_content(self):
        return json.loads(self.content) if self.content else None


class ApiResponseRule(models.Model):
    name = models.CharField(max_length=100)
    response = models.ForeignKey(ApiResponse)
    rule = models.CharField(max_length=50)
    param_name = models.CharField(max_length=100, blank=True, default="")
    param_value = models.CharField(max_length=100, blank=True, default="")

    def __unicode__(self):
        return u"ApiResponseRule: {}[{},{}]".format(self.rule, self.param_name, self.param_value)


class ApiCallback(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __unicode__(self):
        return u"ApiCallback: {}: {}".format(self.name, self.url)


class ApiEndpoint(models.Model):
    path = models.CharField(max_length=254)
    method = models.CharField(max_length=10)
    response = models.ForeignKey(ApiResponse)
    response_rules = models.ManyToManyField(ApiResponseRule, blank=True)
    callbacks = models.ManyToManyField(ApiCallback, blank=True)

    ordering = ('path', 'method')
    unique_together = (('path', 'method'),)

    def __unicode__(self):
        return u"{}: {}".format(self.method, self.path)


class AccessLog(models.Model):
    request_time = models.TimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=254, blank=True, default="")
    path = models.CharField(max_length=254)
    request_method = models.CharField(max_length=10)
    request_headers = models.TextField(blank=True, default="")
    request_query_string = models.TextField(blank=True, default="")
    request_data = models.TextField(blank=True, default="")
    response_status_code = models.IntegerField()
    response_headers = models.TextField(blank=True, default="")
    response_content = models.TextField(blank=True, default="")

    ordering = ('-request_time',)

    def __unicode__(self):
        return u"[{}]: {} [{}] {}".format(self.request_time, self.request_method, self.response_status_code, self.path)
