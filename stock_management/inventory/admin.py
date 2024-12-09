from django.contrib import admin
from .models import Fournisseur, Produit, Client, Commande, LigneCommande

# Register your models here.
@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone')
    search_fields = ('nom', 'email')

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'reference', 'prix_unitaire', 'quantite_stock', 'fournisseur')
    search_fields = ('nom', 'reference')
    list_filter = ('fournisseur',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'preneom', 'email', 'telephone')
    search_fields = ('nom', 'preneom', 'email')

class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1
    readonly_fields = ('prix_unitaire',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_commande', 'statut', 'total')
    list_filter = ('statut', 'date_commande')
    inlines = (LigneCommandeInline,)

    def save_model(self, request, obj, form, change):
        # calculer le total de la commande
        obj.total = sum(ligne.prix_unitaire * ligne.quantite for ligne in obj.lignes.all())
        super().save_model(request, obj, form, change)
        