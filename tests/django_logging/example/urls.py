from django.conf.urls import url

from tests.django_logging.example.views import IndexView, UserLoggingView

urlpatterns = [
    url("^test/path$", IndexView.as_view(), name='log-index')
]
