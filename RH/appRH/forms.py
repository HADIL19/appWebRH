# forms.py
from django import forms
from .models import Candidat, Contrat, Entretien, Evaluation, Favori, OffreEmploi, Employe, Conge, Salaire, Formation, Service
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date


class InscriptionForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmployeForm(forms.ModelForm):  
     class Meta: 
        model = Employe  
        fields = "__all__"

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['type_conge', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class OffreEmploiForm(forms.ModelForm):
    class Meta:
        model = OffreEmploi
        fields = "__all__"

class inscrireoffreForm(forms.ModelForm):
    class Meta:
        model = Candidat  # Le formulaire est basé sur le modèle Candidat
        fields = ['nomC', 'emailC', 'telC', 'cv_path']  # Les champs que l'on veut afficher dans le formulaire
        


class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = ['date_entretien', 'heure', 'type_entretien', 'recruteur']
        recruteur = forms.ModelChoiceField(queryset=Employe.objects.all(), empty_label="Sélectionnez un recruteur")
        widgets = {
            'date_entretien': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
        }

class MassroufForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = ['avance_massrouf']
        widgets = {
            'avance_massrouf': forms.NumberInput(attrs={'min': 0}),
        }

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = ['employe', 'type_contrat', 'date_debut', 'date_fin', 'periode_essai','preavis']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'theme', 'formateure','date_debut', 'date_fin', 'employe']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }


class ServiceForm(forms.ModelForm):
     class Meta: 
        model = Service
        fields = "__all__"

class FavoriForm(forms.ModelForm):
    class Meta:
        model = Favori
        fields = ['nom', 'url']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom de la fonctionnalité'}),
            'url': forms.TextInput(attrs={'placeholder': 'URL de la fonctionnalité'}),
        }

class AssignManagerForm(forms.Form):
    manager = forms.ModelChoiceField(queryset=Employe.objects.filter(fonction="Manager"))
    employes = forms.ModelMultipleChoiceField(
        queryset=Employe.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class SalaireForm(forms.ModelForm):
     class Meta: 
        model = Salaire
        fields = ['employe','salaire_de_base','annee','mois','prime','absences']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['date', 'score', 'commentaire', 'type_evaluation']  # On ne met pas 'employe'

    # Ajout d'un widget de sélection de date
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today  # Utilise la date actuelle par défaut
    )