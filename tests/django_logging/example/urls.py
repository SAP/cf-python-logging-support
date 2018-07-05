""" Urls for django example test app """
from django.conf.urls import url

from tests.django_logging.example.views import IndexView

# pylint: disable=invalid-name
urlpatterns = [
    url("^test/path$", IndexView.as_view(), name='log-index')
]
