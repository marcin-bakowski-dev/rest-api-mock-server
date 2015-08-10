from django.contrib import admin

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
    list_display = ('request_time', 'user_agent', 'request_method', 'path', 'response_status_code')
    readonly_fields = ('request_time', 'user_agent', 'request_method', 'path', 'request_headers',
                       'request_query_string', 'request_data', 'response_status_code', 'response_headers',
                       'response_content')

    def has_add_permission(self, request):
        return False


admin.site.register(ApiResponse, ApiResponseAdmin)
admin.site.register(ApiResponseRule, ApiResponseRuleAdmin)
admin.site.register(ApiCallback, ApiCallbackAdmin)
admin.site.register(ApiEndpoint, ApiEndpointAdmin)
admin.site.register(AccessLog, AccessLogAdmin)
