from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView 
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from .models import Categorie, Produit, Etat, Localisation , Transfert
from .forms import FormulaireCategorie, FormulaireProduit , FormulaireTransfert
import csv
from io import BytesIO
from datetime import datetime
from django.views.generic import ListView


# --- Auth ---
class ConnexionView(LoginView):
    template_name = "login.html"


class DeconnexionView(LogoutView):
    next_page = reverse_lazy("connexion")


# --- Accueil (Dashboard) ---
# views.py
from django.db.models import Q, Count  # <-- ajoute Count

@method_decorator(login_required, name="dispatch")
class AccueilView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        produits = Produit.objects.all()
        categories = Categorie.objects.all()
        etats = Etat.objects.all()
        localisations = Localisation.objects.all()

        request = self.request
        search = request.GET.get("search", "").strip()
        categorie_id = request.GET.get("categorie", "").strip()
        etat_id = request.GET.get("etat", "").strip()
        localisation_id = request.GET.get("localisation", "").strip()

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

        # 🔎 garder uniquement les produits qui n'ont JAMAIS été transférés
        produits = produits.annotate(n_trans=Count('transferts')).filter(n_trans=0)

        ctx.update({
            "categories": categories,
            "etats": etats,
            "localisations": localisations,
            "produits": produits,
            "search": search,
            "categorie_id": categorie_id,
            "etat_id": etat_id,
            "localisation_id": localisation_id,
        })
        return ctx


def _filtered_produits_from_request(request):
    """Retourne le queryset de produits filtré selon les mêmes critères que l'accueil."""
    produits = Produit.objects.all()
    search = request.GET.get("search", "").strip()
    categorie_id = request.GET.get("categorie", "").strip()
    etat_id = request.GET.get("etat", "").strip()
    localisation_id = request.GET.get("localisation", "").strip()

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
    return produits


@login_required
def produits_export_excel(request):
    """Exporte les produits (avec filtres) en CSV ouvrable dans Excel."""
    produits = _filtered_produits_from_request(request)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="produits_{now}.csv"'

    # Write UTF-8 BOM so Excel on Windows detects encoding properly
    response.write("\ufeff")
    writer = csv.writer(response)
    # En-têtes comme dans home.html
    writer.writerow([
        "Nom",
        "Référence / Modèle",
        "Catégorie",
        "Localisation",
        "État",
        "Quantité",
        "Observations",
    ])
    for p in produits.select_related("categorie", "localisation", "etat"):
        writer.writerow([
            p.nom,
            p.reference_modele or "",
            p.categorie.nom if p.categorie_id else "",
            p.localisation.nom if p.localisation_id else "",
            p.etat.nom if p.etat_id else "",
            p.quantite,
            (p.observations or "").replace("\r\n", " ").replace("\n", " "),
        ])

    return response


@login_required
def produits_export_pdf(request):
    """Exporte les produits (avec filtres) en PDF. Nécessite reportlab."""
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
    except ImportError:
        return HttpResponse(
            "Le module 'reportlab' n'est pas installé. Installez-le avec: pip install reportlab",
            content_type="text/plain; charset=utf-8",
            status=500,
        )

    produits = _filtered_produits_from_request(request).select_related("categorie", "localisation", "etat")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=18, rightMargin=18, topMargin=18, bottomMargin=18)

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("Liste des produits", styles["Title"])
    elements.append(title)

    data = [[
        "Nom",
        "Référence / Modèle",
        "Catégorie",
        "Localisation",
        "État",
        "Quantité",
        "Observations",
    ]]

    for p in produits:
        data.append([
            p.nom,
            p.reference_modele or "",
            p.categorie.nom if p.categorie_id else "",
            p.localisation.nom if p.localisation_id else "",
            p.etat.nom if p.etat_id else "",
            str(p.quantite),
            p.observations or "",
        ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.beige]),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="produits_{now}.pdf"'
    return resp


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

# Création via le pop-up (POST)
@login_required
def transfert_creer(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == "POST":
        form = FormulaireTransfert(request.POST)
        if form.is_valid():
            tr = form.save(commit=False)
            tr.produit = produit
            tr.save()  # auto horodaté
    # On revient au dashboard (peut être remplacé par un redirect vers la liste)
    return redirect("accueil")


# Liste des transferts
@method_decorator(login_required, name="dispatch")
class TransfertListeView(ListView):
    template_name = "transferts.html"
    model = Transfert
    context_object_name = "transferts"
    paginate_by = 50

