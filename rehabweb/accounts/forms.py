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

