from django.contrib import admin
from mock_api.forms import ApiEndpointForm
from mock_api.models import ApiEndpoint, AccessLog


class ApiEndpointAdmin(admin.ModelAdmin):
    form = ApiEndpointForm
    list_display = ('method', 'path', 'status_code')


class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('request_time', 'user_agent', 'request_method', 'path', 'response_status_code')
    readonly_fields = ('request_time', 'user_agent', 'request_method', 'path', 'request_headers',
                       'request_query_params', 'request_data', 'response_status_code', 'response_headers',
                       'response_content')

    def has_add_permission(self, request):
        return False


admin.site.register(ApiEndpoint, ApiEndpointAdmin)
admin.site.register(AccessLog, AccessLogAdmin)
