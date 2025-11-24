from django import forms

class ExerciseAPIForm(forms.Form):
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        required=True
    )
    numero_ejercicio = forms.IntegerField(
        label='Número de ejercicio',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )
    repeticiones_base = forms.IntegerField(
        label='Repeticiones',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )
    dificultad = forms.CharField(
        label='Dificultad',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
