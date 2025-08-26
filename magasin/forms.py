from django import forms
from .models import Categorie, Produit

class FormulaireCategorie(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ["nom"]

class FormulaireProduit(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ["nom","categorie"]
