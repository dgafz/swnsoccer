from django import forms

class SearchForm(forms.Form):
    '''
    formulario para buscar notas
    '''
    kword = forms.CharField(
        max_length='300',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Buscar por zona, distrito o nombre de campo deportivo'
            }
        )
    )