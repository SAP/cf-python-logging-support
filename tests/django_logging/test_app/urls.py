""" Urls for example django test app """
from django.conf.urls import url

from tests.django_logging.test_app.views import IndexView

# pylint: disable=invalid-name
urlpatterns = [
    url("^test/path$", IndexView.as_view(), name='log-index')
]
