from django.conf.urls import url
#from django.conf.urls import path
from . import views

urlpatterns = [
    url(r'^.*$', views.calcTIRADSscore, name='calcTIRADSscore'), #this regex means add nothing
    url(r'^(?P<mrn>[A-Za-z0-9]+)/(?P<accession>[A-Za-z0-9]+)$', views.calcTIRADSscore, name='calcTIRADSscore'),
    url(r'^[A-Za-z0-9]+[^ABC]+$', views.calcTIRADSscore, name='calcTIRADSscore'),
]
