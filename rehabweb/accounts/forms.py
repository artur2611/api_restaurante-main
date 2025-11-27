from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'aria-label': 'Usuario',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'aria-label': 'Contraseña',
        })
    )
#se agrego el formulario de registro
class SignupForm(forms.Form):
    nombre = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo',
        })
    )

    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono',
        }),
        required=False
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
            'type': 'date'
        }),
        required=False
    )

    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
        })
    )
    
class UserAPIForm(forms.Form):

    def __init__(self, *args, token=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        
        # Obtener usuarios y ejercicios de la API
        
        roles_choices = [('', '-- Selecciona un ROL --') , ('paciente', 'Paciente'), ('terapeuta', 'Terapeuta'), ('admin', 'Administrador')]
        
        
        # Actualizar los fields con las opciones dinámicas
        self.fields['rol'] = forms.ChoiceField(
            label='Rol de usuario',
            choices=roles_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=True
        )
        
        
        
    nombre = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    # rol = forms.CharField(
        # required=False,
        # widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    
    contrasena = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )