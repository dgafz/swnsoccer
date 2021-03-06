from django.db import models
from django.db.models import Count, Max
from django.contrib.postgres.search import TrigramSimilarity

class CanchaManager(models.Manager):
    """procedimiento para cancha"""

    def search_cancha(self, name, filtro):
        """funcion que busca canchas"""

        # primero realizamos filtro
        if (filtro != ''):
            if filtro == 'parking':
                filtrado = self.filter(
                    state=True,
                    parking=True,
                )
            else:
                filtrado = self.filter(
                    state=True,
                    parking=False,
                )
        else:
            filtrado = self.filter(
                state=True,
            )

        #verificamos si nombre tiene mas de 3 digitos
        if len(name) > 3:
            #filtramos por nombre
            consulta = filtrado.filter(
                name__trigram_similar=name,
            ).order_by('-vists')
            #por direccion
            consulta1 = filtrado.filter(
                addresse__trigram_similar=name,
            ).order_by('-vists')
            #filtramos por zona
            consulta2 = filtrado.filter(
                zone__name__trigram_similar=name,
            ).order_by('-vists')
            #filtramos por distrito
            consulta3 = filtrado.filter(
                zone__distrito__name__trigram_similar=name,
            ).order_by('-vists')

            resultado = consulta | consulta1 | consulta2 | consulta3
            return resultado.distinct()
        else:
            return filtrado.filter(
                name__icontains=name,
            ).order_by('-vists')[:30]

    def relations_canchas(self, cancha):
        """ funcion que devuleve canchas relaciondas"""
        zones = []
        for z in cancha.zone.all():
            zones.append(z.pk)

        return self.filter(
            state = True,
            zone__in=zones,
        ).order_by('-vists').distinct()[:5]

    def agrupar_distrito_cancha(self, distrito):
        """ devuelve un distrito con total de canchas y con cancha mas visitada"""

        consulta = self.filter(
            state=True,
            zone__distrito__pk=distrito.pk
        )

        #cancha mas visitada
        cancha_max = consulta.annotate(
            Max('vists')
        )

        print('cancha_max', cancha_max)

        if consulta.count() > 0:
            resultado = {
                'slug': distrito.slug,
                'name': distrito.name,
                'count': consulta.count(),
                'image': cancha_max[0].image
            }
        else:
            resultado = {
                'slug': distrito.slug,
                'name': distrito.name,
                'count': 0,
                'image': None
            }
        return resultado

    def filter_cancha_by_zone(self, zona):
        return self.filter(
            state=True,
            zone__slug=zona,
        ).order_by(
            '-vists'
        ).order_by(
            'name'
        )

    def search_structure_for_cancha(self, var):
        #buscar por structurure
            if var == 'con-techo':
                #con techo
                return self.filter(
                    techo=True,
                    state=True,
                    anulate=False,
                ).order_by('name')[:20]

            elif var == 'sin-techo':
                 #sin techo
               return self.filter(
                    techo=False,
                    state=True,
                    anulate=False
                ).order_by('name')[:20]

            elif var == 'con-parking':
                #con parking
               return self.filter(
                    parking=True,
                    state=True,
                    anulate=False
                ).order_by('name')[:20]

            elif var == 'todo':
                #todo
                return self.filter(
                    state=True,
                    anulate=False
                ).order_by('name')[:20]
            else:
                print('no encontrado')
