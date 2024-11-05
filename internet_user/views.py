#Django shortcuts
from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

#Class based views
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView,TemplateView

#Model
from django.contrib.auth.models import User


#Forms
from django.contrib.auth.forms import UserCreationForm
from .forms import InternetUserCreationForm


# Create your views here.

#Create User
class CreateInternetUserView(CreateView):
    form_class = InternetUserCreationForm
    template_name = "user_temp/signup.html"
    success_url = reverse_lazy("login")

#my_profile
class DetailInternetUserView(LoginRequiredMixin,DetailView):
    model = User
    template_name = "user_temp/my_profile.html"

#Update user
class UpdateInternetUserView(UpdateView):
    fields = ["email"]
    model = User
    template_name = "user_temp/update_account.html"
    success_url = reverse_lazy("my_profile")
    
    
    def get_success_url(self) -> str:
        return reverse_lazy("my_profile",kwargs={"pk":self.request.user.pk})
    

#Template User confirmation

class TemplateInternetUserView(LoginRequiredMixin,TemplateView):
    template_name = "user_temp/check.html"


#Delete User
class DeleteInternetUserView(LoginRequiredMixin,DeleteView):
    model = User
    success_url = reverse_lazy("index")