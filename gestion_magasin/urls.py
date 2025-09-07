from django.contrib import admin
from django.urls import path
from magasin import views as v

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("connexion/", v.ConnexionView.as_view(), name="connexion"),
    path("deconnexion/", v.DeconnexionView.as_view(), name="deconnexion"),

    # Accueil (liste Catégories + Produits)
    path("", v.AccueilView.as_view(), name="accueil"),

    # Catégories
    path("categories/creer/", v.CategorieCreer.as_view(), name="categorie_creer"),
    path("categories/<int:pk>/modifier/", v.CategorieModifier.as_view(), name="categorie_modifier"),
    path("categories/<int:pk>/supprimer/", v.categorie_supprimer, name="categorie_supprimer"),

    # Produits
    path("produits/creer/", v.ProduitCreer.as_view(), name="produit_creer"),
    path("produits/<int:pk>/modifier/", v.ProduitModifier.as_view(), name="produit_modifier"),
    path("produits/<int:pk>/supprimer/", v.produit_supprimer, name="produit_supprimer"),
    path("produits/export/excel/", v.produits_export_excel, name="produits_export_excel"),
    path("produits/export/pdf/", v.produits_export_pdf, name="produits_export_pdf"),
    # magasin/urls.py
    path("transferts/", v.TransfertListeView.as_view(), name="transferts_liste"),
    path("produits/<int:pk>/transferer/", v.transfert_creer, name="produit_transferer"),

]
