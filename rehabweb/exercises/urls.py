from django.urls import path
from . import views
import uuid

app_name = 'exercises'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('exercises/', views.list_view, name='list'),
    path('create/', views.create_view, name='create'),
    path('<uuid:exercise_id>/', views.detail_view, name='detail'),
    path('<uuid:exercise_id>/edit/', views.edit_view, name='edit'),
]
