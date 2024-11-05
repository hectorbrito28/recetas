from django.urls import path
#Views
from .views import CreateRecipeView, UpdateRecipeView, ListRecipesView, ListIndexView, DetailRecipesView, delete_ingredient, delete_recipe, search_funct, download_pdf


urlpatterns = [
    path("",ListIndexView.as_view(),name="index"),
    path("CreateRecipe/",CreateRecipeView.as_view(),name="CreateRecipe"),
    path("UpdateRecipe/<int:pk>",UpdateRecipeView.as_view(),name="UpdateRecipe"),
    path("Delete_ingredient/<int:pk>",delete_ingredient,name="delete_ing"),
    path("Delete_recipe/<int:pk>",delete_recipe,name="delete_rcp"),
    path("My_recipes/<int:pk>",ListRecipesView.as_view(),name="recipes_list"),
    path("Detail_recipe/<int:pk>",DetailRecipesView.as_view(),name="detail_recipes"),
    #functions
    path("search/",search_funct,name="search_box"),
    path("downloading/<int:id>",download_pdf,name="download")
]