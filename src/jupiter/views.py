from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from models import AuthUser
from forms import AuthUserCreationForm


# Create your views here.
class SignUpView(SuccessMessageMixin, CreateView):
    model = AuthUser
    template_name = 'registration/signup.html'
    form_class = AuthUserCreationForm

    success_url = '/login'
    success_message = 'Your account has been created. Login now!'

    def get_success_message(self, cleaned_data):
        return self.success_message


def home(request):
    return render(request, 'index.html', {})


def handler403(request):
    return JsonResponse({'status': 'error'}, status=403)


def handler404(request):
    return JsonResponse({'status': 'error'}, status=404)


def handler500(request):
    return JsonResponse({'status': 'error'}, status=500)
