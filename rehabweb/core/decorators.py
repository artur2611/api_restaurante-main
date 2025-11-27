from django.shortcuts import redirect

def api_login_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('api_token'):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return _wrapped

# def api_admin_required(view_func):
#     def _wrapped(request, *args, **kwargs):
#         user = request.session.get('id')
#         if user.get('rol') != 'admin':
#             return redirect('exercises:home' , )
#         return view_func(request, *args, **kwargs)
#     return _wrapped