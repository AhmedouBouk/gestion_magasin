from django.contrib import admin
from .models import Categorie, Produit

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ("nom","categorie")
    list_filter = ("categorie",)
    search_fields = ("nom",)
