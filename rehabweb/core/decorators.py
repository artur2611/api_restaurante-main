from django.shortcuts import redirect
from core import api_client

def api_login_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('api_token'):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return _wrapped

def bloquear_pacientes(view_func):
    def _wrapped(request, *args, **kwargs):
        user = request.session.get('user')
        
        #print("USUARIO EN DECORADOR ADMIN:", user)
        if user.get('rol') == 'paciente':
            return redirect('exercises:home' , )
        return view_func(request, *args, **kwargs)
    return _wrapped

def bloquear_terapeutas(view_func):
    def _wrapped(request, *args, **kwargs):
        user = request.session.get('user')
        
        #print("USUARIO EN DECORADOR TERAPEUTA:", user)
        if user.get('rol') == 'terapeuta':
            return redirect('exercises:home' , )
        return view_func(request, *args, **kwargs)
    return _wrapped