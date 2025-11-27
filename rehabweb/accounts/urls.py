from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.users_list_view, name='list'),
    path('<uuid:user_id>/', views.detail_view, name='detail'),
    path('<uuid:user_id>/edit/', views.edit_user_view, name='edit'),
    path('create/', views.create_view, name='create'),
    path('<uuid:user_id>/delete/', views.delete_view, name='delete'),
    
    
]
