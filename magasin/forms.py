from django import forms
from .models import Categorie, Produit, Localisation, Etat


class FormulaireCategorie(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ["nom"]
        labels = {"nom": "Nom de la catégorie"}
        widgets = {
            "nom": forms.TextInput(attrs={"placeholder": "Ex. Matériel audio"})
        }


class FormulaireProduit(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            "nom",
            "categorie",
            "localisation",
            "etat",
            "reference_modele",
            "quantite",
            "observations",
        ]
        labels = {
            "nom": "Nom du matériel / produit",
            "categorie": "Catégorie",
            "localisation": "Localisation",
            "etat": "État",
            "reference_modele": "Référence / Modèle",
            "quantite": "Quantité",
            "observations": "Observations",
        }
        widgets = {
            "categorie": forms.Select(),
            "localisation": forms.Select(),
            "etat": forms.Select(),
            "reference_modele": forms.TextInput(attrs={"placeholder": "Ex. Yamaha MG12XU"}),
            "quantite": forms.NumberInput(attrs={"min": 1}),
            "observations": forms.Textarea(attrs={"rows": 3, "placeholder": "Notes..."}),
        }
