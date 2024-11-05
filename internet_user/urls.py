"""Internet user urls.py"""

from django.urls import path
from .views import CreateInternetUserView,DeleteInternetUserView,DetailInternetUserView,UpdateInternetUserView,TemplateInternetUserView


urlpatterns = [
    path("signup/",CreateInternetUserView.as_view(),name="Signup"),
    path("Delete_account/<int:pk>",DeleteInternetUserView.as_view(),name="Delete_account"),
    path("Confirmation/",TemplateInternetUserView.as_view(),name="Confirmation"),
    path("Update_account/<int:pk>",UpdateInternetUserView.as_view(),name="Update_account"),
    path("My_profile/<int:pk>",DetailInternetUserView.as_view(),name="my_profile")
]

