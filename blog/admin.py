from django.contrib import admin
from blog.models import Recette, Categorie, Member, Ingredient, Commentaire

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'pseudo', 'mdp', 'email', 'date_inscription')
    list_filter = ('id', 'nom', 'pseudo', 'email')
    ordering = ('id',)
    search_fields = ('nom','pseudo','email')
    
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'quantite', 'unit', 'recette')
    list_filter = ('nom', 'recette')
    ordering = ('recette',)
    search_fields = ('nom',)
    
admin.site.register(Categorie)
admin.site.register(Recette)
admin.site.register(Member)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Commentaire)
