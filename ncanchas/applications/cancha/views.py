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
from django.views.generic.edit import FormView

#app zona
from applications.zona.models import Zone

#local app
from .models import Cancha
from .forms import (
    SearchForm,
    ComentarysForm,
    CanchaForm
)


class SearchCanchaView(ListView):
    """ vista que busca canchas"""

    context_object_name = 'canchas'
    template_name = 'cancha/index.html'

    def get_context_data(self, **kwargs):
        context = super(SearchCanchaView, self).get_context_data(**kwargs)
        context['form'] = SearchForm
        #contexto para realizar filtros
        context['len_request'] = len(self.request.GET)
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("kword", '')
        r = self.request.GET.get("filtro", '')
        if r == 'todos':
            r = ''
        #
        queryset = Cancha.objects.search_cancha(q, r)
        return queryset


class ZoneFilterCanchaView(ListView):
    """ vista que filtra canchas por zona"""

    context_object_name = 'canchas'
    template_name = 'cancha/by_zone.html'

    def get_context_data(self, **kwargs):
        context = super(ZoneFilterCanchaView, self).get_context_data(**kwargs)
        context['zona'] = Zone.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        slug=self.kwargs['slug']
        queryset = Cancha.objects.filter_cancha_by_zone(slug)
        return queryset


class CanchaDetailView(FormView):
    template_name = "cancha/detail.html"
    form_class = ComentarysForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(CanchaDetailView, self).get_context_data(**kwargs)
        #recuperamos la cancha
        cancha = Cancha.objects.get(slug=self.kwargs['slug'])
        #actualizamos el numero de visitas de la cancha
        cancha.vists = cancha.vists + 1
        cancha.save()
        #enviaos contexto
        context['cancha'] = cancha
        context['canchas'] = Cancha.objects.relations_canchas(cancha)
        return context

    def form_valid(self, form):
        print('codigo pendiente')
        return super(CanchaDetailView, self).form_valid(form)


class CanchaCreateView(CreateView):
    """
        vista que registra canchas nuevas
    """
    model = Cancha
    form_class = CanchaForm
    success_url = '.'
    template_name = 'cancha/register.html'

    def form_valid(self, form):
        cancha = form.save()
        #si existe usuario registramos usuario
        if self.request.user.is_authenticated:
            cancha.user_created = self.request.user
            cancha.save()

        #completado el registro mandamos a mensaje de con
        return HttpResponseRedirect(
                    reverse(
                        'cancha_app:cancha_confimacion',
                        kwargs={'slug': cancha.slug },
                    )
                )


class MessaggeView(TemplateView):
    """
        vista que muestra mensaje de confirmacion a cancha registrada
    """
    template_name = 'cancha/menssagge.html'

    def get_context_data(self, **kwargs):
        context = super(MessaggeView, self).get_context_data(**kwargs)
        #recuperamos la cancha
        cancha = Cancha.objects.get(slug=self.kwargs['slug'])
        #enviaos contexto
        context['cancha'] = cancha
        return context


class FindStructureView(TemplateView):
    """
        vista que busque canchas por estructura
    """

    template_name = 'cancha/filterstructure.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FindStructureView, self).get_context_data(**kwargs)
        structure = self.kwargs['structure']
        structure = structure.lower()
        cancha = Cancha.objects.search_structure_for_cancha(structure)
        context['structure'] = cancha
        return context
