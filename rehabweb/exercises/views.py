from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from core.decorators import api_login_required
from core import api_client
from .forms import ExerciseForm


@api_login_required
def list_view(request):
    token = request.session.get('api_token')
    exercises = []
    try:
        exercises = api_client.get_exercises(token)
    except Exception as exc:
        messages.error(request, 'Failed to load exercises from API')
    return render(request, 'exercises/list.html', {'exercises': exercises})


@api_login_required
def detail_view(request, exercise_id):
    token = request.session.get('api_token')
    try:
        exercise = api_client.get_exercise(token, exercise_id)
    except Exception:
        messages.error(request, 'Failed to load exercise')
        return redirect(reverse('exercises:list'))
    return render(request, 'exercises/detail.html', {'exercise': exercise})


@api_login_required
def create_view(request):
    token = request.session.get('api_token')
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                api_client.create_exercise(token, payload)
            except Exception:
                messages.error(request, 'Failed to create exercise')
            else:
                return redirect(reverse('exercises:list'))
    else:
        form = ExerciseForm()
    return render(request, 'exercises/form.html', {'form': form})
from django.shortcuts import render
from core import api_client
from core.decorators import api_login_required

@api_login_required
def list_view(request):
    token = request.session.get('api_token')
    exercises = api_client.get_exercises(token)
    return render(request, 'exercises/list.html', {'exercises': exercises})