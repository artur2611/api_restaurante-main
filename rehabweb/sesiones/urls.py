from django.urls import path
from . import views
import uuid

app_name = 'sesiones'

urlpatterns = [
    path('', views.sesion_list_view, name='list'),
    #path('sesiones/crear', views.create_view, name='create'),
    #path('sesiones/<uuid:sesion_id>/', views.detail_view, name='detail'),
    #path('sesiones/<uuid:sesion_id>/edit/', views.edit_view, name='edit'),
]
