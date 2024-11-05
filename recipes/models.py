from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#
ing_quant = (
    ("<4","menos de 4 ingredientes"),
    ("<8","menos de 8 ingredientes"),
    (">8","mas de 8 ingredientes"),
)


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=150)
    ing_category = models.CharField(choices=ing_quant,max_length=100)
    description = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    reference = models.URLField(blank=True)
    
    
    def __str__(self) -> str:
        return f"{self.recipe_name} Pk:{self.pk}"
    



#Measure unit weight
msr_quant = (
    ("kg","Kilogramo (kg)"),
    ("g","Gramo (g)"),
    ("mg","Miligramo (mg)"),
    ("l","Litro (l)"),
    ("dl","Decilitro (dl)"),
    ("ml","Mililitro (ml)"),
)

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=60)
    quantity = models.DecimalField(max_digits=16,decimal_places=2)
    measure_quantity = models.CharField(choices=msr_quant,max_length=255,default=msr_quant[0])
    recipe_fgk = models.ForeignKey(Recipe,on_delete=models.CASCADE,null=True)
   
   
   
    def __str__(self):
       return f"{self.ingredient_name} {self.quantity} {self.measure_quantity}"
  