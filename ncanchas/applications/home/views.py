# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#django library
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
    View,
)

# import app canchas
from applications.cancha.models import Cancha

# import local app
from .models import Home
from .forms import KwordForm
#

class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        #si tenemos in kword mandamos a busqeuda
        if len(self.request.GET) > 0:
            print('en el otro get', self.request.GET.get('csrfmiddlewaretoken'))
            url1 = 'cancha-de-gras/?csrfmiddlewaretoken='
            url2 = str(self.request.GET.get('csrfmiddlewaretoken'))+'&kword='+self.request.GET.get('kword')
            return HttpResponseRedirect(url1+url2)
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        #contexto principal
        #recuperamos pagina principal de la bd
        context['home'] = Home.objects.all()[0]
        context['form'] = KwordForm
        context['canchas'] = Cancha.objects.search_cancha('','')
        return context


class PlantillaView(TemplateView):
    template_name = 'plantilla/menssagge.html'
