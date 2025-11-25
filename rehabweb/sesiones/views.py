from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from core.decorators import api_login_required
from core import api_client
from .forms import SesionAPIForm


@api_login_required
def sesion_list_view(request):
    token = request.session.get('api_token')
    sesiones = []
    try:
        sesiones = api_client.get_sesiones(token)
        print(sesiones)
    except Exception as exc:
        messages.error(request, 'Fallo al obtener las sesiones desde la API')
    return render(request, 'sesiones/list.html', {'sesiones': sesiones})

@api_login_required
def detail_view(request, sesion_id):
    token = request.session.get('api_token')
    try:
        sesion = api_client.get_sesion(token, sesion_id)
    except Exception:
        messages.error(request, 'Failed to load exercise')
        return redirect(reverse('sesiones:list'))
    return render(request, 'sesiones/detail.html', {'sesion': sesion})


@api_login_required
def create_view(request):
    token = request.session.get('api_token')
    if request.method == 'POST':
        form = SesionAPIForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            
            payload['id_ejercicio'] = str(payload['id_ejercicio'])
            payload['id_usuario'] =  str(payload['id_usuario'])
            try:
                api_client.create_sesion(token, payload)
            except Exception as exc:
                messages.error(request, 'No se pudo crear la sesión: %s' % str(exc))
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Sesión creada correctamente.')
                return redirect(reverse('sesiones:list'))
    else:
        form = SesionAPIForm()
    return render(request, 'sesiones/create.html', {'form': form})


@api_login_required
def sesion_edit_view(request, sesion_id):
    """
    Edit an exercise via external API.
    GET: fetch exercise from API and show form.
    POST: submit updated data to API.
    """
    token = request.session.get('api_token')
    sesion = {}
    if request.method == 'POST':
        
        form = SesionAPIForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                api_client.update_sesion(token, sesion_id, payload)
            except Exception as exc:
                messages.error(request, 'No se pudo actualizar la sesión: %s' % str(exc))
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Sesión actualizada correctamente.')
                return redirect(reverse('sesiones:list'))
    else:
        try:
            data = api_client.get_sesion(token, sesion_id)
            data = data.get("sesion")
            print(data , "-----------------")
        except Exception as exc:
            messages.error(request, 'No se pudo obtener la sesión: %s' % str(exc))
            return redirect(reverse('sesiones:list'))
        # map API response keys to form initial values if necessary
        sesion = {
            'maximo_nivel_logrado': data.get('maximo_nivel_logrado'),
            'repeticiones_logradas': data.get('repeticiones_logradas'),
            'id_usuario': data.get('id_usuario'),  
            'id_ejercicio': data.get('id_ejercicio'),
        }
        form = SesionAPIForm(initial=sesion)

    return render(request, 'sesiones/edit.html', {'form': form, 'sesion': sesion})

def home_view(request):
    """
    Página de inicio que hereda de base_regular.html.
    Muestra el logo de la empresa y un mensaje de bienvenida centrado.
    """
    context = {
        'welcome_message': 'Bienvenido a WebRehab'
    }
    return render(request, 'home.html', context)