"""Formset Recipes"""
from typing import Any
from django import forms
from django.forms import inlineformset_factory

#Models
from .models import Ingredient, Recipe


ing_quant = (
    ("<4","menos de 4 ingredientes"),
    (">4","mas de 4 ingredientes"),
    (">8","mas de 8 ingredientes"),
    (">14","mas de 14 ingredientes"),
)

class RecipeForm(forms.ModelForm):
    ing_category = forms.CharField(required=False,widget=forms.NumberInput(attrs={"hidden":"True"}))
    
    class Meta:
        model = Recipe
        fields = ["recipe_name","description","reference","ing_category"]
        widgets = {
            "recipe_name":forms.TextInput(attrs={
                "placeholder":"Recipe name"
            }),
            "description":forms.Textarea(attrs={"placeholder":"How to prepare"}),
            
            "reference":forms.URLInput(attrs={
                "placeholder":"URL Reference"
            }),
        }
    


#Measure unit weight
msr_quant = (
    ("kg","Kilogramo (kg)"),
    ("g","Gramo (g)"),
    ("mg","Miligramo (mg)"),
    ("l","Litro (l)"),
    ("dl","Decilitro (dl)"),
    ("ml","Mililitro (ml)"),
)

class IngredientForm(forms.ModelForm):
    
    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets ={
            "ingredient_name":forms.TextInput(attrs={"placeholder":"Ingredient name"}),
            "quantity":forms.NumberInput(attrs={"placeholder":"Total","required":"True"}),
        }
        
    
    def clean_ingredient(self):
        data = self.cleaned_data["quantity"]
        
        if not data:
            raise forms.ValidationError("Warning you haven't write any ingredient")

        return data


IngredientsInlineFormSet = inlineformset_factory(
    Recipe,Ingredient,
    form=IngredientForm,
    extra=2,can_delete_extra=True,
    can_delete=False,
    )