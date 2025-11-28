from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from core.decorators import api_login_required , bloquear_pacientes, bloquear_terapeutas
from core import api_client
from .forms import ExerciseAPIForm
from core import api_client


@api_login_required
@bloquear_pacientes
def list_view(request):
    token = request.session.get('api_token')
    exercises = []
    try:
        exercises = api_client.get_exercises(token)
    except Exception as exc:
        messages.error(request, 'Fallo al obtener los ejercicios desde la API')
    return render(request, 'exercises/list.html', {'exercises': exercises})


@api_login_required 
@bloquear_pacientes
@bloquear_terapeutas
def detail_view(request, exercise_id):
    token = request.session.get('api_token')
    try:
        exercise = api_client.get_exercise(token, exercise_id)
    except Exception:
        messages.error(request, 'Failed to load exercise')
        return redirect(reverse('exercises:list'))
    return render(request, 'exercises/detail.html', {'exercise': exercise})

@api_login_required
@bloquear_pacientes
@bloquear_terapeutas
def delete_view(request, exercise_id):
    token = request.session.get('api_token')
    if request.method == 'POST':
        try:
            api_client.delete_exercise(token, exercise_id)
        except Exception as exc:
            messages.error(request, 'No se pudo eliminar el ejercicio: %s' % str(exc))
        else:
            messages.success(request, 'Ejercicio eliminado correctamente.')
        return redirect(reverse('exercises:list'))
    else:
        return render(request, 'exercises/delete.html', {'exercise_id': exercise_id})


@api_login_required
@bloquear_pacientes
@bloquear_terapeutas
def create_view(request):
    token = request.session.get('api_token')
    if request.method == 'POST':
        form = ExerciseAPIForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                api_client.create_exercise(token, payload)
            except Exception as exc:
                messages.error(request, 'No se pudo crear el ejercicio: %s' % str(exc))
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Ejercicio creado correctamente.')
                return redirect(reverse('exercises:list'))
    else:
        form = ExerciseAPIForm()
    return render(request, 'exercises/create.html', {'form': form})

@api_login_required
@bloquear_pacientes
@bloquear_terapeutas
def edit_view(request, exercise_id):
    """
    Edit an exercise via external API.
    GET: fetch exercise from API and show form.
    POST: submit updated data to API.
    """
    token = request.session.get('api_token')
    exercise = {}

    if request.method == 'POST':
        form = ExerciseAPIForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                api_client.update_exercise(token, exercise_id, payload)
            except Exception as exc:
                messages.error(request, 'No se pudo actualizar el ejercicio: %s' % str(exc))
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Ejercicio actualizado correctamente.')
                return redirect(reverse('exercises:list'))
    else:
        try:
            data = api_client.get_exercise(token, exercise_id)
            data = data.get("ejercicio")
        except Exception as exc:
            messages.error(request, 'No se pudo obtener el ejercicio: %s' % str(exc))
            return redirect(reverse('exercises:list'))
        # map API response keys to form initial values if necessary
        exercise = {
            'descripcion': data.get('descripcion', ''),
            'numero_ejercicio': data.get('numero_ejercicio'),
            'repeticiones_base': data.get('repeticiones_base'),
            'dificultad': data.get('dificultad', ''),
        }
        form = ExerciseAPIForm(initial=exercise)

    return render(request, 'exercises/edit.html', {'form': form, 'exercise': exercise})

def home_view(request):
    """
    Página de inicio que hereda de base_regular.html.
    Muestra el logo de la empresa y un mensaje de bienvenida centrado.
    """
    context = {
        'welcome_message': 'Bienvenido a WebRehab'
    }
    return render(request, 'home.html', context)