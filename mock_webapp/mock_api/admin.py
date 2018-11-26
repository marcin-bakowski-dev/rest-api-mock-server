from django.contrib import admin, messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, re_path

from mock_api import callbacks
from mock_api.forms import ApiResponseForm, ApiResponseRuleForm, ApiEndpointForm, ApiCallbackForm
from mock_api.models import ApiEndpoint, AccessLog, ApiResponse, ApiResponseRule, ApiCallback


class ApiResponseAdmin(admin.ModelAdmin):
    form = ApiResponseForm


class ApiResponseRuleAdmin(admin.ModelAdmin):
    form = ApiResponseRuleForm
    list_display = ('name', 'response', 'rule', 'param_name', 'param_value')


class ApiEndpointAdmin(admin.ModelAdmin):
    form = ApiEndpointForm
    list_display = ('method', 'path', 'response')


class ApiCallbackAdmin(admin.ModelAdmin):
    form = ApiCallbackForm
    list_display = ('name', 'url', 'method')


class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('request_time', 'api_endpoint', 'user_agent', 'request_method', 'path', 'response_status_code')
    readonly_fields = ('request_time', 'api_endpoint', 'user_agent', 'request_method', 'path', 'request_headers',
                       'request_query_string', 'request_data', 'response_status_code', 'response_headers',
                       'response_content')

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super(AccessLogAdmin, self).get_urls()
        urls.insert(0,
                    re_path(r'^(?P<pk>\d+)/run-api-endpoint-callbacks/$',
                            self.admin_site.admin_view(self.run_api_endpoint_callback),
                            name='run_api_endpoint_callback'))
        return urls

    def run_api_endpoint_callback(self, request, pk):
        access_log = self.get_object(request, pk)
        if not access_log:
            raise Http404("No access_log found")

        if access_log.api_endpoint:
            if access_log.api_endpoint.callbacks.exists():
                callbacks.run_api_endpoint_callbacks(access_log.api_endpoint)
                messages.add_message(request, messages.INFO,
                                     'Api endpoint {} callbacks were run'.format(access_log.api_endpoint))
            else:
                messages.add_message(request, messages.INFO,
                                     'No callbacks for api endpoint {}'.format(access_log.api_endpoint))

        return redirect(reverse("admin:mock_api_accesslog_change", args=(pk,)))


admin.site.register(ApiResponse, ApiResponseAdmin)
admin.site.register(ApiResponseRule, ApiResponseRuleAdmin)
admin.site.register(ApiCallback, ApiCallbackAdmin)
admin.site.register(ApiEndpoint, ApiEndpointAdmin)
admin.site.register(AccessLog, AccessLogAdmin)
