from django.conf.urls import url
import listener

urlpatterns = [
    url(r'^$', listener.activate_listener),
]
