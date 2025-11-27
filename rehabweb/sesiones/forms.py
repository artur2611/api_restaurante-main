from django import forms
from core import api_client

class SesionAPIForm(forms.Form):
    def __init__(self, *args, token=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        
        # Obtener usuarios y ejercicios de la API
        usuarios_choices = [('', '-- Selecciona un usuario --')]
        ejercicios_choices = [('', '-- Selecciona un ejercicio --')]
        
        try:
            # Obtener lista de usuarios
            usuarios_data = api_client.get_users(token=token)
            print("USUARIOS", usuarios_data)
            #print(usuarios_data, "Se obtuvieron los usuarios")
            for user in usuarios_data.get('usuarios', []):
                # Mostrar nombre pero guardar id
                label = f"{user.get('nombre', 'Sin nombre')}"
                usuarios_choices.append((user.get('id'), label))
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
        
        try:
            # Obtener lista de ejercicios
            ejercicios_data = api_client.get_exercises(token=token)
           # print("EJERCICIOS", ejercicios_data)
            for ej in ejercicios_data:
                # Mostrar número y descripción pero guardar id
                label = f"{ej.get('descripcion', 'Sin descripción')}"
                ejercicios_choices.append((ej.get('id'), label))
        except Exception as e:
            print(f"Error al obtener ejercicios: {e}")
        
        # Actualizar los fields con las opciones dinámicas
        self.fields['id_usuario'] = forms.ChoiceField(
            label='Usuario que realiza la sesión',
            choices=usuarios_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=True
        )
        
        self.fields['id_ejercicio'] = forms.ChoiceField(
            label='Ejercicio Asignado',
            choices=ejercicios_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
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


