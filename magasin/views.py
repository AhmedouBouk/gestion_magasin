from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Categorie, Produit, Etat, Localisation
from .forms import FormulaireCategorie, FormulaireProduit


# --- Auth ---
class ConnexionView(LoginView):
    template_name = "login.html"


class DeconnexionView(LogoutView):
    next_page = reverse_lazy("connexion")


# --- Accueil (Dashboard) ---
@method_decorator(login_required, name="dispatch")
class AccueilView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        produits = Produit.objects.all()
        categories = Categorie.objects.all()
        etats = Etat.objects.all()
        localisations = Localisation.objects.all()

        # Récupération des filtres (GET)
        request = self.request
        search = request.GET.get("search", "").strip()
        categorie_id = request.GET.get("categorie", "").strip()
        etat_id = request.GET.get("etat", "").strip()
        localisation_id = request.GET.get("localisation", "").strip()

        # Application des filtres
        if search:
            produits = produits.filter(
                Q(nom__icontains=search)
                | Q(reference_modele__icontains=search)
                | Q(observations__icontains=search)
            )
        if categorie_id:
            produits = produits.filter(categorie_id=categorie_id)
        if etat_id:
            produits = produits.filter(etat_id=etat_id)
        if localisation_id:
            produits = produits.filter(localisation_id=localisation_id)

        # Contexte
        ctx.update(
            {
                "categories": categories,
                "etats": etats,
                "localisations": localisations,
                "produits": produits,
                "search": search,
                "categorie_id": categorie_id,
                "etat_id": etat_id,
                "localisation_id": localisation_id,
            }
        )
        return ctx


# --- Catégories ---
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
def categorie_supprimer(request, pk):
    cat = get_object_or_404(Categorie, pk=pk)
    cat.delete()
    return redirect("accueil")


# --- Produits ---
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
def produit_supprimer(request, pk):
    prod = get_object_or_404(Produit, pk=pk)
    prod.delete()
    return redirect("accueil")


@login_required
def accueil(request):
    # Cette vue n'est plus utilisée car les filtres sont gérés dans AccueilView.
    # Conservée uniquement si référencée ailleurs.
    from django.shortcuts import render
    produits = Produit.objects.all()
    return render(request, "home.html", {"produits": produits})
