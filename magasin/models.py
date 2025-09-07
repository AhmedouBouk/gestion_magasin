from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Localisation(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "localisation"
        verbose_name_plural = "localisations"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Etat(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "état"
        verbose_name_plural = "états"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=150)

    # ⚠️ defaults=1 to satisfy existing rows during migration (option 2)
    # Assumes rows with id=1 will exist (via the init script below)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name="produits",
        default=1,
    )
    localisation = models.ForeignKey(
        Localisation,
        on_delete=models.PROTECT,
        related_name="produits",
        default=1,
    )
    etat = models.ForeignKey(
        Etat,
        on_delete=models.PROTECT,
        related_name="produits",
        default=1,
    )

    reference_modele = models.CharField(max_length=150, blank=True)
    quantite = models.PositiveIntegerField(default=1)
    observations = models.TextField(blank=True)

    class Meta:
        ordering = ["nom"]
        unique_together = ("nom", "categorie", "localisation")

    def __str__(self):
        return f"{self.nom} / {self.categorie} / {self.localisation}"

class Transfert(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='transferts')
    # ⚠️ on n’utilise PAS 'localisation' existante : on stocke la VILLE (texte libre)
    ville = models.CharField(max_length=120)
    motif = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-cree_le']

    def __str__(self):
        return f"Transfert {self.produit} → {self.ville} ({self.cree_le:%Y-%m-%d %H:%M})"
