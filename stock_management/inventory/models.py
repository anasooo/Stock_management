from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Fournisseur(models.Model):
    """Model definition for Fournisseur."""
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    """Model definition for Produit."""
    nom = models.CharField(max_length=200)
    reference = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Client(models.Model):
    """Model definition for Client."""
    nom = models.CharField(max_length=100)
    preneom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    """Model definition for Commande."""
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('TRAITEE', 'Traitee'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Commande {self.id} - {self.client}'

class LigneCommande(models.Model):
    """Model definition for LigneCommande."""
    commande = models.ForeignKey(Commande, related_name='lignes', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        #verifier si le produit est en stock
        if self.quantite > self.produit.quantite_stock:
            raise ValueError('Quantité insuffisante en stock')
        
        #mettre à jour la quantité en stock
        self.produit.quantite_stock -= self.quantite
        self.produit.save()

        #calculer le total de la ligne de commande
        self.prix_unitaire = self.produit.prix_unitaire

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"