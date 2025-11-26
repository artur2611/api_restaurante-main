from django.urls import path
from . import views
import uuid

app_name = 'sesiones'

urlpatterns = [
    path('', views.sesion_list_view, name='list'),
    path('crear/', views.create_view, name='create'),
    path('<uuid:sesion_id>/', views.detail_view, name='detail'),
    path('<uuid:sesion_id>/edit/', views.sesion_edit_view, name='edit'),
    path('<uuid:sesion_id>/delete/', views.delete_view, name='delete'),
]
