import json

from django.db import models


class ApiEndpoint(models.Model):
    path = models.CharField(max_length=254)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    response = models.TextField(blank=True, default="")

    ordering = ('path', 'method', 'status_code')

    def __unicode__(self):
        return u"{}: [{}] {}".format(self.method, self.status_code, self.path)

    def get_response(self):
        return json.loads(self.response) if self.response else None


class AccessLog(models.Model):
    request_time = models.TimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=254, blank=True, default="")
    path = models.CharField(max_length=254)
    request_method = models.CharField(max_length=10)
    request_headers = models.TextField(blank=True, default="")
    request_query_params = models.TextField(blank=True, default="")
    request_data = models.TextField(blank=True, default="")
    response_status_code = models.IntegerField()
    response_headers = models.TextField(blank=True, default="")
    response_content = models.TextField(blank=True, default="")

    ordering = ('-request_time',)

    def __unicode__(self):
        return u"[{}]: {} [{}] {}".format(self.request_time, self.request_method, self.response_status_code, self.path)
