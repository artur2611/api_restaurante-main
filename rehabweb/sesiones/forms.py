from django import forms

class SesionAPIForm(forms.Form):
    id_ejercicio = forms.CharField(
        label='ID del Ejercicio',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    id_usuario = forms.CharField(
        label='ID del Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    repeticiones_logradas = forms.IntegerField(
        label='Repeticiones logradas',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    maximo_nivel_logrado = forms.IntegerField(
        label='Máximo nivel logrado',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )

