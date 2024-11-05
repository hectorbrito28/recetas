#Django utilities
from typing import Any
from django.shortcuts import redirect,HttpResponseRedirect,render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView,DetailView
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
#Form
from .forms import  RecipeForm,IngredientForm
from django.forms import inlineformset_factory

#Model
from .models import Recipe,Ingredient

#PDF

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader


# Create your views here.

#Base recipe

class RecipeInline():
    
    form_class = RecipeForm
    model = Recipe
    template_name = "probre.html"
    
    
    def form_valid(self,form):
      
        #Get set of formsets from CreateRecipeView
        named_formsets = self.get_named_formsets()
        
        
        #Get total forms
        total_forms = len(named_formsets["ingredients"])
        
        #Get instance for modify
        ins = form.instance
        
        if total_forms <= 4:
            ins.ing_category = "<4"
            
        elif total_forms <= 8:
            ins.ing_category = "<8"
            
        else:
             ins.ing_category = ">8"
        
        #Set user     
        ins.user = self.request.user
        
        #Apply changes
        form.instance = ins 
        
        
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form,warning="Warning you haven't complete any ingredient"))
        
        
        
        
        #Save in object the form recipe
        self.object = form.save()
        
        #Save the form
        form.save()
        
        
        #Run the formsets dict
        for name, formset in named_formsets.items():
            
            #Search attribute that have the same name like formset_{0}_valid
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            
            
            #If that name exists, call fuction and save that formset with that custom fuction
            if formset_save_func is not None:
                
                formset_save_func(formset)
            else:
                #Else save normaly
                formset.save()
        
        return HttpResponseRedirect(self.get_success_url())
        
        

    #Custom function saving    
    def formset_ingredients_valid(self,formset):
        
        ingredient = formset.save(commit=False)
        
        
        for obj in formset.deleted_objects:
            
            obj.delete()
        
        for ing in ingredient:
            ing.recipe_fgk = self.object
            ing.save()


   
             

#Create

