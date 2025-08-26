from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=150)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="produits")

    class Meta:
        ordering = ["nom"]
        unique_together = ("nom", "categorie")

    def __str__(self):
        return f"{self.nom} ({self.categorie})"
