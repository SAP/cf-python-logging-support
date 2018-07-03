import os

from django.test import Client


os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'


def test_view():
    c = Client()
    response = c.get("/")
    assert response.content.decode() == 'Hello test!'