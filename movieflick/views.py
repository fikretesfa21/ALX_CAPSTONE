from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home_view(request):
    """Home view - redirects to appropriate page based on authentication"""
    if request.user.is_authenticated:
        return redirect('movies:mood-selection')
    else:
        return redirect('accounts:login')

