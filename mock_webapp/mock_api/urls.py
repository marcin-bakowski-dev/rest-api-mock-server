from django.conf.urls import url

from mock_api.views import MockApiView

urlpatterns = [
    url(r'^.*$', MockApiView.as_view())
]
