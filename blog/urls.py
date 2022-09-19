from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('recette/<int:id_recette>', views.recette, name="recette"),
    path('redirect_django', views.redirect_django, name='redirect_django'),
    path('view_redirection', views.view_redirection, name="view_redirection"),
    path('homepage', views.homepage, name="homepage"),
    path('categorie/<int:id_categorie>', views.categorie, name="categorie"),
    path('inscription', views.inscription, name="inscription"),
    path('connexion', views.connexion, name="connexion"),
    path('deconnexion', views.deconnexion, name="deconnexion"),
]

