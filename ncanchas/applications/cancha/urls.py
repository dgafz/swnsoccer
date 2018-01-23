# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

app_name="cancha_app"

urlpatterns = [
    #url para pantalla de inicio
    url(r'^cancha-de-gras/$',
        views.SearchCanchaView.as_view(),
        name='cancha_search'
    ),
	#url para detalle cancha
    url(r'^detalle/(?P<slug>[-\w]+)/$',
        views.CanchaDetailView.as_view(),
        name='cancha_detalle'
    ),
]
