# -*- coding: utf-8 -*-
from django import forms

class KwordForm(forms.Form):
    """ formulario para buscar  """

    kword = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'banner__copy__form__text',
                'placeholder': 'Buscar por zona, distrito o nombre de cancha'
            }
        )
    )
