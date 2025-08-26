from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Categorie, Produit
from .forms import FormulaireCategorie, FormulaireProduit


class ConnexionView(LoginView):
    # tes templates sont directement dans magasin/templates/
    template_name = "login.html"


class DeconnexionView(LogoutView):
    pass


@method_decorator(login_required, name="dispatch")
class AccueilView(TemplateView):
    # page unique qui affiche les listes
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Categorie.objects.all().order_by("nom")
        ctx["produits"] = Produit.objects.select_related("categorie").all().order_by("nom")
        return ctx


# ---------- Catégories ----------
@method_decorator(login_required, name="dispatch")
class CategorieCreer(CreateView):
    model = Categorie
    form_class = FormulaireCategorie
    template_name = "add.html"
    success_url = reverse_lazy("accueil")


@method_decorator(login_required, name="dispatch")
class CategorieModifier(UpdateView):
    model = Categorie
    form_class = FormulaireCategorie
    template_name = "update.html"
    success_url = reverse_lazy("accueil")


@login_required
def categorie_supprimer(request, pk: int):
    categorie = get_object_or_404(Categorie, pk=pk)
    categorie.delete()
    return redirect("accueil")


# ---------- Produits ----------
@method_decorator(login_required, name="dispatch")
class ProduitCreer(CreateView):
    model = Produit
    form_class = FormulaireProduit
    template_name = "add.html"
    success_url = reverse_lazy("accueil")


@method_decorator(login_required, name="dispatch")
class ProduitModifier(UpdateView):
    model = Produit
    form_class = FormulaireProduit
    template_name = "update.html"
    success_url = reverse_lazy("accueil")


@login_required
def produit_supprimer(request, pk: int):
    produit = get_object_or_404(Produit, pk=pk)
    produit.delete()
    return redirect("accueil")
