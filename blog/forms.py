from django import forms 
from django.core import validators
from django.core.exceptions import ValidationError

class InscriptionForm(forms.Form):
    nom = forms.CharField(max_length=100, label="Nom", 
        widget=forms.TextInput(attrs={'placeholder':'Votre nom *', 'class': 'inputChamp'}))
    pseudo = forms.CharField(max_length=100, label="Pseudo", 
        widget=forms.TextInput(attrs={'placeholder':'Votre pseudo *', 'class': 'inputChamp'}))
    email = forms.CharField(max_length=200, label="Adresse mail", validators=[validators.validate_email],
        widget=forms.EmailInput(attrs={'placeholder':'Votre adresse mail *', 'class': 'inputChamp'}))
    mdp = forms.CharField(label="Mode de passe", 
        widget=forms.PasswordInput(attrs={'placeholder':'Votre mot de passe *', 'class': 'inputChamp'}))
    conf_mdp = forms.CharField(label="Confirmation du mode de passe", 
        widget=forms.PasswordInput(attrs={'placeholder':'Votre mot de passe *', 'class': 'inputChamp'}))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        if "test" in data:
            raise ValidationError("Votre email n'est pas une adresse valide")
        
        return data 
    
    def clean(self):
        cleaned_data = super().clean()
        
        if(len(cleaned_data)):
            cleaned_mdp = cleaned_data['mdp']
            cleaned_conf_mdp = cleaned_data['conf_mdp']
            
            if (cleaned_mdp != cleaned_conf_mdp):
                raise ValidationError("Vos mots de passe ne sont pas identiques")
            
        return cleaned_data
    
class CommentaireForm(forms.Form):
    auteur = forms.CharField(max_length=100, label="Auteur :", 
        widget=forms.TextInput(attrs={'placeholder':'Auteur *', 'class': 'inputChamp'}))
    contenu = forms.CharField(max_length=100, label="Contenu :", 
        widget=forms.TextInput(attrs={'placeholder':'Votre commentaire *', 'class': 'inputTextArea', 'rows':'4'}))
    note = forms.ChoiceField(label="Note :", choices=[(x, x) for x in range(1,6)])
    
class ConnexionForm(forms.Form):
    pseudo = forms.CharField(max_length=100, label="Pseudo :", 
        widget=forms.TextInput(attrs={'placeholder':'Pseudo *', 'class': 'inputChamp'}))
    mdp = forms.CharField(max_length=100, label="Mot de passe :", 
        widget=forms.TextInput(attrs={'placeholder':'Mot de passe *', 'class': 'inputChamp'}))