from django import forms
from cookbook.ingredients.models import Category, Ingredient

class AddIngredientForm(forms.ModelForm):
