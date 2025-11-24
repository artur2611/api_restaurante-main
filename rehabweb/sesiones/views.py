from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from core.decorators import api_login_required
from core import api_client
#from .forms import ExerciseAPIForm


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