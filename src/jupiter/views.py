from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from models import AuthUser
from forms import AuthUserCreationForm
from decorators import allow

# Create your views here.
class SignUpView(SuccessMessageMixin, CreateView):
    model = AuthUser
    template_name = 'registration/signup.html'
    form_class = AuthUserCreationForm

    success_url = '/'
    success_message = 'Your account has been created. Login now!'

    def get_success_message(self, cleaned_data):
        return self.success_message

def home(request):
    return render(request, 'home.html', {})

def handler403(request):
    return render(request, 'error/403.html', {})

def handler404(request):
    return render(request, 'error/404.html', {})

def handler500(request):
    return render(request, 'error/500.html', {})