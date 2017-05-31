from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$',views.home),
    url(r'^logout/$', views.logout),
    url(r'^trip_add/$', views.trip_add, name="trip_add"),
    url(r'^destination/(?P<id>\d+)/$', views.destination, name="destination"),
    url(r'^join/(?P<id>\d+)/$', views.join, name="join"),
    # url(r'^validate/$', views.validate, name="validate"),
    # url(r'^success/$', views.success, name="success"),

]
