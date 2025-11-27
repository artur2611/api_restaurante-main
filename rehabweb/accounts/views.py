from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from core.decorators import api_login_required
from core import api_client
from .forms import LoginForm, SignupForm
from core import api_client
from .forms import UserAPIForm

@api_login_required
def users_list_view(request):
    token = request.session.get('api_token')
    try:
        users = api_client.get_users(token)
        users = users.get('usuarios', [])
        print("USUARIOS EN LA VISTA LISTA:", users)
    except Exception as exc:
        messages.error(request, 'Failed to retrieve users from API.')
        users = []
    return render(request, 'accounts/list.html', {'users': users})

@api_login_required
def detail_view(request, user_id):
    token = request.session.get('api_token')
    try:
        user = api_client.get_user(token, user_id)
    except Exception:
        messages.error(request, 'Failed to load user')
        return redirect(reverse('accounts:list'))
    return render(request, 'accounts/detail.html', {'user': user})

@api_login_required
def edit_user_view(request, user_id):
    """
    Editar usuario vía API externa.
    GET: obtiene usuario y muestra formulario.
    POST: envía datos actualizados a la API.
    """
    token = request.session.get('api_token')
    user = {}
    
    if request.method == 'POST':
        form = UserAPIForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                print("Payload para actualizar usuario:", payload)
                payload['fecha_nacimiento'] = str(payload['fecha_nacimiento'])
                api_client.update_user(token, user_id, payload)
            except Exception as exc:
                messages.error(request, f'No se pudo actualizar el usuario: {exc}')
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Usuario actualizado correctamente.')
                return redirect(reverse('accounts:list'))
    else:
        try:
            data = api_client.get_user(token, user_id)
            print("Datos del usuario obtenido de la API:", data)
        except Exception as exc:
            messages.error(request, f'No se pudo obtener el usuario: {exc}')
            return redirect(reverse('accounts:list'))

        # Mapear datos de la API → formulario
        data = data.get ('usuario')
        user = {
            'nombre': data.get('nombre', ''),
            'telefono': data.get('telefono', ''),
            'fecha_nacimiento': data.get('fecha_nacimiento'),
            'rol': data.get('rol', ''),
        }
        print(user)
        form = UserAPIForm(initial=user)

    return render(request, 'accounts/edit.html', {
        'form': form,
        'user': user
    })
    
    
    
@api_login_required
def create_view(request):
    """
    Crear nuevo usuario vía API externa.
    GET: muestra formulario vacío.
    POST: envía datos a la API para crear usuario.
    """
    token = request.session.get('api_token')
    
    if request.method == 'POST':
        form = UserAPIForm(request.POST)
        if form.is_valid():
            print("peyload para testear las respuestas de la api ", form.cleaned_data)
            payload = form.cleaned_data
            
            if payload.get('fecha_nacimiento'):
                payload['fecha_nacimiento'] = str(payload['fecha_nacimiento'])
            
            if not payload.get('contrasena'):
                messages.error(request, 'La contraseña es requerida')
                form.add_error('contrasena', 'La contraseña es requerida')
                return render(request, 'accounts/create.html', {
                    'form': form
                })
                
            try:
                print("Payload para crear usuario:", payload)
                
                api_client.create_user(token, payload)
            except Exception as exc:
                messages.error(request, f'No se pudo crear el usuario: {exc}')
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Usuario creado correctamente.')
                return redirect(reverse('accounts:list'))
    else:
        form = UserAPIForm()

    return render(request, 'accounts/create.html', {
        'form': form
    })
    

@api_login_required
def delete_view(request, user_id):
    token = request.session.get('api_token')
    try:
        api_client.delete_user(token, user_id)
        messages.success(request, 'Usuario eliminado correctamente.')
    except Exception as exc:
        messages.error(request, f'No se pudo eliminar el usuario: {str(exc)}')
    return redirect(reverse('accounts:list'))




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
                return redirect(reverse('accounts:list'))
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})



def logout_view(request):
    request.session.pop('api_token', None)
    request.session.pop('api_user', None)
    return redirect(reverse('accounts:login'))

