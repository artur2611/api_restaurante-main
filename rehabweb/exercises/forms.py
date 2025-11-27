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
    


    def __init__(self, *args, token=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        
        # Obtener usuarios y ejercicios de la API
        
        niveles_choices = [('', '-- Selecciona una DIFICULTAD --') , ('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')]
        
        
        # Actualizar los fields con las opciones dinámicas
        self.fields['dificultad'] = forms.ChoiceField(
            label='Nivel de dificultad',
            choices=niveles_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=True
        )
        
        
    # dificultad = forms.CharField(
        # label='Dificultad',
        # widget=forms.TextInput(attrs={'class': 'form-control'}),
        # required=False
    # )
