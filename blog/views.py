from django.shortcuts import render
from django.http import HttpResponse,  Http404
from django.shortcuts import redirect
from blog.models import Recette, Categorie, Member, Ingredient, Commentaire
from .forms import InscriptionForm, CommentaireForm, ConnexionForm
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg 
from math import floor

def index (request):
    
    member = None
    member_id = request.session.get('member_id')
    if(member_id):
        member = Member.objects.get(pk=member_id)

    recettes = Recette.objects.all()#Nous sélectionnons toutes nos recettes
    categories = Categorie.objects.all().order_by('nom')#Nous sélectionnons toutes nos catégories
    
    return render(request, 'blog/index.html', {
        'recettes':recettes, 
        'categories':categories,
        'member':member})

def redirect_django(request):
    return redirect('https://www.djangoproject.com')

def view_redirection(request):
    return HttpResponse("Vous avez été redirigé")

def homepage (request):
    return render(request, 'blog/index.html')

def recette (request, id_recette):
        
    categories = Categorie.objects.all().order_by('nom')
    recette = Recette.objects.get(pk=id_recette)
    list_ingredient = recette.ingredient_set.all()
    
    note = None
    note_value = floor(recette.commentaire_set.all().aggregate(Avg('note'))['note__avg'])
    if note_value:
        note = floor(note_value)
    
    if (request.method == 'POST'):   
        form = CommentaireForm(request.POST)
        
        if form.is_valid():
            auteur = form.cleaned_data['auteur']
            contenu = form.cleaned_data['contenu']
            note = form.cleaned_data['note']
            
            #crée le membre et l'enregistre en base de données.
            commentaire = Commentaire(auteur = auteur, contenu = contenu, note = note, recette_id = id_recette)
            commentaire.save()
                    
    else : 
        form = CommentaireForm()
    
    list_commentaire = recette.commentaire_set.all()
    
    return render(request, 'blog/recette.html', {
        'ingredients': list_ingredient,
        'recette': recette,
        'commentaires': list_commentaire,
        'categories': categories,
        'form': form,
        'note':note})

def categorie (request, id_categorie):
    
    member = None
    member_id = request.session.get('member_id')
    if(member_id):
        member = Member.objects.get(pk=member_id) 
    
    categorie = Categorie.objects.get(pk=id_categorie) #Nous sélectionnons la catégorie indiqué via categorie_id
    categories = Categorie.objects.all().order_by('nom')#Nous séléctionnons toutes nos catégories
    recettes = categorie.recette_set.all()#Nous sélectionnons toutes les recettes de la catégorie récupéré précedemment
    
    return render(request, 'blog/categorie.html', {
        'categorie': categorie, 
        'categories':categories, 
        'recettes':recettes,
        'member': member})

def inscription (request):
    
    if (request.method == 'POST'):
        
        form = InscriptionForm(request.POST)
        
        if form.is_valid():
            nom = form.cleaned_data['nom']
            pseudo = form.cleaned_data['pseudo']
            email = form.cleaned_data['email']
            mdp = form.cleaned_data['mdp']
            
            mdp_encoded = make_password(mdp)
            
            #crée le membre et l'enregistre en base de données.
            member = Member(nom = nom, pseudo = pseudo, email = email, mdp = mdp_encoded)
            member.save()
            
            #ajoute dans la session l'objet membre
            request.session['member_id'] = member.id
            
            #rediriger sur la page d'acceuil
            return redirect(index)
                    
    else : 
        form = InscriptionForm()

    return render(request, 'blog/inscription.html', {'form':form})

def connexion(request):
    
    if(request.method == "POST"):
        
        form = ConnexionForm(request.POST)
        
        if form.is_valid():
            
            member= None
            
            pseudo = form.cleaned_data['pseudo']
            mdp = form.cleaned_data['mdp']
        
        try:
            member = Member.objects.get(pseudo=pseudo)
        except Member.DoesNotExist:
            pass
        
        if member and check_password(mdp, member.mdp):
            
            request.session['member_id'] = member.id
            
            return redirect(index)
        else:
            form.errors['__all__'] = form.error_class(['Pseudo ou mot de passe incorrect'])
    else:
        form = ConnexionForm()
    
    return render(request, 'blog/connexion.html', {'form':form})
    
    
def deconnexion(request):
    #nettoie les informations contenu dans la session
    request.session.clear()
    
    #redirige vers la page d'acceuil
    return redirect(index)
