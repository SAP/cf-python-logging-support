from django.conf.urls import url

from example.views import index

urlpatterns = [
    url("^$", index, name='log-index'),
]