from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('create/', views.create_view, name='create'),
    path('<int:exercise_id>/', views.detail_view, name='detail'),
]
