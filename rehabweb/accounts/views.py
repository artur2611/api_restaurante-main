from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import LoginForm, SignupForm
from core import api_client


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                data = api_client.login(form.cleaned_data['username'], form.cleaned_data['password'])
            except Exception as exc:
                messages.error(request, 'Login failed. Check credentials or API availability.')
                form.add_error(None, str(exc))
            else:
                token = data.get('token') or data.get('access_token')
                user = data.get('user')
                request.session['api_token'] = token
                request.session['api_user'] = user
                return redirect(reverse('exercises:list'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

#se agrego la vista de registro
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                api_client.signup(
                    form.cleaned_data['nombre'],
                    form.cleaned_data['telefono'],
                    form.cleaned_data['fecha_nacimiento'],
                    form.cleaned_data['contrasena']
                )
            except Exception as exc:
                messages.error(request, f"Error al registrarse: {str(exc)}")
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Cuenta creada correctamente, ahora inicia sesión')
                return redirect(reverse('accounts:login'))
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})



def logout_view(request):
    request.session.pop('api_token', None)
    request.session.pop('api_user', None)
    return redirect(reverse('accounts:login'))