class CreateRecipeView(LoginRequiredMixin,RecipeInline,CreateView):
    
    model = Recipe
    template_name = "recipes_temp/create_recipe.html"
    success_url = reverse_lazy("index")
    form_class = RecipeForm
    
    #Get older context and add it new dictionary that comes from funct= get_named_formsets 
    def get_context_data(self, **kwargs):
        ctx = super(CreateRecipeView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    
    def get_named_formsets(self):
        
        #Rewrite formset_factory
        
        IngredientsInlineFormSet = inlineformset_factory(
        Recipe,Ingredient,
        form=IngredientForm,
        extra=1,can_delete_extra=True,
        can_delete=False,
        )
        
        if self.request.method == "GET":
            return {
                "ingredients":IngredientsInlineFormSet(prefix="ingredients")
            }
        
        else:
             return {
                "ingredients":IngredientsInlineFormSet(self.request.POST or None, prefix="ingredients")
            }



#Update

class UpdateRecipeView(LoginRequiredMixin,RecipeInline,UpdateView):
    template_name = "recipes_temp/create_recipe.html"
    
    
    def get_success_url(self) -> str:
        return reverse_lazy("recipes_list",kwargs={"pk":self.request.user.pk})
    
    
    #Get older context and add it new dictionary that comes from funct= get_named_formsets 
    def get_context_data(self, **kwargs):
        
        ctx = super(UpdateRecipeView, self).get_context_data(**kwargs)
        
        ctx['named_formsets'] = self.get_named_formsets()
        
        #gives total formsets saved
        ctx["total_formsets"] = len(ctx['named_formsets']["ingredients"])
        
        return ctx
    
    
    
    def get_named_formsets(self):
        IngredientsInlineFormSet = inlineformset_factory(
        Recipe,Ingredient,
        form=IngredientForm,
        extra=0,can_delete_extra=True,
        can_delete=False,
        )
        
        return {
                "ingredients":IngredientsInlineFormSet(self.request.POST or None, prefix="ingredients",instance=self.object)
            }


#Delete
@login_required
def delete_ingredient(request,pk):
    if pk:
        ing = Ingredient.objects.get(id=pk)
        ing.delete()
    return redirect("UpdateRecipe",pk=ing.recipe_fgk.pk)


#Delete recipe
@login_required
def delete_recipe(request,pk):
    if pk:
        rcp = Recipe.objects.get(id=pk)
        rcp.delete()
    return redirect("recipes_list",pk=request.user.pk)


#Index

class ListIndexView(ListView):
    model = Recipe
    template_name = "recipes_temp/index.html"
    context_object_name = "recipes"

    
    def get_queryset(self):
        if self.request.GET:
            
            if self.request.GET.get("search_text"):
            
                search_text = self.request.GET["search_text"]
                
                new_queryset = Recipe.objects.filter(recipe_name__startswith=search_text)
                
                return new_queryset
            
            elif self.request.GET.get("categories") and  self.request.GET["categories"] != "0":
                search_text = self.request.GET["categories"]
                
                new_queryset = Recipe.objects.filter(ing_category=search_text)
                
                return new_queryset
            
            else:
                return Recipe.objects.all()

                
        else:
            return Recipe.objects.all()

#Search_box
@login_required
def search_funct(request):
    search_text = request.GET["search_text"]
    
    
    
    
#List recipes

class ListRecipesView(LoginRequiredMixin,ListView):
    template_name = "recipes_temp/list_recipes.html"
    context_object_name = "recipes"
    
    
    def get_queryset(self):
        if self.request.GET and self.request.GET["category"] != "0":
            
            search_text = self.request.GET["category"]
            
            
            new_queryset = Recipe.objects.filter(ing_category=search_text,user=self.request.user)
            
            return new_queryset
        else:
            return Recipe.objects.filter(user=self.request.user)
        
        



class DetailRecipesView(DetailView):
    model = Recipe
    template_name = "recipes_temp/detail_recipe.html"
    context_object_name = "recipe"
    
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        recipe_id = self.request.resolver_match.kwargs["pk"]
        
        ingredients = Ingredient.objects.filter(recipe_fgk=recipe_id)
        
        ctx["ingredients"]  = ingredients
        
        
        
        return ctx
    



def reset_values():
    y_space = 450
    x_space = 20
    letter = 0
    
    return y_space,x_space,letter
    


def download_pdf(request,id):
    
    rcp = Recipe.objects.get(id=id)
    
    title = rcp.recipe_name
    
    description = str(rcp.description)
    
    ingredients = list()
    
    obj_ing = Ingredient.objects.filter(recipe_fgk__id=rcp.id)
    
    #listing ingredients
    for ing in obj_ing:
        name = f"{ing.ingredient_name} {ing.quantity}-{ing.measure_quantity}"
        ingredients.append(name)
    
    
    
    
    response = HttpResponse(content_type="application/pdf")
        
    response_instance = canvas.Canvas(response,pagesize=(400,500))
    
    y_space = 450
    
    x_space = 20
        
    letter = 0
    
    #Title
    response_instance.setFont("Courier",20)
    
    for i in title:

         
        if letter == 33:
            letter = 0
            y_space = y_space - 18
            x_space = 20
        
            
        response_instance.drawString(x_space,y_space,i)
        x_space += 10
        letter +=1
    
    y_space -= 20
    x_space = 20    
    letter = 0
    
    
    
    #Ingredients
    response_instance.setFont("Courier",10)
    for i in ingredients:
        print(y_space)
        
        if y_space <= 30:
            response_instance.showPage()
            response_instance.setFont("Courier",10)
            y_space = 450
            response_instance.drawString(20,y_space,i)
        
        elif len(i) >= 19:
            y_space -= 20
            response_instance.drawString(20,y_space,i)
        
        else:
           
            y_space -= 20
            
            response_instance.drawString(x_space,y_space,i)
            
            
    
    #Reset
    y_space,x_space,letter = reset_values()
    
    #New page
    response_instance.showPage()

        
    #Description    
    response_instance.setFont("Courier",20)
    response_instance.drawString(x_space,y_space,"Description:")
    response_instance.setFont("Courier",10)
    y_space -= 20

    
    for i in description:
        if letter == 60:
            letter = 0
            y_space = y_space - 15
            x_space = 20
        
            
        response_instance.drawString(x_space,y_space,i)
        x_space += 6
        letter +=1
   
    response_instance.save()

    
    

    
    return response