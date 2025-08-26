import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_magasin.settings")
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from magasin.models import Categorie, Localisation, Etat

CATEGORIES = [
    "Matériel de diffusion",
    "Matériel audio",
    "Matériel d’enregistrement",
    "Matériel informatique",
    "Matériel électrique",
    "Matériel de transmission",
    "Consommables",
    "Mobilier de bureau",
]

LOCALISATIONS = [
    "Studio principal",
    "Salle technique",
    "Studio A",
    "Studio B",
    "Studio reportage",
    "Salle montage",
    "Bureau administratif",
    "Magasin câblage",
    "Salle serveurs",
    "Site antenne",
    "Magasin consommables",
    "Bureaux",
]

ETATS = ["Bon", "Neuf"]


def run():
    print("⚠️  Flush database (suppression des données)…")
    call_command("flush", "--noinput")

    print("🔧 Migrate…")
    call_command("migrate")

    print("📚 Insertion catégories…")
    for i, nom in enumerate(CATEGORIES, start=1):
        obj, _ = Categorie.objects.get_or_create(nom=nom)
        # assure que la 1re entrée (id=1) existe pour le default
        if i == 1 and obj.id != 1:
            pass  # pas critique; le default=1 fonctionne si id=1 existe

    print("📍 Insertion localisations…")
    for i, nom in enumerate(LOCALISATIONS, start=1):
        obj, _ = Localisation.objects.get_or_create(nom=nom)
        if i == 1 and obj.id != 1:
            pass

    print("✅ Insertion états…")
    for i, nom in enumerate(ETATS, start=1):
        obj, _ = Etat.objects.get_or_create(nom=nom)
        if i == 1 and obj.id != 1:
            pass

    print("👤 Création administrateur…")
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin", email="admin@gmail.com", password="1234admin"
        )
        print("Admin créé : admin / 1234admin")
    else:
        print("Admin déjà existant — mot de passe non modifié.")

    print("✅ Terminé.")


if __name__ == "__main__":
    run()
